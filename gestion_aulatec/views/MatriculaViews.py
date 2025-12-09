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

from gestion_aulatec.forms import MatriculaForm
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
        messages.error(self.request, 'No tienes permiso para realizar matrículas.')
        return redirect('gestion_aulatec:home')

    # Método GET: Muestra el formulario vacío
    def get(self, request, *args, **kwargs):
        form = MatriculaForm()
        return render(request, self.template_name, {'form': form})

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
                    }

                    contrasena_estudiante = generar_contrasena_segura(12) 

                    estudiante_usuario, created_eu = Usuario.objects.get_or_create(
                        NumId=estudiante_usuario_data['NumId'],
                        defaults=estudiante_usuario_data
                    )
                    
                    if created_eu:
                        estudiante_usuario.set_password(contrasena_estudiante)
                        estudiante_usuario.save()
                    # Nota: si el usuario ya existe, no se actualiza la contraseña ni se guarda aquí.
                    # Se asume que el usuario ya tiene una contraseña y sus datos ya están correctos.

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
                return render(request, self.template_name, {'form': form})
            
            except Exception as e:
                # Maneja cualquier otro error inesperado
                messages.error(request, f'Ocurrió un error inesperado al guardar la matrícula: {e}')
                return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
            return render(request, self.template_name, {'form': form})
        
# Listar Matriculas.
# Esta parte también tiene un pequeño ajuste, aunque no es la causa del error actual
class MatriculaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Matricula
    template_name = 'gestion_aulatec/matricula_list.html'
    context_object_name = 'matriculas'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para ver las matrículas.')
        return redirect('gestion_aulatec:home')

#detalles de matricula
class MatriculaDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Matricula
    template_name = 'gestion_aulatec/matricula_detail.html'
    context_object_name = 'matriculas'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para ver las matrículas.')
        return redirect('gestion_aulatec:home')
    
#editar matricula
class MatriculaUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Matricula
    template_name = 'gestion_aulatec/matricula_form.html'
    context_object_name = 'matriculas'
    form_class = MatriculaForm

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para ver las matrículas.')
        return redirect('gestion_aulatec:home')
    
#eliminar matricula
class MatriculaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Matricula
    template_name = 'gestion_aulatec/matricula_confirm_delete.html'
    success_url = reverse_lazy('gestion_aulatec:matricula_list')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para ver las matrículas.')
        return redirect('gestion_aulatec:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'La matrícula "{self.object.NumMatricula}" ha sido eliminada exitosamente.')
        return response
    
@login_required
@require_POST
def toggle_matricula_activa (request, pk):
    if not request.user.Rol == 'Administrador':
        messages.error(request, 'No tienes permiso para cambiar el estado de la matrícula.')
        return redirect('gestion_aulatec:matricula_list')

    matricula = get_object_or_404(Matricula, pk=pk)
        
    # 1. Toglea el valor de Activa (True -> False, False -> True)
    matricula.Activa = not matricula.Activa
    matricula.save()
        
    # 2. Prepara el mensaje de éxito
    status = "activa" if matricula.Activa else "inactiva"
    messages.success(request, f"Matrícula {matricula.NumMatricula} marcada como {status} correctamente.")
            
    # 3. Redirige de vuelta a la lista
    return redirect('gestion_aulatec:matricula_list')