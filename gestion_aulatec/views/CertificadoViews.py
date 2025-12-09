# Archivo: gestion_aulatec/views/CertificadoViews.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from gestion_aulatec.models.certificado import Certificado
from gestion_aulatec.models.estudiante import Estudiante
from gestion_aulatec.models.usuario import Usuario
from datetime import datetime
import os
from django.conf import settings


# ==================== VISTAS PARA ESTUDIANTES ====================

@login_required
def solicitar_certificado(request):
    """Vista para que el estudiante solicite un certificado"""
    # Verificar que el usuario tenga rol de Estudiante
    if request.user.Rol != 'Estudiante':
        messages.error(request, 'Solo los estudiantes pueden solicitar certificados.')
        return redirect('gestion_aulatec:home')
    
    try:
        # Obtener el estudiante asociado al usuario logueado
        estudiante = Estudiante.objects.get(IdUsuario=request.user)
    except Estudiante.DoesNotExist:
        messages.error(request, 'No tienes un perfil de estudiante asociado.')
        return redirect('gestion_aulatec:estudiante_dashboard')
    
    if request.method == 'POST':
        tipo_certificado = request.POST.get('tipo', 'estudio')
        observaciones = request.POST.get('observaciones', '')
        
        # Crear la solicitud de certificado
        certificado = Certificado.objects.create(
            IdEstudiante=estudiante,
            tipo=tipo_certificado,
            observaciones=observaciones,
            estado='pendiente'
        )
        
        messages.success(request, f'Solicitud de certificado creada exitosamente. Código: {certificado.codigo}')
        return redirect('gestion_aulatec:mis_certificados')
    
    # Verificar si tiene solicitudes pendientes
    solicitudes_pendientes = Certificado.objects.filter(
        IdEstudiante=estudiante,
        estado='pendiente'
    ).count()
    
    context = {
        'estudiante': estudiante,
        'solicitudes_pendientes': solicitudes_pendientes,
    }
    return render(request, 'certificados/solicitar_certificado.html', context)


@login_required
def mis_certificados(request):
    """Vista para que el estudiante vea sus certificados"""
    # Verificar que el usuario tenga rol de Estudiante
    if request.user.Rol != 'Estudiante':
        messages.error(request, 'Solo los estudiantes pueden ver esta página.')
        return redirect('gestion_aulatec:home')
    
    try:
        estudiante = Estudiante.objects.get(IdUsuario=request.user)
    except Estudiante.DoesNotExist:
        messages.error(request, 'No tienes un perfil de estudiante asociado.')
        return redirect('gestion_aulatec:estudiante_dashboard')
    
    # Obtener todos los certificados del estudiante
    certificados = Certificado.objects.filter(IdEstudiante=estudiante).order_by('-fecha_solicitud')
    
    context = {
        'estudiante': estudiante,
        'certificados': certificados,
    }
    return render(request, 'certificados/mis_certificados.html', context)


@login_required
def descargar_certificado(request, certificado_id):
    """Vista para descargar el PDF del certificado aprobado"""
    # Verificar que el usuario tenga rol de Estudiante
    if request.user.Rol != 'Estudiante':
        messages.error(request, 'No tienes permiso para descargar este certificado.')
        return redirect('gestion_aulatec:home')
    
    try:
        estudiante = Estudiante.objects.get(IdUsuario=request.user)
        certificado = get_object_or_404(
            Certificado, 
            IdCertificado=certificado_id,
            IdEstudiante=estudiante
        )
    except Estudiante.DoesNotExist:
        messages.error(request, 'No tienes un perfil de estudiante asociado.')
        return redirect('gestion_aulatec:estudiante_dashboard')
    
    # Verificar que el certificado esté aprobado
    if certificado.estado != 'aprobado':
        messages.error(request, 'Este certificado aún no ha sido aprobado.')
        return redirect('gestion_aulatec:mis_certificados')
    
    # Verificar que exista el archivo PDF
    if not certificado.archivo_pdf:
        messages.error(request, 'El archivo PDF no está disponible.')
        return redirect('gestion_aulatec:mis_certificados')
    
    # Ruta completa del archivo
    ruta_archivo = os.path.join(settings.MEDIA_ROOT, certificado.archivo_pdf)
    
    if not os.path.exists(ruta_archivo):
        messages.error(request, 'El archivo no se encuentra en el servidor.')
        return redirect('gestion_aulatec:mis_certificados')
    
    # Retornar el archivo
    return FileResponse(
        open(ruta_archivo, 'rb'),
        content_type='application/pdf',
        as_attachment=True,
        filename=f'certificado_{certificado.codigo}.pdf'
    )


# ==================== VISTAS PARA ADMINISTRADORES ====================

@login_required
def listar_solicitudes_admin(request):
    """Vista para que el admin vea todas las solicitudes de certificados"""
    # Verificar que el usuario sea administrador
    if request.user.Rol != 'Administrador':
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('gestion_aulatec:home')
    
    # Filtrar certificados según el estado
    estado_filtro = request.GET.get('estado', 'pendiente')
    
    if estado_filtro == 'todos':
        certificados = Certificado.objects.all().order_by('-fecha_solicitud')
    else:
        certificados = Certificado.objects.filter(estado=estado_filtro).order_by('-fecha_solicitud')
    
    # Contar solicitudes por estado
    pendientes = Certificado.objects.filter(estado='pendiente').count()
    aprobados = Certificado.objects.filter(estado='aprobado').count()
    rechazados = Certificado.objects.filter(estado='rechazado').count()
    
    context = {
        'certificados': certificados,
        'estado_filtro': estado_filtro,
        'pendientes': pendientes,
        'aprobados': aprobados,
        'rechazados': rechazados,
    }
    return render(request, 'certificados/admin_solicitudes.html', context)


@login_required
def aprobar_certificado(request, certificado_id):
    """Vista para que el admin apruebe un certificado y genere el PDF"""
    # Verificar permisos
    if request.user.Rol != 'Administrador':
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('gestion_aulatec:home')
    
    certificado = get_object_or_404(Certificado, IdCertificado=certificado_id)
    
    if request.method == 'POST':
        # Actualizar estado del certificado
        certificado.estado = 'aprobado'
        certificado.fecha_aprobacion = datetime.now()
        certificado.aprobado_por = request.user
        certificado.save()
        
        # Generar el PDF
        try:
            from gestion_aulatec.views.certificado_pdf import generar_certificado_pdf
            ruta_pdf = generar_certificado_pdf(certificado)
            certificado.archivo_pdf = ruta_pdf
            certificado.save()
            
            messages.success(request, f'Certificado {certificado.codigo} aprobado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al generar el PDF: {str(e)}')
        
        return redirect('gestion_aulatec:admin_solicitudes')
    
    context = {
        'certificado': certificado,
    }
    return render(request, 'certificados/aprobar_certificado.html', context)


@login_required
def rechazar_certificado(request, certificado_id):
    """Vista para que el admin rechace un certificado"""
    # Verificar permisos
    if request.user.Rol != 'Administrador':
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('gestion_aulatec:home')
    
    certificado = get_object_or_404(Certificado, IdCertificado=certificado_id)
    
    if request.method == 'POST':
        motivo = request.POST.get('motivo_rechazo', '')
        
        certificado.estado = 'rechazado'
        certificado.motivo_rechazo = motivo
        certificado.save()
        
        messages.success(request, f'Certificado {certificado.codigo} rechazado.')
        return redirect('gestion_aulatec:admin_solicitudes')
    
    context = {
        'certificado': certificado,
    }
    return render(request, 'certificados/rechazar_certificado.html', context)


@login_required
def ver_detalle_certificado_admin(request, certificado_id):
    """Vista para que el admin vea el detalle completo de un certificado"""
    # Verificar permisos
    if request.user.Rol != 'Administrador':
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('gestion_aulatec:home')
    
    certificado = get_object_or_404(Certificado, IdCertificado=certificado_id)
    
    context = {
        'certificado': certificado,
    }
    return render(request, 'certificados/detalle_certificado_admin.html', context)