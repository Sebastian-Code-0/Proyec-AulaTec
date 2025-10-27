from django.db import models

class ChecklistDocumentos(models.Model):
    IdChecklist = models.AutoField(primary_key=True)
    
    # Relación 1 a 1: Cada matrícula tiene un único checklist
    IdMatricula = models.OneToOneField('Matricula', on_delete=models.CASCADE, verbose_name="Matrícula Asociada")
    
    # --- CAMPOS DE DOCUMENTOS MOVIDOS ---
    DocIdentidadEstudiantePresentado = models.BooleanField(default=False, verbose_name="Documento de Identidad Estudiante Presentado")
    CertificadoNotasAnteriorPresentado = models.BooleanField(default=False, verbose_name="Certificado de Notas Anterior Presentado")
    FotocopiaCarnetVacunacionPresentado = models.BooleanField(default=False, verbose_name="Fotocopia Carnet de Vacunación Presentado")
    FotocopiaEpsSeguroMedicoPresentado = models.BooleanField(default=False, verbose_name="Fotocopia EPS/Seguro Médico Presentado")
    FotosTamanoDocumentoPresentadas = models.BooleanField(default=False, verbose_name="Fotos Tamaño Documento Presentadas")
    CertificadoMedicoPresentado = models.BooleanField(default=False, verbose_name="Certificado Médico Presentado")
    CopiaCedulaAcudientePresentado = models.BooleanField(default=False, verbose_name="Copia Cédula Acudiente Presentado")
    ComprobanteResidenciaAcudientePresentado = models.BooleanField(default=False, verbose_name="Comprobante de Residencia Acudiente Presentado")
    # -----------------------------------------
    
    def __str__(self):
        return f"Checklist para Matrícula {self.IdMatricula.NumMatricula}"

    class Meta:
        db_table = 'ChecklistDocumentos'
        verbose_name = 'Checklist Documentos'
        verbose_name_plural = 'Checklist Documentos'