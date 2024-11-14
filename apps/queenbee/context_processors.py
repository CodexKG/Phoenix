from apps.queenbee.permissions import check_admin_director
from apps.settings.models import Setting
from apps.erp.models import City, Permission

def personnel_panel_access(request):
    if not request.user.is_authenticated:
        return {'can_view_personnel': False}
    return {'can_view_personnel': check_admin_director(request.user)}

def access_rights(request):
    if not request.user.is_authenticated:
        return {}

    employee = getattr(request.user, 'user_employee', None)
    if employee:
        user_permissions = employee.user_permissions.all()
        group_permissions = Permission.objects.filter(grouppermission__employee=employee)
        all_permissions = user_permissions | group_permissions

        permissions = {perm.codename: True for perm in all_permissions}
        return {'permissions': permissions}

    return {}

def settings_context(request):
    try:
        setting = Setting.objects.latest('id')
    except Setting.DoesNotExist:
        setting = None
    return {'setting': setting}

def cities_context(request):
    cities = City.objects.all()
    selected_city_id = request.session.get('selected_city')
    selected_city = None
    if selected_city_id:
        selected_city = City.objects.get(id=selected_city_id)
    return {
        'cities': cities,
        'selected_city': selected_city
    }

def city_access_rights(request):
    if not request.user.is_authenticated:
        return {}

    employee = getattr(request.user, 'user_employee', None)
    if employee:
        return {
            'can_change_city': employee.employee_position in ['Администратор', 'Директор']
        }
    return {
        'can_change_city': False
    }

def selected_city(request):
    selected_city_id = request.session.get('selected_city')
    if selected_city_id:
        try:
            city = City.objects.get(id=selected_city_id)
        except City.DoesNotExist:
            city = None
    else:
        city = None
    
    return {
        'selected_city': city
    }