from django import forms

from apps.kanban import models 

class ListForm(forms.ModelForm):
    class Meta:
        model = models.List
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название списка'
            })
        }

class BoardForm(forms.ModelForm):
    class Meta:
        model = models.Board
        fields = ['title']