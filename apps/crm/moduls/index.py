from django.shortcuts import render, redirect

def crm_index(request):
    return render(request, 'crm/index.html')