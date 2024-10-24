from django.urls import path 

from apps.settings.views import index, about, contact, faq, services, services_details

urlpatterns = [
    path('', index, name="index"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),
    path('faq/', faq, name="faq"),
    path('services/', services, name="services"),
    path('services_details/', services_details, name="services_details"),
]