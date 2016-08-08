from django import forms
from .models import Advisers
from ..models import User


class AdviserApplicationForm(forms.ModelForm):
    class Meta:
        model = Advisers
        fields = ['accept_terms']


class ApproveAdviserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_adviser']


class UpdateAvailableForm(forms.ModelForm):
    class Meta:
        model = Advisers
        fields = ['is_available']
