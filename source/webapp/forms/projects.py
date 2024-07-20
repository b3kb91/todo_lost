from django import forms
from django.core.exceptions import ValidationError
from webapp.models import Project
from django.forms import widgets


class ProjectForm(forms.ModelForm):

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) <= 3:
            raise ValidationError("Слишком короткое описание, попробуйте подлиннее")
        else:
            return title

    def clean_description(self):
        description = self.cleaned_data['description']
        if not len(description) <= 75:
            raise ValidationError("Это поле очень длинное, нужно меньше символов")
        else:
            return description

    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date']
        error_messages = {
            "title": {
                "required": "Поле обязательное"},
            "start_date": {
                "required": "Поле обязательное"},

        }
        widgets = {
            'description': widgets.Textarea(attrs={'cols': 20, "rows": 5}),
            'start_date': widgets.DateInput(attrs={'type': 'date'}),
            'end_date': widgets.DateInput(attrs={'type': 'date'})

        }
