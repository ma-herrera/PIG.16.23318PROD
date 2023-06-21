from django.shortcuts import redirect



class LoginYSuperUsuarioMixin(object):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                 return super().dispatch(request, *args, **kwargs)
        return redirect('home')


def has_permission(function):
    def wrap(request, *args, **kwargs):
        # agregar tu lógica de verificación de permisos
        # Por ejemplo, si solo los usuarios autenticados pueden acceder:
        if request.user.is_authenticated:
            if request.user.is_staff:
                 return function(request, *args, **kwargs)
            else:
                return redirect('home')
        else:
           return redirect('home')
    return wrap

class LoginMixin(object):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect('home')