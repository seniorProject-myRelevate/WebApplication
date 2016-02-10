import os

from django import forms
from passwords.fields import PasswordField
from passwords.validators import LengthValidator, ComplexityValidator

from .models import ContributorProfile, Subscriber
from django.contrib.auth import get_user_model


class ExtFileField(forms.FileField):
    """
    Same as forms.FileField, but you can specify a file extension whitelist.

    >>> from django.core.files.uploadedfile import SimpleUploadedFile
    >>>
    >>> t = ExtFileField(ext_whitelist=(".pdf", ".txt"))
    >>>
    >>> t.clean(SimpleUploadedFile('filename.pdf', 'Some File Content'))
    >>> t.clean(SimpleUploadedFile('filename.txt', 'Some File Content'))
    >>>
    >>> t.clean(SimpleUploadedFile('filename.exe', 'Some File Content'))
    Traceback (most recent call last):
    ...
    ValidationError: [u'Not allowed filetype!']
    """

    def __init__(self, *args, **kwargs):
        ext_whitelist = kwargs.pop("ext_whitelist")
        ext_maxsize = kwargs.pop("ext_maxsize")

        self.ext_whitelist = [i.lower() for i in ext_whitelist]
        self.maxsize = ext_maxsize

        super(ExtFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ExtFileField, self).clean(*args, **kwargs)
        filename = data.name
        ext = os.path.splitext(filename)[1]
        ext = ext.lower()
        if ext not in self.ext_whitelist:
            raise forms.ValidationError("Not allowed filetype!")


class SpecificFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        mimetype_whitelist = kwargs.pop("mimetype_whitelist")

        self.mimetype_whitelist = [i.lower() for i in mimetype_whitelist]

        super(SpecificFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(SpecificFileField, self).clean(*args, **kwargs)
        mime_type = data.content_type
        bool = False
        if mime_type not in self.mimetype_whitelist:
            bool = True
            raise forms.ValidationError("Not allowed filetype!")


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
                                label='')
    password = PasswordField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
                             label='')

    class Meta:
        fields = ['email', 'password']


class RegistrationForm(forms.ModelForm):
    """
    Registration form, allows users to create accounts.
    """
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
                               label='')
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

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

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


class PasswordChangeForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}), label='')

    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Old Password', 'class': 'form-control'}), label='')

    password1 = PasswordField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': 'form-control'}), label='',
        validators=[LengthValidator(min_length=6), ComplexityValidator(complexities=dict(UPPER=1, LOWER=1, DIGITS=1))])

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}), label='')

    class Meta:
        model = get_user_model()
        fields = ['email', 'old_password', 'password1', 'password2']

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        cleaned_data = super(PasswordChangeForm, self).clean()
        user = get_user_model().objects.get(email=self.cleaned_data['email'])
        if user.check_password(self.cleaned_data['old_password']):
            raise forms.ValidationError("Your password is incorrect.")
        elif 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(PasswordChangeForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user_profile = None
        if commit:
            user.save()
        return user_profile


class ContributorRequestForm(forms.ModelForm):
    cv = SpecificFileField(label='Specific MIME type',
                           mimetype_whitelist=("application/pdf", "application/msword",
                                               "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))
    accept_terms = forms.BooleanField(widget=forms.CheckboxInput(), label='I agree to terms')

    class Meta:
        model = ContributorProfile
        fields = ['cv']

    def clean(self):
        cleaned_data = super(ContributorRequestForm, self).clean()
        return self.cleaned_data

    def save(self):
        pass


class SubscribeForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'required': True, 'placeholder': 'Email', 'class': 'form-control', 'data-toggle': 'popover',
               'data-placement': 'bottom', 'data-content': 'Please enter a valid email address.'}), label='')

    idea = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'What would you like to see?'}), label='',
                           required=False)

    class Meta:
        model = Subscriber
        fields = ['email']
