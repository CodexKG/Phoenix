from django.shortcuts import render, redirect

def crm_index(request):
    return render(request, 'queenbee/index.html')