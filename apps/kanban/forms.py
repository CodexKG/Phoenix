from django import forms

from apps.kanban import models
from apps.erp.models import Employee
from .models import Attachment


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True  # Разрешить множественный выбор файлов


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


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
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-title-table',
                'placeholder': 'Название доски'
            })
        }


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
    file = MultipleFileField(
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'multiple': True,
        }),
        label="Файл",
        required=False
    )

    class Meta:
        model = models.Attachment
        fields = ['file']
