from django.shortcuts import redirect
from  django.http import HttpResponse
from django.contrib.auth.models import Group
from django.views.decorators.csrf import ensure_csrf_cookie

def authenticatedUser(view_func):
    def wrapper_func( request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect ('home')
        else:
            return view_func( request, *args, **kwargs)
    return wrapper_func

def unauthenticatedUser(view_func):
    def wrapper_func( request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect ('login')
        else:
            return view_func( request, *args, **kwargs)
    return wrapper_func

def ensureCSRF(view_func):
    def wrapper_func( request, *args, **kwargs):

        ensure_csrf_cookie(view_func)
        return view_func( request, *args, **kwargs)
    return wrapper_func

# def admin_only(view_func):
#     def wrapper_func( request, *args, **kwargs):
#         group = None
#         if request.user.groups.exists():
#             group = Group.objects.all()[0].name
            
#         if group == 'admin':
#             return
#         else:
#             return view_func( request, *args, **kwargs)
#     return wrapper_func