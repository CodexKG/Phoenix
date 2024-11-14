from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from apps.hiveclient.models import User
from apps.erp.models import Employee

class UsersForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = "__all__"

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Текущий пароль'}),
        label="Текущий пароль"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новый пароль'}),
        label="Новый пароль"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите новый пароль'}),
        label="Подтвердите новый пароль"
    )

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        
class CRMEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'phone', 'email',
                  'address', 'date_of_birth', 'image', 'bio')