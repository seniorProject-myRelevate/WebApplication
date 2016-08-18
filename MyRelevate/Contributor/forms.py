from django import forms
from .models import ContributorProfile
from ..models import User
from ..Advisers.models import Advisers


class ContributorForm(forms.ModelForm):
    interests = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Clinical and resources interests.',
                                                             'class': 'form-control'}), label='', required=False)
    cv = forms.FileField(label='Specific MIME type', required=True)
                           # mimetype_whitelist=("application/pdf", "application/msword",
                           #                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                           #                     ))

    class Meta:
        model = ContributorProfile
        fields = [
            'adviser', 'degree', 'program', 'institution', 'biography', 'interests', 'address',
            'city', 'state', 'zipcode', 'cv', 'accept_terms', 'website_url'
        ]
        widgets = {
            'accept_terms': forms.CheckboxInput(),
            'program': forms.TextInput(attrs={'placeholder': 'Field of study/specialization', 'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'placeholder': 'Institution ex:Kansas State University',
                                                  'class': 'form-control'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}),
            'state': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'placeholder': 'Zipcode', 'class': 'form-control'}),
            'website_url': forms.URLInput(attrs={'placeholder': 'Website URL', 'class': 'form-control'}),
            'biography': forms.Textarea(attrs={'placeholder': 'Write a brief biography about yourself.',
                                               'class': 'form-control'}),
        }
        labels = {
            'adviser': '',
            'program': '',
            'institution': '',
            'address': '',
            'city': '',
            'state': '',
            'zipcode': '',
            'website_url': '',
            'biography': '',
        }


class DegreeForm(forms.ModelForm):
    class Meta:
        model = ContributorProfile
        fields = ['degree']
        labels = {
            'degree': ''
        }


class ProgramForm(forms.ModelForm):
    class Meta:
        model = ContributorProfile
        fields = ['program']
        labels = {
            'program': ''
        }


class AreaOfExpertiseForm(forms.ModelForm):
    class Meta:
        model = ContributorProfile
        fields = ['expertise_topics']
        labels = {
            'expertise_topics': ''
        }


class BiographyForm(forms.ModelForm):
    class Meta:
        model = ContributorProfile
        fields = ['biography']
        labels = {
            'biography': ''
        }


class InterestForm(forms.ModelForm):
    class Meta:
        model = ContributorProfile
        fields = ['interests']
        labels = {
            'interests': ''
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContributorProfile
        fields = ['address', 'city', 'state', 'zipcode', 'website_url']


class AvatarForm(forms.ModelForm):
    class Meta:
        model = ContributorProfile
        fields = ['avatar']


class CVResumeForm(forms.ModelForm):
    class Meta:
        model = ContributorProfile
        fields = ['cv']
        labels = {
            'cv': ''
        }


class ApprovalUpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_contributor']
        labels = {
            'is_contributor': 'Approve Contributor',
        }


# class DeniedContributorForm(forms.ModelForm):
#     class Meta:
#         model = DeniedContributors
#         fields = ['reason, denied']
#         widgets = {
#             'reason': forms.Textarea(attrs={'placeholder': 'Write a brief biography about yourself.',
#                                             'class': 'form-control'}),
#         }
#         labels = {
#             'reason': '',
#             'denied': '',
#         }
