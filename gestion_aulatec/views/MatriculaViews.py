from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # Mixins para CBVs(Vistas basadas en clases)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, View, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db import IntegrityError,transaction
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import random
import string

from django.core.mail import send_mail
from django.conf import settings
from gestion_aulatec.forms import MatriculaForm
from gestion_aulatec.forms.MatriculaForm import MUNICIPIOS_COLOMBIA, EPS_COLOMBIA
from gestion_aulatec.models import Usuario,Estudiante,Matricula,Acudiente

#funcion para generar una constrasela aleatoria segura
def generar_contrasena_segura(longitud=12):                         
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contrasena


# Vistas CRUD Matricula
class MatriculaCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    form_class = MatriculaForm
    template_name = 'gestion_aulatec/matricula_form.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        return redirect('gestion_aulatec:home')

    def _ctx(self, form):
        return {'form': form, 'municipios': MUNICIPIOS_COLOMBIA, 'eps_lista': EPS_COLOMBIA}

    # Método GET: Muestra el formulario vacío
    def get(self, request, *args, **kwargs):
        from gestion_aulatec.models import Grado
        if not Grado.objects.exists():
            messages.warning(
                request,
                'No hay grados creados. Primero crea al menos un grado antes de registrar matrículas.'
            )
        return render(request, self.template_name, self._ctx(MatriculaForm()))

    # Método POST: Procesa el formulario enviado
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST) 
        if form.is_valid():
            try:
                # Usa una transacción atómica para garantizar que todo se guarde o nada se guarde.
                with transaction.atomic():
                    # --- 1. Crear/Obtener Usuario para el Estudiante
                    estudiante_usuario_data = {
                        'TipoId': form.cleaned_data['EstudianteTipoId'],
                        'NumId': form.cleaned_data['EstudianteNumId'],
                        'Nombres': form.cleaned_data['EstudianteNombres'],
                        'Apellidos': form.cleaned_data['EstudianteApellidos'],
                        'Rol': 'Estudiante',
                        'Celular': form.cleaned_data['EstudianteCelular'],
                        'Email': form.cleaned_data['EstudianteEmail'],
                    }

                    contrasena_estudiante = generar_contrasena_segura(12) 

                    estudiante_usuario, created_eu = Usuario.objects.get_or_create(
                        NumId=estudiante_usuario_data['NumId'],
                        defaults=estudiante_usuario_data
                    )

                    if created_eu:
                        # Estudiante nuevo: asignar contraseña y enviar correo
                        estudiante_usuario.set_password(contrasena_estudiante)
                        estudiante_usuario.save()
                        try:
                            asunto = 'Bienvenido a AulaTec — Tus credenciales'
                            mensaje = (
                                f'Hola {estudiante_usuario.Nombres},\n\n'
                                f'Se ha creado tu cuenta en la plataforma AulaTec.\n\n'
                                f'Usuario (documento): {estudiante_usuario.NumId}\n'
                                f'Contraseña inicial: {contrasena_estudiante}\n\n'
                                f'Por seguridad, cambia tu contraseña al ingresar por primera vez.\n\n'
                                f'Institución Educativa AulaTec'
                            )
                            send_mail(
                                asunto,
                                mensaje,
                                settings.EMAIL_HOST_USER,
                                [estudiante_usuario.Email],
                                fail_silently=False,
                            )
                        except Exception as e:
                            messages.warning(
                                request,
                                f'Matrícula creada correctamente, pero no se pudo enviar el correo '
                                f'a {estudiante_usuario.Email}. Entrega las credenciales manualmente.'
                            )
                    else:
                        # Estudiante existente (rematrícula): actualizar datos si cambiaron
                        campos_a_actualizar = ['Nombres', 'Apellidos', 'Email', 'Celular', 'TipoId']
                        cambio = False
                        for campo in campos_a_actualizar:
                            valor_nuevo = estudiante_usuario_data.get(campo)
                            if valor_nuevo and getattr(estudiante_usuario, campo) != valor_nuevo:
                                setattr(estudiante_usuario, campo, valor_nuevo)
                                cambio = True
                        if cambio:
                            estudiante_usuario.save()
                    # --- 2. Crear/Obtener el objeto Estudiante
                    estudiante, created_e = Estudiante.objects.get_or_create(
                        IdUsuario=estudiante_usuario,
                        defaults={}
                    )

                    # --- 3. Crear o encontrar el Acudiente
                    acudiente_data = {
                        'TipoId': form.cleaned_data['AcudienteTipoId'],
                        'NumId': form.cleaned_data['AcudienteNumId'],
                        'Nombres': form.cleaned_data['AcudienteNombres'],
                        'Apellidos': form.cleaned_data['AcudienteApellidos'],
                        'Celular': form.cleaned_data['AcudienteCelular'],
                        'Parentesco': form.cleaned_data['AcudienteParentesco'],
                    }
                    
                    # Usa get_or_create para evitar duplicar acudientes
                    acudiente, created_a = Acudiente.objects.get_or_create(
                        NumId=acudiente_data['NumId'],
                        defaults=acudiente_data
                    )

                    # Si el acudiente ya existía, actualiza sus datos por si cambiaron
                    if not created_a:
                        # Usar setattr para actualizar dinámicamente
                        for key, value in acudiente_data.items():
                            setattr(acudiente, key, value)
                        acudiente.save()

                    # --- 4. Crear la Matrícula y asignar el Acudiente
                    num_matricula = f"MAT-{form.cleaned_data['AnioLectivo']}-{random.randint(10000, 99999)}"
                    while Matricula.objects.filter(NumMatricula=num_matricula).exists():
                        num_matricula = f"MAT-{form.cleaned_data['AnioLectivo']}-{random.randint(10000, 99999)}"

                    matricula = form.save(commit=False)
                    matricula.NumMatricula = num_matricula
                    matricula.IdEstudiante = estudiante
                    matricula.IdAcudiente = acudiente # Asignación del objeto Acudiente
                    matricula.save()

                    estudiante.IdGrado = matricula.IdGrado
                    estudiante.save()

                    messages.success(request, f'Matrícula {matricula.NumMatricula} creada con éxito para {estudiante.IdUsuario.Nombres}.')
                    messages.info(request, f'Contraseña inicial estudiante (C.I.: {estudiante.IdUsuario.NumId}): {contrasena_estudiante}.')
                    
                    return redirect(reverse_lazy('gestion_aulatec:matricula_list'))
            
            except IntegrityError as e:
                # Maneja errores de integridad (ej. número de documento duplicado)
                messages.error(request, f'Error al guardar la matrícula: {e}. Es posible que un estudiante o acudiente con este número de identificación ya exista.')
                return render(request, self.template_name, self._ctx(form))

            except Exception as e:
                # Maneja cualquier otro error inesperado
                messages.error(request, f'Ocurrió un error inesperado al guardar la matrícula: {e}')
                return render(request, self.template_name, self._ctx(form))
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
            return render(request, self.template_name, self._ctx(form))
        
# Listar Matriculas.
# Esta parte también tiene un pequeño ajuste, aunque no es la causa del error actual
class MatriculaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Matricula
    template_name = 'gestion_aulatec/matricula_list.html'
    context_object_name = 'matriculas'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        return redirect('gestion_aulatec:home')

#detalles de matricula
class MatriculaDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Matricula
    template_name = 'gestion_aulatec/matricula_detail.html'
    context_object_name = 'matriculas'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'
    
    def handle_no_permission(self):
        return redirect('gestion_aulatec:home')

#editar matricula
class MatriculaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Matricula
    template_name = 'gestion_aulatec/matricula_form.html'
    context_object_name = 'matriculas'
    form_class = MatriculaForm
    success_url = reverse_lazy('gestion_aulatec:matricula_list')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        return redirect('gestion_aulatec:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['municipios'] = MUNICIPIOS_COLOMBIA
        context['eps_lista'] = EPS_COLOMBIA
        return context

#eliminar matricula
class MatriculaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Matricula
    template_name = 'gestion_aulatec/matricula_confirm_delete.html'
    success_url = reverse_lazy('gestion_aulatec:matricula_list')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'
    
    def handle_no_permission(self):
        return redirect('gestion_aulatec:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'La matrícula "{self.object.NumMatricula}" ha sido eliminada exitosamente.')
        return response
    
@login_required
@require_POST
def toggle_matricula_activa (request, pk):
    if not request.user.Rol == 'Administrador':
        return redirect('gestion_aulatec:home')

    matricula = get_object_or_404(Matricula, pk=pk)
        
    # 1. Toglea el valor de Activa (True -> False, False -> True)
    matricula.Activa = not matricula.Activa
    matricula.save()
        
    # 2. Prepara el mensaje de éxito
    status = "activa" if matricula.Activa else "inactiva"
    messages.success(request, f"Matrícula {matricula.NumMatricula} marcada como {status} correctamente.")
            
    # 3. Redirige de vuelta a la lista
    return redirect('gestion_aulatec:matricula_list')


class ExportarMatriculasExcelView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Descarga un Excel con las matrículas activas, filtrable por año lectivo."""

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        return redirect('gestion_aulatec:home')

    def get(self, request):
        try:
            import openpyxl
            from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
            from openpyxl.utils import get_column_letter
        except ImportError:
            from django.http import HttpResponse
            return HttpResponse('openpyxl no está instalado. Ejecuta: pip install openpyxl', status=500)

        from datetime import date
        from django.http import HttpResponse

        anio_actual = date.today().year
        anio = request.GET.get('anio', anio_actual)

        try:
            anio = int(anio)
        except (ValueError, TypeError):
            anio = anio_actual

        matriculas = Matricula.objects.filter(
            Activa=True,
            AnioLectivo=anio,
        ).select_related(
            'IdEstudiante__IdUsuario',
            'IdEstudiante__IdGrado',
            'IdAcudiente',
        ).order_by('IdEstudiante__IdUsuario__Apellidos', 'IdEstudiante__IdUsuario__Nombres')

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f'Matrículas {anio}'

        # ── Estilos ──
        color_header = '3B1F6E'
        color_subheader = '6D4FA0'
        color_alt = 'F3F0FA'

        header_font    = Font(bold=True, color='FFFFFF', size=11)
        subheader_font = Font(bold=True, color='FFFFFF', size=10)
        title_font     = Font(bold=True, size=14, color='3B1F6E')
        center         = Alignment(horizontal='center', vertical='center', wrap_text=True)
        left           = Alignment(horizontal='left',   vertical='center', wrap_text=True)

        thin = Side(style='thin', color='CCCCCC')
        border = Border(left=thin, right=thin, top=thin, bottom=thin)

        def fill(hex_color):
            return PatternFill(fill_type='solid', fgColor=hex_color)

        def si_no(val):
            return '✓' if val else '✗'

        # ── Fila 1: Título ──
        ws.merge_cells('A1:V1')
        ws['A1'] = f'REPORTE DE MATRÍCULAS ACTIVAS — AÑO LECTIVO {anio}'
        ws['A1'].font = title_font
        ws['A1'].alignment = center
        ws.row_dimensions[1].height = 30

        # ── Fila 2: Fecha de generación ──
        ws.merge_cells('A2:V2')
        ws['A2'] = f'Generado el {date.today().strftime("%d/%m/%Y")} por {request.user.Nombres} {request.user.Apellidos}'
        ws['A2'].font = Font(italic=True, size=9, color='888888')
        ws['A2'].alignment = center
        ws.row_dimensions[2].height = 18

        # ── Fila 3: Encabezados de grupo ──
        grupos = [
            ('A3', 'D3', 'DATOS DEL ESTUDIANTE'),
            ('E3', 'G3', 'INFORMACIÓN ACADÉMICA'),
            ('H3', 'K3', 'DATOS DE SALUD'),
            ('L3', 'N3', 'INSTITUCIÓN ANTERIOR'),
            ('O3', 'P3', 'CONDICIONES'),
            ('Q3', 'V3', 'DOCUMENTOS PRESENTADOS'),
        ]
        for inicio, fin, texto in grupos:
            ws.merge_cells(f'{inicio}:{fin}')
            celda = ws[inicio]
            celda.value = texto
            celda.font = subheader_font
            celda.fill = fill(color_subheader)
            celda.alignment = center
            celda.border = border
        ws.row_dimensions[3].height = 22

        # ── Fila 4: Columnas individuales ──
        columnas = [
            'N° Matrícula', 'Apellidos', 'Nombres', 'Documento',
            'Grado', 'Año Lectivo', 'Fecha Nacimiento',
            'Lugar Nacimiento', 'Barrio/Vereda', 'EPS/Seguro', 'Cond. Médica',
            'Colegio Anterior', 'Último Grado', 'Ciudad Inst. Anterior',
            'Repite Grado', 'Apoyo Pedagógico',
            'Doc. Identidad', 'Cert. Notas Ant.', 'Carnet Vacunas',
            'EPS Fotocopia', 'Fotos Doc.', 'Céd. Acudiente',
        ]
        for col_idx, nombre in enumerate(columnas, start=1):
            celda = ws.cell(row=4, column=col_idx, value=nombre)
            celda.font = header_font
            celda.fill = fill(color_header)
            celda.alignment = center
            celda.border = border
        ws.row_dimensions[4].height = 36

        # ── Filas de datos ──
        for row_idx, m in enumerate(matriculas, start=5):
            est = m.IdEstudiante
            usr = est.IdUsuario
            grado = f'{est.IdGrado.NumGrado}°{est.IdGrado.NumCurso}' if est.IdGrado else 'Sin asignar'

            fila = [
                m.NumMatricula,
                usr.Apellidos,
                usr.Nombres,
                usr.NumId,
                grado,
                m.AnioLectivo,
                m.FechaNacimientoEstudiante.strftime('%d/%m/%Y') if m.FechaNacimientoEstudiante else '',
                m.LugarNacimientoEstudiante,
                m.BarrioVeredaEstudiante,
                m.EPSSeguroMedicoEstudiante,
                m.EspecificacionCondicionMedica if m.TieneCondicionMedica else 'No',
                m.NombreColegio,
                m.UltimoGradoCursado,
                m.CiudadMunicipioInstitucionAnterior,
                si_no(m.RepiteGrado),
                si_no(m.RequiereApoyoPedagogico),
                si_no(m.DocIdentidadEstudiantePresentado),
                si_no(m.CertificadoNotasAnteriorPresentado),
                si_no(m.FotocopiaCarnetVacunacionPresentado),
                si_no(m.FotocopiaEpsSeguroMedicoPresentado),
                si_no(m.FotosTamanoDocumentoPresentadas),
                si_no(m.CopiaCedulaAcudientePresentado),
            ]

            bg = fill(color_alt) if row_idx % 2 == 0 else fill('FFFFFF')

            for col_idx, valor in enumerate(fila, start=1):
                celda = ws.cell(row=row_idx, column=col_idx, value=valor)
                celda.fill = bg
                celda.alignment = left if col_idx <= 4 else center
                celda.border = border

        # ── Fila de totales ──
        total_row = len(matriculas) + 5
        ws.merge_cells(f'A{total_row}:D{total_row}')
        ws[f'A{total_row}'] = f'TOTAL: {len(matriculas)} matrícula{"s" if len(matriculas) != 1 else ""} activa{"s" if len(matriculas) != 1 else ""}'
        ws[f'A{total_row}'].font = Font(bold=True, size=10, color='3B1F6E')
        ws[f'A{total_row}'].alignment = left

        # ── Anchos de columna ──
        anchos = [18, 20, 18, 14, 10, 10, 14, 18, 16, 18, 20, 22, 12, 20, 12, 14, 12, 14, 13, 12, 10, 14]
        for i, ancho in enumerate(anchos, start=1):
            ws.column_dimensions[get_column_letter(i)].width = ancho

        # ── Congelar paneles (encabezados siempre visibles) ──
        ws.freeze_panes = 'A5'

        # ── Respuesta HTTP ──
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="matriculas_activas_{anio}.xlsx"'
        wb.save(response)
        return response