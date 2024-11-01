from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(login_url='/admin/login')
def crm_index(request):
    return render(request, 'queenbee/index.html')