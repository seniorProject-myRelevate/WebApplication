from django import forms
from .models import Advisers
from ..User.models import User


class AdviserApplicationForm(forms.ModelForm):
    class Meta:
        model = Advisers
        fields = ['accept_terms', 'number_of_advisees', 'description']


class ApproveAdviserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_adviser']


class UpdateAdviserForm(forms.ModelForm):
    class Meta:
        model = Advisers
        fields = ['is_available', 'number_of_advisees', 'description']
        labels = {
            'is_available': 'Approve Adviser',
            'number_of_advisees': '',
            'description': '',
        }

