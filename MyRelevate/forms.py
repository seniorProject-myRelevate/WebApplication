from django import forms
from .models import User
from .models import User
from passwords.fields import PasswordField
from passwords.validators import LengthValidator, ComplexityValidator


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput, label="Email")
    password = PasswordField(widget=forms.PasswordInput, label='Password')

    class Meta:
        fields = ['email', 'password']


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput, label='Email')
    password1 = PasswordField(widget=forms.PasswordInput, label='Password', validators=[{
        LengthValidator(min_length=5), ComplexityValidator(complexities=dict(UPPER=1, LOWER=1, DIGITS=1))
    }])
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    first_name = forms.CharField(widget=forms.TextInput, max_length=50, label='First name')
    last_name = forms.CharField(widget=forms.TextInput, max_length=100, label='Last name')

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data
