from django import forms 

from apps.erp.models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"
    
    # def __init__(self, *args, **kwargs):
    #     request = kwargs.pop('request', None)
    #     super().__init__(*args, **kwargs)
    #     if request:
    #         selected_city_id = request.session.get('selected_city')
    #         if selected_city_id:
    #             try:
    #                 selected_city = City.objects.get(id=selected_city_id)
    #                 self.fields['city'].initial = selected_city
    #             except City.DoesNotExist:
    #                 pass