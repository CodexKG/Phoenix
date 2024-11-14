from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.admin.utils import label_for_field
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import admin
import traceback

from apps.erp.models import GroupPermission
from apps.erp.forms import GroupPermissionForm
from apps.queenbee.permissions import permission_required
# from apps.crm.tasks import log_change

User = get_user_model()

@login_required(login_url='/admin/login/')
@permission_required('crm_group_index', 'Просмотр раздела Группы разрешений')
def crm_group_index(request):
    return render(request, 'queenbee/group/index.html')

@staff_member_required(login_url='/admin/login/')
@permission_required('crm_group_detail', 'Добавление или детальный просмотр раздела Группы разрешений')
def crm_group_detail(request, id=None):
    group = get_object_or_404(GroupPermission, id=id) if id else None

    if request.method == "POST":
        form = GroupPermissionForm(request.POST, request.FILES, instance=group)
        if "update" in request.POST and form.is_valid():
            form.save()
            return redirect('crm_group_detail', id=group.id)
        elif "delete" in request.POST:
            group.delete()
            return redirect('crm_group_index')
        else:
            if form.is_valid():
                form.save()
                return redirect('crm_group_index')
    else:
        form = GroupPermissionForm(instance=group)

    context = {
        'form': form,
        'group': group
    }
    return render(request, 'queenbee/group/detail.html', context)

@staff_member_required(login_url='/admin/login/')
def get_group_data(request):
    fields = request.GET.get('fields')
    list_display = fields.split(',') if fields else ['id', 'name', 'created']
    try:
        groups = GroupPermission.objects.all().values_list(*list_display, named=True)
        model_admin = admin.site._registry[GroupPermission]
        field_names = {
            field: label_for_field(field, GroupPermission, model_admin)
            for field in list_display
        }

        return JsonResponse({
            'groups': [group._asdict() for group in groups],
            'field_names': field_names,
        })

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)