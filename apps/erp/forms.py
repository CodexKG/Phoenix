from django import forms 
from django.db.models import Q

from apps.erp.models import Employee, GroupPermission
from apps.hiveclient.models import User

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('user', 'last_name', 'first_name', 'phone', 'selery',
                  'email', 'address', 'date_of_birth', 'image', 'employee_position',
                  'bio', 'groups', 'user_permissions')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если запись редактируется и у сотрудника уже есть связанный пользователь
        if self.instance and self.instance.pk:
            # Включаем текущего пользователя в список доступных
            self.fields['user'].queryset = User.objects.filter(
                Q(user_employee__isnull=True) | Q(pk=self.instance.user.pk)
            )
        else:
            # Если запись новая, фильтруем, чтобы показывать только пользователей без Employee
            self.fields['user'].queryset = User.objects.filter(user_employee__isnull=True)
    
class GroupPermissionForm(forms.ModelForm):
    class Meta:
        model = GroupPermission
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