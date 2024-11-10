from django import forms

from apps.kanban import models 
from apps.erp.models import Employee

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
        label="Срок выполнения",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False
    )
    members = forms.ModelMultipleChoiceField(
        queryset=models.Employee.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'placeholder': 'Выберите участников',
        }),
        required=False
    )

    class Meta:
        model = models.Card
        fields = ['title', 'description', 'due_date', 'members']

# Создаем InlineFormSet для вложений
AttachmentInlineFormset = forms.inlineformset_factory(
    models.Card,
    models.Attachment,
    fields=('file',),
    extra=1,
    can_delete=True
)

class AttachmentForm(forms.ModelForm):
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
        }),
        label="Файл"
    )

    class Meta:
        model = models.Attachment
        fields = ['file']