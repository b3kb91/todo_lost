from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class MyUserCreationForm(UserCreationForm):

    def clean_first_name_last_name(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if not first_name or last_name:
            raise ValidationError('Введите имя или фамилию')
        else:
            return last_name, first_name

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']
        error_messages = {
            "email": {
                "required": "Поле обязательное"}
        }

