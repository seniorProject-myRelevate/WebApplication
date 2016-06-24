import os

from django import forms

from .models import Subscriber
from .models import Adviser


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


class SubscribeForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'required': True, 'placeholder': 'Email', 'class': 'form-control', 'data-toggle': 'popover',
               'data-placement': 'bottom', 'data-content': 'Please enter a valid email address.'}), label='')

    class Meta:
        model = Subscriber
        fields = ['email']


class AdviserForm(forms.ModelForm):
    adviser_email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Adviser Email', 'class': 'form-control'}),
                                     label='', required=False)
    adviser_first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Adviser First Name',
                                                                       'class': 'form-control'}), label='', required=False)
    adviser_last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Adviser Last Name',
                                                                      'class': 'form-control'}), label='', required=False)

    class Meta:
        model = Adviser
        fields = {'adviser_email', 'adviser_first_name', 'adviser_last_name'}

    # def save(self, commit=True, email=None):
    #     adviser = super(AdviserForm, self).save(commit=False)
    #     if commit:
    #         adviser