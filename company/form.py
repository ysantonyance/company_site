import re
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator

from .models import Branch, Employee


def validate_no_forbidden_words(value):
    forbidden = ['спам', 'реклама', 'казино']
    lowered = value.lower()
    for word in forbidden:
        if word in lowered:
            raise ValidationError(f"Слово «{word}» запрещено в этом поле.")


phone_validator = RegexValidator(
    regex=r'^\+?[0-9\s\-\(\)]{7,20}$',
    message="Введите корректный номер телефона (например, +359 87 758 2495)."
)

name_validator = RegexValidator(
    regex=r'^[A-Za-zА-Яа-яЁёІіЇїЄєҐґ\s\-\']+$',
    message="Имя может содержать только буквы, пробелы, дефис и апостроф — без цифр."
)


class CompanyEntryForm(forms.Form):
    full_name = forms.CharField(
        label="Имя / Контактное лицо",
        max_length=150,
        validators=[
            MinLengthValidator(2, message="Имя должно содержать минимум 2 символа."),
            name_validator,
            validate_no_forbidden_words,
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Карина Зиновьева'}),
    )

    email = forms.EmailField(
        label="Email",
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': 'name@example.com'}),
    )

    phone = forms.CharField(
        label="Телефон",
        max_length=20,
        required=False,
        validators=[phone_validator],
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
        widget=forms.NumberInput(attrs={'step': '0.50', 'placeholder': '10.00'}),
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
        widget=forms.DateInput(attrs={'type': 'date'}),
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

    is_urgent = forms.BooleanField(
        label="Срочно",
        required=False,
    )

    notes = forms.CharField(
        label="Комментарий / описание",
        min_length=10,
        validators=[validate_no_forbidden_words],
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Опишите детали...',
        }),
    )

    def clean_notes(self):
        notes = self.cleaned_data.get('notes', '').strip()
        if len(notes) < 10:
            raise ValidationError("Комментарий должен содержать минимум 10 символов без учёта пробелов.")
        return notes

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        is_urgent = cleaned_data.get('is_urgent')
        deadline = cleaned_data.get('deadline')

        if not email and not phone:
            raise ValidationError("Укажите хотя бы Email или телефон для обратной связи.")

        if is_urgent and not deadline:
            self.add_error('deadline', "Для срочного обращения укажите дату / дедлайн.")

        return cleaned_data