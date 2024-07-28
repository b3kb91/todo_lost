from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class MyUserCreationForm(UserCreationForm):

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')

        if not (first_name or last_name):
            raise ValidationError('Введите имя или фамилию')

        if not email:
            raise ValidationError('Введите свой email')

        return cleaned_data

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']
        error_messages = {
            "email": {
                "required": "Поле обязательное"}
        }


class UserForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple,
                                           required=False)

