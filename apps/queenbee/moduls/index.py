from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required

from apps.crm.models import Billing

@staff_member_required(login_url='/admin/login')
def crm_index(request):
    billings = Billing.objects.all().order_by('-created')[:7]
    return render(request, 'queenbee/index.html', locals())