from django import forms
from django.core.validators import MinLengthValidator

from .models import Branch, Employee


class CompanyEntryForm(forms.Form):
    """Form for company requests, branches, tasks, or ice cream donations."""

    full_name = forms.CharField(
        label="Имя / Контактное лицо",
        max_length=150,
        validators=[MinLengthValidator(2)],
        widget=forms.TextInput(attrs={
            'placeholder': 'Карина Зиновьева',
        }),
    )

    email = forms.EmailField(
        label="Email",
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'name@example.com',
        }),
    )

    phone = forms.CharField(
        label="Телефон",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '+359 87 758 2495',
            'type': 'tel',
        }),
    )

    amount = forms.DecimalField(
        label="Сумма (донаты / бюджет)",
        max_digits=10,
        decimal_places=2,
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'step': '0.50',
            'placeholder': '10.00',
        }),
    )

    priority = forms.IntegerField(
        label="Приоритет задачи (1–5)",
        min_value=1,
        max_value=5,
        required=False,
        initial=3,
        widget=forms.NumberInput(),
    )

    deadline = forms.DateField(
        label="Дата / Дедлайн",
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
        }),
    )

    branch = forms.ModelChoiceField(
        label="Филиал",
        queryset=Branch.objects.all(),
        required=False,
        empty_label="— Выберите филиал —",
    )

    assignee = forms.ModelChoiceField(
        label="Ответственный сотрудник",
        queryset=Employee.objects.all(),
        required=False,
        empty_label="— Без ответственного —",
    )

    flavor = forms.ChoiceField(
        label="Вкус мороженого",
        required=False,
        choices=[
            ('plombir', 'Пломбир'),
            ('pistachio', 'Фисташка'),
            ('chocolate', 'Шоколад'),
            ('mango', 'Манго'),
        ],
    )

    categories = forms.MultipleChoiceField(
        label="Разделы компании",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[
            ('branches', 'Филиалы'),
            ('employees', 'Работники'),
            ('news', 'Новости'),
            ('donations', 'Фонд мороженого'),
            ('tasks', 'Задачи'),
        ],
    )

    is_urgent = forms.BooleanField(
        label="Срочно",
        required=False,
    )

    notes = forms.CharField(
        label="Комментарий / описание",
        min_length=10,
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Опишите детали...',
        }),
    )

    def clean_notes(self):
        notes = self.cleaned_data.get('notes', '')
        cleaned = notes.strip()
        if len(cleaned) < 10:
            raise forms.ValidationError("Комментарий должен содержать минимум 10 символов.")
        return cleaned