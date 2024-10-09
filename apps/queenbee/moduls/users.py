from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.contrib.admin.utils import label_for_field
from django.shortcuts import get_object_or_404
from django.contrib import admin
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate
from django.urls import reverse
import traceback

from apps.hiveclient.models import User
from apps.erp.models import Employee, PhotosProfile, EmployeeExperience, EmployeeEducation
from apps.hiveclient.forms import UsersForm, CustomPasswordChangeForm, CRMEmployeeForm
# from apps.hiveclient.permissions import permission_required
# from apps.hiveclient.tasks import log_change

@staff_member_required(login_url='/admin/login')
# @permission_required('crm_index_users', 'Просмотр раздела Пользователи')
def crm_index_users(request):
    return render(request, 'crm/user/index.html', locals())

@staff_member_required(login_url='/admin/login/')
# @permission_required('crm_detail_users', 'Добавление или детальный просмотр раздела Пользователи')
def crm_detail_users(request, id=None):
    user = None  # Определяем переменную user

    if id:
        user = get_object_or_404(User, id=id)
        form = UsersForm(request.POST or None, request.FILES or None, instance=user)

        if request.method == "POST":
            if form.is_valid():
                user = form.save(commit=False)
                # Хешируем пароль, если он был изменен
                if form.cleaned_data['password']:
                    user.password = make_password(form.cleaned_data['password'])
                user.save()

                if "update" in request.POST:
                    # log_change.delay(
                    #     request.user.id, 
                    #     f"Обновлен пользователь #ID {user.id} {user.username} пользователем {request.user.username} {request.user.first_name} {request.user.last_name}"
                    # )
                    return redirect('crm_detail_user', id=user.id)
                elif "delete" in request.POST:
                    # log_change.delay(
                    #     request.user.id, 
                    #     f"Удален пользователь #ID {user.id} {user.username} пользователем {request.user.username} {request.user.first_name} {request.user.last_name}"
                    # )
                    user.delete()
                    return redirect('crm_index_user')
                else:
                    # log_change.delay(
                    #     request.user.id, 
                    #     f"Создан новый пользователь #ID {user.id} {user.username} пользователем {request.user.username} {request.user.first_name} {request.user.last_name}"
                    # )
                    return redirect('crm_index_user')
        else:
            form = UsersForm(instance=user)
    else:
        form = UsersForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()

            # log_change.delay(
            #     request.user.id, 
            #     f"Создан новый пользователь #ID {user.id} {user.username} пользователем {request.user.username} {request.user.first_name} {request.user.last_name}"
            # )
            return redirect('crm_index_user')

    return render(request, 'crm/user/detail.html', {'form': form, 'user': user})

@staff_member_required(login_url='/admin/login/')
def get_user_data(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    fields = request.GET.get('fields')
    list_display = fields.split(',') if fields else ['id', 'username', 'first_name', 'last_name', 'date_joined']  # Значения по умолчанию

    try:
        users = User.objects.all().values_list(*list_display, named=True).order_by('-date_joined', )

        model_admin = admin.site._registry[User]
        field_names = {
            field: label_for_field(field, User, model_admin)
            for field in list_display
        }

        return JsonResponse({
            'users': [user._asdict() for user in users],
            'field_names': field_names,
        })

    except Exception as e:
        print("Error", e)
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)
    
@staff_member_required(login_url='/admin/login/')
def crm_user_profile(request, id):
    user = User.objects.get(id=id)
    employee = Employee.objects.get(user=user)
    photos = PhotosProfile.objects.filter(user=employee)
    experiences = EmployeeExperience.objects.filter(user=employee)
    educations = EmployeeEducation.objects.filter(user=employee)
    return render(request, 'crm/user/profile.html', locals())

@staff_member_required(login_url='/admin/login/')
def crm_user_setting(request, id):
    user = User.objects.get(id=id)
    employee = get_object_or_404(Employee, user=user)
    if request.method == 'POST':
        form = CRMEmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('crm_user_setting', user.id)  # Redirect to a success page or the same page after saving
    else:
        form = CRMEmployeeForm(instance=employee)
    return render(request, 'crm/user/setting.html', {'form': form})

@staff_member_required(login_url='/admin/login/')
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Важно!
            messages.success(request, 'Ваш пароль был успешно изменен!')
            return redirect('profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'crm/user/change_password.html', {'form': form})

"""Страница авторизации пользователя"""
def crm_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Проверяем, есть ли у пользователя связанный объект Employee
            employee = getattr(user, 'user_employee', None)
            if employee and employee.city.exists():
                # Устанавливаем первый город сотрудника в сессию (если сотрудник связан с несколькими городами, вы можете выбрать логику, которая подходит вам)
                request.session['selected_city'] = employee.city.first().id
            
            return JsonResponse({'success': True, 'redirect_url': reverse('crm_index')})
        else:
            return JsonResponse({'success': False, 'error_message': 'Неверное имя пользователя или пароль'})
    return render(request, 'queenbee/hiveclient/login.html', locals())