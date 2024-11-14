from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.utils import label_for_field
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import admin
import traceback, logging, json

from apps.cms.models import Partners
from apps.cms.forms import PartnersForm
from apps.queenbee.permissions import permission_required

logger = logging.getLogger(__name__)

@staff_member_required(login_url='/admin/login')
@permission_required('crm_partner_index', 'Просмотр раздела Партнеры')
def crm_partner_index(request):
    return render(request, 'queenbee/partner/index.html')

@staff_member_required(login_url='/admin/login')
@permission_required('crm_partner_detail', 'Детальный просмотр раздела Партнеры')
def crm_partner_detail(request, id=None):
    partner = get_object_or_404(Partners, id=id) if id else None

    if request.method == "POST":
        form = PartnersForm(request.POST, request.FILES, instance=partner)
        if "update" in request.POST and form.is_valid():
            form.save()
            return redirect('crm_partner_index')
        elif "delete" in request.POST:
            partner.delete()
            return redirect('crm_partner_index')
        elif "save" in request.POST and form.is_valid():
            form.save()
            return redirect('crm_partner_index')
    else:
        form = PartnersForm(instance=partner)

    context = {
        'form': form,
        'partner': partner
    }
    return render(request, 'queenbee/partner/detail.html', context)

def get_partner_data(request):
    fields = request.GET.get('fields')
    list_display = fields.split(',') if fields else ['id', 'title', 'partners_url', 'created']

    try:
        filters = {}

        partners = Partners.objects.filter(**filters).values_list(*list_display, named=True).order_by('-created')

        model_admin = admin.site._registry[Partners]
        field_names = {
            field: label_for_field(field, Partners, model_admin)
            for field in list_display
        }

        return JsonResponse({
            'partners': [partner._asdict() for partner in partners],
            'field_names': field_names,
        })

    except Exception as e:
        print("Error", e)
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)