from functools import wraps
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def rol_required(allowed_roles):
    """
    allowed_roles: string o lista/tuple de strings ('productor', 'empresa', 'admin')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(f'/accounts/login/?next={request.path}')
            perfil = getattr(request.user, 'perfil', None)
            if perfil is None:
                raise PermissionDenied
            allowed = allowed_roles
            if isinstance(allowed, (list, tuple)):
                if perfil.rol not in allowed:
                    raise PermissionDenied
            else:
                if perfil.rol != allowed:
                    raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
