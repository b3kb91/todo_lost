from django import forms
from django.core.exceptions import ValidationError
from webapp.models import Issue, Type, Status
from django.forms import widgets


class IssueForm(forms.ModelForm):
    statuses = forms.ModelChoiceField(queryset=Status.objects.all()),
    types = forms.ModelMultipleChoiceField(queryset=Type.objects.all(),
                                           widget=forms.CheckboxSelectMultiple(), required=False)

    def clean_summary(self):
        summary = self.cleaned_data['summary']
        if len(summary) <= 3:
            raise ValidationError("Слишком короткое описание, попробуйте подлиннее")
        else:
            return summary

    def clean_description(self):
        description = self.cleaned_data['description']
        if not len(description) <= 100:
            raise ValidationError("Это поле очень длинное, нужно меньше символов")
        else:
            return description

    class Meta:
        model = Issue
        fields = ['description', 'summary', 'statuses', 'types']
        error_messages = {
            "summary": {
                "required": "Поле обязательное"},

        }
        widgets = {
            'description': widgets.Textarea(attrs={'cols': 20, "rows": 5}),

        }
