from django.db import models

class Matricula(models.Model):
    NumMatricula = models.CharField(max_length=100, unique=True, verbose_name="Número de Matrícula")
    IdEstudiante = models.ForeignKey('Estudiante', on_delete=models.CASCADE, verbose_name="Estudiante")
    IdGrado = models.ForeignKey('Grado', on_delete=models.CASCADE, verbose_name="Grado a Matricular")
    AnioLectivo = models.IntegerField(verbose_name="Año Lectivo")
    NombreColegio = models.CharField(max_length=200, verbose_name="Nombre del Colegio de Procedencia")
    FechaNacimientoEstudiante = models.DateField(verbose_name="Fecha de Nacimiento del Estudiante")
    LugarNacimientoEstudiante = models.CharField(max_length=100, verbose_name="Lugar de Nacimiento del Estudiante")
    BarrioVeredaEstudiante = models.CharField(max_length=100, verbose_name="Barrio/Vereda del Estudiante")
    EPSSeguroMedicoEstudiante = models.CharField(max_length=100, verbose_name="EPS o Seguro Médico del Estudiante")
    TieneCondicionMedica = models.BooleanField(default=False, verbose_name="¿Tiene alguna condición médica?")
    EspecificacionCondicionMedica = models.TextField(blank=True, null=True, verbose_name="Especificar condición médica (si aplica)")

    UltimoGradoCursado = models.CharField(max_length=50, verbose_name="Último Grado Cursado")
    InstitucionAnterior = models.CharField(max_length=200, verbose_name="Institución Educativa Anterior")
    CiudadMunicipioInstitucionAnterior = models.CharField(max_length=100, verbose_name="Ciudad/Municipio de la Institución Anterior")
    RepiteGrado = models.BooleanField(default=False, verbose_name="¿Repite Grado?")
    RequiereApoyoPedagogico = models.BooleanField(default=False, verbose_name="¿Requiere Apoyo Pedagógico?")
    AutorizaTratamientoDatos = models.BooleanField(default=False, verbose_name="Autoriza Tratamiento de Datos")

    #campo relacionado con acudiente
    IdAcudiente = models.ForeignKey('Acudiente', on_delete=models.CASCADE)

    Activa = models.BooleanField(default=True, verbose_name="Matricula Activa")

    DocIdentidadEstudiantePresentado = models.BooleanField(default=False, verbose_name="Documento de Identidad Estudiante Presentado")
    CertificadoNotasAnteriorPresentado = models.BooleanField(default=False, verbose_name="Certificado de Notas Anterior Presentado")
    FotocopiaCarnetVacunacionPresentado = models.BooleanField(default=False, verbose_name="Fotocopia Carnet de Vacunación Presentado")
    FotocopiaEpsSeguroMedicoPresentado = models.BooleanField(default=False, verbose_name="Fotocopia EPS/Seguro Médico Presentado")
    FotosTamanoDocumentoPresentadas = models.BooleanField(default=False, verbose_name="Fotos Tamaño Documento Presentadas")
    CertificadoMedicoPresentado = models.BooleanField(default=False, verbose_name="Certificado Médico Presentado")
    CopiaCedulaAcudientePresentado = models.BooleanField(default=False, verbose_name="Copia Cédula Acudiente Presentado")
    ComprobanteResidenciaAcudientePresentado = models.BooleanField(default=False, verbose_name="Comprobante de Residencia Acudiente Presentado")

    FechaMatricula = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Matrícula")

    class Meta:
        db_table = 'Matricula'
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'

    def __str__(self):
        return f"Matrícula {self.NumMatricula} - {self.IdEstudiante.IdUsuario.Nombres} {self.IdEstudiante.IdUsuario.Apellidos}"
