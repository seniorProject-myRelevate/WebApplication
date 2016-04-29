from django import forms
from django.contrib.auth import get_user_model
from passwords.fields import PasswordField
from passwords.validators import LengthValidator, ComplexityValidator


class UserDataForm(forms.ModelForm):
    curr_password = PasswordField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Current Password', 'class': 'form-control'}), label='')
    new_password1 = PasswordField(required=False, widget=forms.PasswordInput(
        attrs={'placeholder': 'New Password', 'class': 'form-control'}), label='',
                                  validators=[LengthValidator(min_length=6),
                                              ComplexityValidator(complexities=dict(UPPER=1, LOWER=1, DIGITS=1))])
    new_password2 = PasswordField(required=False, widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}), label='')

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),

        }

    def clean(self):
        cleaned_data = super(UserDataForm, self).clean()
        user = get_user_model().objects.get(email=self.cleaned_data['email'])
        if not user.check_password(self.cleaned_data['curr_password']):
            self.add_error('curr_password', 'Incorrect password')
        if self.cleaned_data['new_password1'] and not self.cleaned_data['new_password1'] < \
                self.new_password1.validators[LengthValidator.min_length]:
            self.add_error('new_password1', 'Password must have atleast 6 characters.')
            if self.cleaned_data['new_password1'] is self.cleaned_data['new_password2']:
                self.add_error('new_password2', 'Passwords must match')
        return cleaned_data

    def save(self, commit=True):
        cleaned_data = super(UserDataForm, self).save(commit=False)
        if commit:
            user = get_user_model().objects.get(email=self.cleaned_data['email'])
