from functools import wraps
from django.http import HttpResponseForbidden


def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role == role:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Siz ushbu sahifaga kirish huquqiga ega emassiz.")
        return _wrapped_view
    return decorator
