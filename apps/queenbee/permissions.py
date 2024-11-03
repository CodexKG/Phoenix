from functools import wraps
from django.shortcuts import render
from django.db import ProgrammingError, OperationalError
from django.apps import apps

from apps.erp.models import Permission

def check_admin_director(user):
    employee = getattr(user, 'user_employee', None)
    return employee and employee.employee_position in ['Администратор', 'Директор']

def permission_required(codename, name=None):
    def decorator(view_func):
        permission_name = name or view_func.__name__

        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if apps.get_app_config('crm').models_module is None:
                return view_func(request, *args, **kwargs)

            try:
                permission, created = Permission.objects.get_or_create(codename=codename, defaults={'name': permission_name})
            except (ProgrammingError, OperationalError):
                return view_func(request, *args, **kwargs)

            if not request.user.is_authenticated:
                return render(request, 'queenbee/no_access.html', status=403)

            employee = getattr(request.user, 'user_employee', None)
            if employee:
                user_permissions = employee.user_permissions.all()
                group_permissions = Permission.objects.filter(grouppermission__employee=employee)
                all_permissions = user_permissions | group_permissions
                
                if all_permissions.filter(codename=codename).exists():
                    return view_func(request, *args, **kwargs)
            
            return render(request, 'queenbee/no_access.html', status=403)
        _wrapped_view.permission_codename = codename
        _wrapped_view.permission_name = permission_name
        return _wrapped_view
    return decorator

def register_permissions():
    """Функция для регистрации всех разрешений, использующих @permission_required."""
    # Импортируем все views, чтобы декораторы были загружены
    from django.urls import get_resolver

    # Получаем все URL, чтобы получить доступ к view-функциям
    urlconf = get_resolver().url_patterns
    views = []

    def gather_views(patterns):
        for pattern in patterns:
            if hasattr(pattern, 'url_patterns'):
                gather_views(pattern.url_patterns)
            else:
                callback = pattern.callback
                if hasattr(callback, 'permission_codename'):
                    views.append(callback)

    gather_views(urlconf)

    # Добавляем недостающие разрешения
    for view in views:
        codename = view.permission_codename
        name = view.permission_name
        Permission.objects.get_or_create(codename=codename, defaults={'name': name})

def check_and_add_permission(employee, codename):
    permission = Permission.objects.filter(codename=codename).first()
    if not permission:
        permission = Permission.objects.create(codename=codename, name=codename)
    
    user_permissions = employee.user_permissions.all()
    group_permissions = Permission.objects.filter(grouppermission__employee=employee)
    all_permissions = user_permissions | group_permissions

    if not all_permissions.filter(codename=codename).exists():
        employee.user_permissions.add(permission)