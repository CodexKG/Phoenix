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

class CardForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        label="Срок выполнения",  # Это verbose_name для поля
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False
    )
    members = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Участники',  # Placeholder для поля участников
        }),
        required=False
    )

    class Meta:
        model = models.Card
        fields = ['title', 'description', 'due_date', 'members']