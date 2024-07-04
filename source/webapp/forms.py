from django import forms
from django.core.exceptions import ValidationError
from webapp.models import ToDo
from django.forms import widgets


class ToDoForm(forms.ModelForm):
    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) <= 3:
            raise ValidationError("Слишком короткое описание, попробуйте подлиннее")
        else:
            return description

    class Meta:
        model = ToDo
        fields = ['description', 'description_detail', 'status', 'date_completion']
        error_messages = {
            "description": {
                "required": "Поле обязательное"
            }
        }
        widgets = {
            'description_detail': widgets.Textarea(attrs={'cols': 20, "rows": 5}),
            'date_completion': widgets.DateInput(attrs={"type": "date"}),
        }
