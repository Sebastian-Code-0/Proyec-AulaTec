from django.urls import path
from gestion_aulatec.views.CertificadoViews import (
    AdminSolicitudesView,
    DetalleCertificadoAdminView,
    AprobarCertificadoView,
    RechazarCertificadoView,
    DescargarCertificadoPDFView,
    SolicitarCertificadoView,
    MisCertificadosView,
    DescargarCertificadoEstudianteView,
    DescargarReporteNotasView,
)

urlpatterns = [
    # Admin
    path('',                              AdminSolicitudesView.as_view(),          name='admin_solicitudes'),
    path('<int:pk>/',                     DetalleCertificadoAdminView.as_view(),   name='detalle_certificado_admin'),
    path('<int:pk>/aprobar/',             AprobarCertificadoView.as_view(),        name='aprobar_certificado'),
    path('<int:pk>/rechazar/',            RechazarCertificadoView.as_view(),       name='rechazar_certificado'),
    path('<int:pk>/descargar/',           DescargarCertificadoPDFView.as_view(),   name='descargar_certificado_admin'),
    # Estudiante
    path('solicitar/',                    SolicitarCertificadoView.as_view(),      name='solicitar_certificado'),
    path('mis-certificados/',             MisCertificadosView.as_view(),           name='mis_certificados'),
    path('mis-certificados/<int:pk>/pdf/', DescargarCertificadoEstudianteView.as_view(), name='descargar_certificado_est'),
    path('reporte-notas/', DescargarReporteNotasView.as_view(), name='descargar_reporte_notas'),
]
