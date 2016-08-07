from django import forms
from .models import Advisers


class AdviserApplicationForm(forms.ModelForm):
    class Meta:
        model = Advisers
        fields = ['accept_terms']


class UpdateAvailableForm(forms.ModelForm):
    class Meta:
        model = Advisers
        fields = ['is_available']
