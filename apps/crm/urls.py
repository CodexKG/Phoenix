from django.urls import path 

from apps.crm.moduls.index import crm_index

urlpatterns = [
    path('', crm_index, name="crm_index")
]