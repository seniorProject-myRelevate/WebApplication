from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, ReadOnlyPasswordHashField
from passwords.fields import PasswordField
from passwords.validators import LengthValidator, ComplexityValidator


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
                             label='')
    password = PasswordField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
                             label='')

    class Meta:
        fields = ['email', 'password']


class PasswordChangeForm(UserChangeForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}), label='')

    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"password/\">this form</a>."))

    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Old Password', 'class': 'form-control'}), label='')

    new_password1 = PasswordField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': 'form-control'}), label='',
        validators=[LengthValidator(min_length=6), ComplexityValidator(complexities=dict(UPPER=1, LOWER=1, DIGITS=1))])

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}), label='')

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'old_password', 'new_password1', 'new_password2']

    def clean(self):
        """
        Verifies that the values entered into the password fields match
        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        cleaned_data = super(PasswordChangeForm, self).clean()
        try:
            user = get_user_model().objects.get(email=self.cleaned_data['email'])
        except:
            raise forms.ValidationError('Email not found.')

        if not user.check_password(self.cleaned_data['old_password']):
            raise forms.ValidationError('Old password is not correct.')
        if self.cleaned_data['new_password1'] != self.cleaned_data['new_password2'] and \
                        self.cleaned_data['old_password'] != self.cleaned_data['new_password1'] and \
                        self.cleaned_data['new_password1'] != "":
            raise forms.ValidationError('Passwords must match.')

        return self.cleaned_data

    def save(self, commit=True):
        user = super(PasswordChangeForm, self).save(commit=False)
        user.set_password(self.cleaned_data['new_password1'])
        if commit:
            user.save()
        return user


class RegistrationForm(forms.ModelForm):
    """
    Registration form, allows users to create accounts.
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}), label='')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
                                 label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
                                label='')
    password1 = PasswordField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
                              label='', validators=[LengthValidator(min_length=6),
                                                    ComplexityValidator(complexities=dict(UPPER=1, LOWER=1, DIGITS=1))])
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}), label='')

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['email']
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError("Email is already in use.")
        return username

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        self.cleaned_data['first_name'] = self.cleaned_data['first_name'].capitalize()
        self.cleaned_data['last_name'] = self.cleaned_data['last_name'].capitalize()
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
