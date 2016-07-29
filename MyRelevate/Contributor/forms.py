from django import forms
from .models import ContributorProfile
from ..models import User
from MyRelevate.models import Denied


class ContributorForm(forms.ModelForm):
    DEGREES = (
        ('-1', ''),
        ('MS', 'MS (Master of Science)'),
        ('MA', 'MA (Master of Arts)'),
        ('PhD', 'PhD (Doctor of Philosophy)'),
        ('PsyD', 'PsyD (Doctor of Psychology)'),
        ('SU', 'Student-Undergraduate'),
        ('SM', 'Student-Masters'),
        ('SPhD', 'Student-PhD'),
        ('SPsyD', 'Student-PsyD')
    )

    credential = forms.ChoiceField(choices=DEGREES, required=True)
    adviser_email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Adviser Email', 'class': 'form-control'}),
                                     label='', required=False)
    adviser_first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Adviser First Name',
                                                                       'class': 'form-control'}), label='', required=False)
    adviser_last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Adviser Last Name',
                                                                      'class': 'form-control'}), label='', required=False)
    # program = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Field of study/specialization',
    #                                                         'class': 'form-control'}), label='')
    # institution = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Institution ex:Kansas State University',
    #                                                             'class': 'form-control'}), label='')
    # address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control'}),
    #                           label='')
    # city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}), label='')
    # state = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control'}), label='')
    # zipcode = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Zipcode', 'class': 'form-control'}),
    #                           label='')
    # website_url = forms.URLField(widget=forms.URLInput(attrs={'placeholder': 'Website URL', 'class': 'form-control'}),
    #                              label='')
    # biography = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write a brief biography about yourself.',
    #                                                          'class': 'form-control'}), label='')
    interests = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Clinical and resources interests.',
                                                             'class': 'form-control'}), label='', required=False)
    cv = forms.FileField(label='Specific MIME type', required=False)
                           # mimetype_whitelist=("application/pdf", "application/msword",
                           #                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                           #                     ))

    accept_terms = forms.BooleanField(widget=forms.CheckboxInput(), label='I agree to terms')

    class Meta:
        model = ContributorProfile
        fields = ['credential', 'program', 'institution', 'adviser_email', 'adviser_first_name', 'adviser_last_name',
                  'biography', 'interests', 'address', 'city', 'state', 'zipcode', 'cv', 'accept_terms', 'website_url']
        widgets = {
            'program': forms.TextInput(attrs={'placeholder': 'Field of study/specialization', 'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'placeholder': 'Institution ex:Kansas State University',
                                                  'class': 'form-control'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'placeholder': 'Zipcode', 'class': 'form-control'}),
            'website_url': forms.URLInput(attrs={'placeholder': 'Website URL', 'class': 'form-control'}),
            'biography': forms.Textarea(attrs={'placeholder': 'Write a brief biography about yourself.',
                                               'class': 'form-control'}),
        }
        labels = {
            'program': '',
            'institution': '',
            'address': '',
            'city': '',
            'state': '',
            'zipcode': '',
            'website_url': '',
            'biography': '',
        }


class CredentialForm(forms.ModelForm):
    class Meta:
        model = ContributorProfile
        fields = ['credential']


class AreaOfExpertiseForm(forms.ModelForm):
    class Meta:
        model = ContributorProfile
        fields = ['expertise_topics']


class BiographyForm(forms.ModelForm):
    class Meta:
        model = ContributorProfile
        fields = ['biography']


class InterestForm(forms.ModelForm):
    class Meta:
        model = ContributorProfile
        fields = ['interests']


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContributorProfile
        fields = ['address', 'city', 'state', 'zipcode']


class ApprovalUpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_contributor']
        labels = {
            'is_contributor': 'Approve Contributor',
        }


# class DeniedContributorUserForm(forms.ModelForm):
#     reason1 = forms.CharField(widget=forms.Textarea(
#         attrs={'placeholder': 'Write a brief reason why user was denied contributor access.',
#                'class': 'form-control'}), label='')
#     reason2 = forms.CharField(widget=forms.Textarea(
#         attrs={'placeholder': 'Write a brief reason why user was denied contributor access.',
#                'class': 'form-control'}), label='')
#     reason3 = forms.CharField(widget=forms.Textarea(
#         attrs={'placeholder': 'Write a brief reason why user was denied contributor access.',
#                'class': 'form-control'}), label='')
#     reason4 = forms.CharField(widget=forms.Textarea(
#         attrs={'placeholder': 'Write a brief reason why user was denied contributor access.',
#                'class': 'form-control'}), label='')
#     reason5 = forms.CharField(widget=forms.Textarea(
#         attrs={'placeholder': 'Write a brief reason why user was denied contributor access.',
#                'class': 'form-control'}), label='')
#
#     class Meta:
#         model = Denied
#         fields = ['user, reason1, reason2, reason3, reason4, reason5']
