from functools import wraps
from django.shortcuts import render
from django.db import ProgrammingError, OperationalError
from django.apps import apps

from apps.erp.models import Permission

def check_admin_director(user):
    # Проверяем, есть ли у пользователя связанный объект Employee
    employee = getattr(user, 'user_employee', None)
    # Если есть, проверяем его должность
    return employee and employee.employee_position in ['Администратор', 'Директор']

def permission_required(codename, name=None):
    def decorator(view_func):
        permission_name = name or view_func.__name__

        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Проверка на выполнение миграций
            if apps.get_app_config('crm').models_module is None:
                # Пропустить проверку разрешений, если выполняются миграции
                return view_func(request, *args, **kwargs)
            
            try:
                # Регистрируем разрешение
                permission, created = Permission.objects.get_or_create(codename=codename, defaults={'name': permission_name})
            except (ProgrammingError, OperationalError):
                # Если таблицы не существует, пропускаем проверку разрешений
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
        return _wrapped_view
    return decorator

def check_and_add_permission(employee, codename):
    permission = Permission.objects.filter(codename=codename).first()
    if not permission:
        permission = Permission.objects.create(codename=codename, name=codename)
    
    user_permissions = employee.user_permissions.all()
    group_permissions = Permission.objects.filter(grouppermission__employee=employee)
    all_permissions = user_permissions | group_permissions

    if not all_permissions.filter(codename=codename).exists():
        employee.user_permissions.add(permission)