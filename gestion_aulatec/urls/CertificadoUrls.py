# Archivo: gestion_aulatec/urls/CertificadoUrls.py

from django.urls import path
from gestion_aulatec.views import CertificadoViews



urlpatterns = [
    # URLs para estudiantes
    path('solicitar/', CertificadoViews.solicitar_certificado, name='solicitar_certificado'),
    path('mis-certificados/', CertificadoViews.mis_certificados, name='mis_certificados'),
    path('descargar/<int:certificado_id>/', CertificadoViews.descargar_certificado, name='descargar_certificado'),
    
    # URLs para administradores
    path('admin/solicitudes/', CertificadoViews.listar_solicitudes_admin, name='admin_solicitudes'),
    path('admin/aprobar/<int:certificado_id>/', CertificadoViews.aprobar_certificado, name='aprobar_certificado'),
    path('admin/rechazar/<int:certificado_id>/', CertificadoViews.rechazar_certificado, name='rechazar_certificado'),
    path('admin/detalle/<int:certificado_id>/', CertificadoViews.ver_detalle_certificado_admin, name='detalle_certificado_admin'),
]