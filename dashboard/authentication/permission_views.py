from functools import wraps
from django.http import HttpResponse
def check_user_permission(request,username):
    if request.user.category == 'admin':
        return 'admin'
    elif request.user.category == 'hr':
        return 'hr'
    elif request.user.category == 'manager':
        return 'manager'
    else:
        return None
def admin_perm(request, username):
    permissions = check_user_permission(request, username)
    return permissions == 'admin'

def manager_perm(request, username):
    permissions = check_user_permission(request, username)
    return permissions == 'manager'

def hr_perm(request, username):
    permissions = check_user_permission(request, username)
    return permissions == 'hr'
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if admin_perm(request,request.user.username):
            # User has admin permissions, execute the view function
            return view_func(request, *args, **kwargs)
        else:
            # User does not have admin permissions, return an error response
            return HttpResponse("You do not have permission to access this page")
    return _wrapped_view

def manager_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if manager_perm(request,request.user.username):
            # User has manager permissions, execute the view function
            return view_func(request, *args, **kwargs)
        else:
            # User does not have manager permissions, return an error response
            return HttpResponse("You do not have permission to access this page")
    return _wrapped_view

def hr_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if hr_perm(request,request.user.username):
            # User has HR permissions, execute the view function
            return view_func(request, *args, **kwargs)
        else:
            # User does not have HR permissions, return an error response
            return HttpResponse("You do not have permission to access this page")
    return _wrapped_view

def admin_or_manager_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if admin_perm(request,request.user.username) or manager_perm(request.user.username):
            # User has either admin or manager permissions, execute the view function
            return view_func(request, *args, **kwargs)
        else:
            # User does not have admin or manager permissions, return an error response
            return HttpResponse("You do not have permission to access this page")
    return _wrapped_view

def admin_or_hr_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if admin_perm(request,request.user.username) or hr_perm(request.user.username):
            # User has either admin or HR permissions, execute the view function
            return view_func(request, *args, **kwargs)
        else:
            # User does not have admin or HR permissions, return an error response
            return HttpResponse("You do not have permission to access this page")
    return _wrapped_view

def admin_hr_or_manager_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if admin_perm(request,request.user.username) or hr_perm(request.user.username) or manager_perm(request.user.username):
            # User has either admin, HR, or manager permissions, execute the view function
            return view_func(request, *args, **kwargs)
        else:
            # User does not have admin, HR, or manager permissions, return an error response
            return HttpResponse("You do not have permission to access this page")
    return _wrapped_view
