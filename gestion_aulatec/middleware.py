from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # 1. Si es admin, lo dejamos pasar de una vez
            if request.user.is_staff or request.user.is_superuser:
                return self.get_response(request)

            # 2. Definimos las rutas (Asegúrate de que estos nombres existan)
            path_cambio = reverse('gestion_aulatec:cambiar_password')
            path_logout = reverse('gestion_aulatec:logout')

            # 3. Verificamos si debe cambiar la contraseña
            if request.user.debe_cambiar_password:
                # Si no está en la página de cambio ni intentando salir, lo mandamos a cambiar clave
                if request.path != path_cambio and request.path != path_logout:
                    return redirect(path_cambio)

        return self.get_response(request)