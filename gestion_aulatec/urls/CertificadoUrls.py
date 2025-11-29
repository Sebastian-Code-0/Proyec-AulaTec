from django.urls import path
from gestion_aulatec.views.CertificadoViews import test_view
from gestion_aulatec.views.CertificadoViews import (
    certificado_list,
    certificado_create,
    certificado_detail,
    certificado_delete,
    certificado_pdf,
    certificado_preview,
    descargar_mi_certificado,
    test_view
)
from gestion_aulatec.views.CertificadoViews import certificado_preview

urlpatterns = [
    path('test/', test_view, name='certificado_test'),
    path('', certificado_list, name='certificado_list'),
    path('nuevo/', certificado_create, name='certificado_create'),
    path('<int:pk>/', certificado_detail, name='certificado_detail'),
    path('<int:pk>/eliminar/', certificado_delete, name='certificado_delete'),
    path('<int:pk>/pdf/', certificado_pdf, name='certificado_pdf'),
    path('preview/<int:id>/', certificado_preview, name='certificado_preview'),
    path('mi-certificado/<int:pk>/descargar/', descargar_mi_certificado, name='descargar_mi_certificado'),
]
