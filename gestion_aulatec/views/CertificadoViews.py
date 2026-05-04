from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.utils import timezone

from gestion_aulatec.models import Certificado, Estudiante
from gestion_aulatec.utils.certificado_pdf import generar_certificado_pdf


# ─── Mixins de permisos ───────────────────────────────────────────

class EsAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        return redirect('gestion_aulatec:home')


class EsEstudianteMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.Rol == 'Estudiante'

    def handle_no_permission(self):
        return redirect('gestion_aulatec:home')


# ─── Vistas del Administrador ─────────────────────────────────────

class AdminSolicitudesView(EsAdminMixin, View):
    """Lista todas las solicitudes de certificados con filtro por estado."""

    def get(self, request):
        estado_filtro = request.GET.get('estado', 'pendiente')

        pendientes = Certificado.objects.filter(estado='pendiente').count()
        aprobados  = Certificado.objects.filter(estado='aprobado').count()
        rechazados = Certificado.objects.filter(estado='rechazado').count()

        if estado_filtro == 'todos':
            certificados = Certificado.objects.all()
        else:
            certificados = Certificado.objects.filter(estado=estado_filtro)

        return render(request, 'gestion_aulatec/admin_solicitudes.html', {
            'certificados': certificados,
            'pendientes': pendientes,
            'aprobados': aprobados,
            'rechazados': rechazados,
            'estado_filtro': estado_filtro,
        })


class DetalleCertificadoAdminView(EsAdminMixin, View):
    """Detalle de un certificado para el administrador."""

    def get(self, request, pk):
        certificado = get_object_or_404(Certificado, pk=pk)
        return render(request, 'gestion_aulatec/detalle_certificado_admin.html', {
            'certificado': certificado,
        })


class AprobarCertificadoView(EsAdminMixin, View):
    """Aprueba un certificado y genera el PDF."""

    def get(self, request, pk):
        certificado = get_object_or_404(Certificado, pk=pk, estado='pendiente')
        return render(request, 'gestion_aulatec/aprobar_certificado.html', {
            'certificado': certificado,
        })

    def post(self, request, pk):
        certificado = get_object_or_404(Certificado, pk=pk, estado='pendiente')
        certificado.estado = 'aprobado'
        certificado.fecha_aprobacion = timezone.now()
        certificado.aprobado_por = request.user
        certificado.save()
        messages.success(request, f'Certificado {certificado.codigo} aprobado correctamente.')
        return redirect('gestion_aulatec:admin_solicitudes')


class RechazarCertificadoView(EsAdminMixin, View):
    """Rechaza un certificado con motivo."""

    def get(self, request, pk):
        certificado = get_object_or_404(Certificado, pk=pk, estado='pendiente')
        return render(request, 'gestion_aulatec/rechazar_certificado.html', {
            'certificado': certificado,
        })

    def post(self, request, pk):
        certificado = get_object_or_404(Certificado, pk=pk, estado='pendiente')
        motivo = request.POST.get('motivo_rechazo', '').strip()
        if not motivo:
            messages.error(request, 'Debes indicar el motivo del rechazo.')
            return render(request, 'gestion_aulatec/rechazar_certificado.html', {
                'certificado': certificado,
            })
        certificado.estado = 'rechazado'
        certificado.motivo_rechazo = motivo
        certificado.save()
        messages.success(request, f'Certificado {certificado.codigo} rechazado.')
        return redirect('gestion_aulatec:admin_solicitudes')


class DescargarCertificadoPDFView(EsAdminMixin, View):
    """Descarga el PDF de un certificado aprobado."""

    def get(self, request, pk):
        certificado = get_object_or_404(Certificado, pk=pk, estado='aprobado')
        try:
            pdf_bytes = generar_certificado_pdf(certificado)
        except ImportError as e:
            messages.error(request, str(e))
            return redirect('gestion_aulatec:detalle_certificado_admin', pk=pk)

        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        filename = f"certificado_{certificado.codigo}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


# ─── Vistas del Estudiante ────────────────────────────────────────

class SolicitarCertificadoView(EsEstudianteMixin, View):
    """Formulario para que el estudiante solicite un certificado."""

    def _get_estudiante(self, request):
        return get_object_or_404(Estudiante, IdUsuario=request.user)

    def get(self, request):
        estudiante = self._get_estudiante(request)
        solicitudes_pendientes = Certificado.objects.filter(
            IdEstudiante=estudiante, estado='pendiente'
        ).count()
        return render(request, 'gestion_aulatec/solicitar_certificado.html', {
            'solicitudes_pendientes': solicitudes_pendientes,
        })

    def post(self, request):
        estudiante = self._get_estudiante(request)
        solicitudes_pendientes = Certificado.objects.filter(
            IdEstudiante=estudiante, estado='pendiente'
        ).count()

        if solicitudes_pendientes > 0:
            messages.error(request, 'Tienes solicitudes pendientes. Espera la respuesta antes de enviar otra.')
            return redirect('gestion_aulatec:solicitar_certificado')

        tipo = request.POST.get('tipo', 'estudio')
        observaciones = request.POST.get('observaciones', '').strip()

        Certificado.objects.create(
            IdEstudiante=estudiante,
            tipo=tipo,
            observaciones=observaciones or None,
        )
        messages.success(request, 'Solicitud enviada correctamente. El administrador la revisará pronto.')
        return redirect('gestion_aulatec:mis_certificados')


class MisCertificadosView(EsEstudianteMixin, View):
    """
    Lista los certificados del estudiante autenticado.
    Al cargar: marca como vencidos los aprobados expirados,
    y elimina definitivamente los vencidos con más de 7 días de gracia.
    """
    DIAS_GRACIA_ELIMINACION = 7

    def get(self, request):
        from django.utils import timezone

        estudiante = get_object_or_404(Estudiante, IdUsuario=request.user)
        ahora = timezone.now()

        # 1. Marcar como vencidos los aprobados cuya fecha_vencimiento ya pasó
        Certificado.objects.filter(
            IdEstudiante=estudiante,
            estado='aprobado',
            fecha_vencimiento__lt=ahora,
        ).update(estado='vencido')

        # 2. Eliminar definitivamente los vencidos con más de 7 días de gracia
        limite_eliminacion = ahora - timezone.timedelta(days=self.DIAS_GRACIA_ELIMINACION)
        Certificado.objects.filter(
            IdEstudiante=estudiante,
            estado='vencido',
            fecha_vencimiento__lt=limite_eliminacion,
        ).delete()

        # 3. Cargar los certificados restantes
        certificados = Certificado.objects.filter(IdEstudiante=estudiante)
        return render(request, 'gestion_aulatec/mis_certificados.html', {
            'certificados': certificados,
        })


class DescargarReporteNotasView(EsEstudianteMixin, View):
    """
    Descarga directa del reporte de notas con gráficas (PDF).
    Rate limit: una descarga cada 14 días por estudiante.
    """
    INTERVALO_DIAS = 14

    def get(self, request):
        from gestion_aulatec.models import Calificacion
        from gestion_aulatec.utils.reporte_notas_pdf import generar_reporte_notas_pdf
        from datetime import date

        estudiante = get_object_or_404(Estudiante, IdUsuario=request.user)

        # ── Rate limiting ──
        ahora = timezone.now()
        if estudiante.ultima_descarga_notas:
            dias_pasados = (ahora - estudiante.ultima_descarga_notas).days
            dias_restantes = self.INTERVALO_DIAS - dias_pasados
            if dias_restantes > 0:
                messages.warning(
                    request,
                    f'Puedes descargar tu reporte de notas en {dias_restantes} día{"s" if dias_restantes != 1 else ""}. '
                    f'El intervalo entre descargas es de {self.INTERVALO_DIAS} días.'
                )
                return redirect('gestion_aulatec:estudiante_dashboard')

        anio = date.today().year
        calificaciones = Calificacion.objects.filter(
            IdEstudiante=estudiante,
            AnioLectivo=anio,
        ).select_related('IdMateria', 'IdDocente__IdUsuario').order_by('Periodo', 'IdMateria')

        if not calificaciones.exists():
            messages.warning(request, 'No tienes calificaciones registradas este año para generar el reporte.')
            return redirect('gestion_aulatec:estudiante_dashboard')

        try:
            pdf_bytes = generar_reporte_notas_pdf(estudiante, calificaciones, anio)
        except ImportError as e:
            messages.error(request, str(e))
            return redirect('gestion_aulatec:estudiante_dashboard')

        # Actualizar fecha de última descarga
        estudiante.ultima_descarga_notas = ahora
        estudiante.save(update_fields=['ultima_descarga_notas'])

        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte_notas_{estudiante.IdUsuario.NumId}_{anio}.pdf"'
        return response


class DescargarCertificadoEstudianteView(EsEstudianteMixin, View):
    """El estudiante descarga su propio certificado aprobado y vigente."""

    def get(self, request, pk):
        from django.utils import timezone

        estudiante = get_object_or_404(Estudiante, IdUsuario=request.user)
        certificado = get_object_or_404(Certificado, pk=pk, IdEstudiante=estudiante)

        # Verificar que esté aprobado
        if certificado.estado != 'aprobado':
            messages.error(request, 'Este certificado no está disponible para descarga.')
            return redirect('gestion_aulatec:mis_certificados')

        # Verificar vigencia
        if certificado.fecha_vencimiento and certificado.fecha_vencimiento < timezone.now():
            messages.warning(
                request,
                f'Este certificado venció el {certificado.fecha_vencimiento.strftime("%d/%m/%Y")}. '
                f'Solicita uno nuevo si lo necesitas.'
            )
            return redirect('gestion_aulatec:mis_certificados')

        try:
            pdf_bytes = generar_certificado_pdf(certificado)
        except ImportError as e:
            messages.error(request, str(e))
            return redirect('gestion_aulatec:mis_certificados')

        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        filename = f"certificado_{certificado.codigo}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
