from django import forms
from .models import User, UserProfile
from passwords.fields import PasswordField
from passwords.validators import LengthValidator, ComplexityValidator


class LoginForm(forms.Form):
    username = forms.EmailField(widget=forms.EmailInput, label="Email")
    password = PasswordField(widget=forms.PasswordInput, label='Password')

    class Meta:
        fields = ['username', 'password']


class RegistrationForm(forms.ModelForm):
    """
    Registration form, allows users to create accounts.
    """
    username = forms.CharField(widget=forms.EmailInput, label='Email')
    first_name = forms.CharField(widget=forms.TextInput, label='First Name')
    last_name = forms.CharField(widget=forms.TextInput, label='Last Name')
    password1 = PasswordField(widget=forms.PasswordInput, label='Password',
                              validators=[LengthValidator(min_length=6),
                                          ComplexityValidator(complexities=dict(UPPER=1, LOWER=1, DIGITS=1))])
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

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

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user