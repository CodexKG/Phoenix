from django import forms 

from apps.cms.models import Partners, Service, FAQ

class PartnersForm(forms.ModelForm):
    class Meta:
        model = Partners
        fields = "__all__"

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = "__all__"