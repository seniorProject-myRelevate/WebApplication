from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.forms import modelformset_factory

from .forms import ContributorForm, DegreeForm, ProgramForm, AreaOfExpertiseForm, BiographyForm, InterestForm, \
    ContactForm, AvatarForm, CVResumeForm, ApprovalUpdateUserForm

from ..models import Topics
from models import ContributorProfile, PendingContributors
from ..models import User
from ..Advisers.models import Advisers

from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context


def index(request):
    if not request.user.is_contributor:
        return HttpResponseRedirect(reverse('myrelevate:index'))
    return render(request, 'articles.html', {'form': None})


@login_required()
def create(request):
    """
    Allows user to apply to get become a contributor
    :param request:
    :return: redirect to index page
    """
    advisers = Advisers.objects.filter(is_available=True)
    users = User.objects.filter(is_adviser=True)

    if request.method == 'POST':
        form = ContributorForm(request.POST, request.FILES)
        if form.is_valid():
            user = get_user_model().objects.get(email=request.user.email)
            pending_contributor = PendingContributors()
            contributor_profile = form.save()
            user.contributor_profile = contributor_profile
            pending_contributor.contributor = contributor_profile
            pending_contributor.save()
            user.save()
            return HttpResponseRedirect(reverse('myrelevate:index'))
        else:
            return HttpResponse(form.errors)
    else:
        contributor_form = ContributorForm()
    return render(request, 'application.html', {'contributorForm': contributor_form,
                                                'advisers': advisers, 'users': users})


@login_required()
def update(request):
    """
    Allows a user with contributor access to edit their contributor profile page
    Allows a contributor to post new articles
    :param request:
    :return: a redirect to contributor profile page
    """
    if request.method == 'POST':
        user = get_user_model().objects.get(email=request.user.email)
        form = ContributorForm(request.POST, request.FILES, instance=user.contributor_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myrelevate:contributor_profile'))
        else:
            return HttpResponse(form.errors)
    else:
        user = get_user_model().objects.get(email=request.user.email)
        profile = user.get_contributor_profile()
        topics = Topics.objects.all()
    return render(request, 'contributorprofile.html', {'contributorProfile': profile,
                                                       'topics': topics,
                                                       'contributorForm': ContributorForm(instance=profile),
                                                       'degreeForm': DegreeForm(instance=profile),
                                                       'programForm': ProgramForm(instance=profile),
                                                       'biographyForm': BiographyForm(instance=profile),
                                                       'interestForm': InterestForm(instance=profile),
                                                       'contactForm': ContactForm(instance=profile),
                                                       'avatarForm': AvatarForm(instance=profile),
                                                       'resumeForm': CVResumeForm(instance=profile)})


@login_required()
def update_degree(request):
    if request.method == 'POST':
        form = DegreeForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid:
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def update_area_of_expertise(request):
    if request.method == 'POST':
        form = AreaOfExpertiseForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid:
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def update_biography(request):
    if request.method == 'POST':
        form = BiographyForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid:
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def update_interest(request):
    if request.method == 'POST':
        form = InterestForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid:
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def update_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid:
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def update_program(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse(form.errors)
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def update_avatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=request.user.contributor_profile)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse(form.errors)
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def update_cv_resume(request):
    if request.method == 'POST':
        form = CVResumeForm(request.POST, request.FILES, instance=request.user.contributor_profile)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse(form.errors)
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def remove(request):
    pass


def contributors(request):
    """
    Displays list of all contributors.
    Allows a person to search contributors based on a set of given topics
    :param request:
    :return: The requested searched data
    """
    users = User.objects.filter(is_contributor=True)
    profiles_ids = User.objects.values_list('contributor_profile_id', flat=True)
    contributor_profiles = ContributorProfile.objects.filter(id__in=profiles_ids)
    if request.method == 'GET':
        if 'q' in request.GET and request.GET['q']:
            q = request.GET['q']
            profiles = users.filter(first_name__icontains=q)
            return render(request, 'contributors.html', {'profiles': profiles, 'query': q})
        else:
            pass
    else:
        pass
    return render(request, 'contributors.html', {'contributors': contributor_profiles, 'users': users})


@login_required()
def approve(request):
    """
    Displays list of all users that have applied for contributor access
    Displays application from user for contributor access
    Allows staff member to approve user for contributor access
    :param request:
    :return: The contributor profile from application, the users being evaluated, and
    formset: a list of forms for each user
    """
    pending_contributor_ids = PendingContributors.objects.values_list('contributor_id', flat=True)
    contributor_profiles = ContributorProfile.objects.filter(id__in=pending_contributor_ids)
    users = User.objects.filter(contributor_profile=pending_contributor_ids)
    # profile_ids = User.objects.values_list('contributor_profile_id', flat=True)
    # profiles = ContributorProfile.objects.filter(id__in=profile_ids)
    approve_form_set = modelformset_factory(User, form=ApprovalUpdateUserForm, extra=0)

    for user in users:
        if user.is_contributor:
            PendingContributors.objects.filter(contributor_id=user.contributor_profile).delete()

    if request.method == 'POST':
        formset = approve_form_set(request.POST, queryset=users)
        if formset.is_valid():
            formset.save()
            for form in formset:
                contact_name = form.instance.first_name + user.last_name
                contact_email = form.instance.email

                # Email the profile with the
                # contact information
                if (user.is_contributor):
                    template = get_template('approval.txt')
                else:
                    template = get_template('denied.txt')
                context = Context({
                    'contact_name': contact_name,
                    'contact_email': contact_email,
                })
                content = template.render(context)

                email = EmailMessage(
                    "Contributor Application Status",
                    content,
                    "http://www.myrelevate.com" +'',
                    ['relevate@gmail.com'],
                    headers = {'Reply-To': contact_email }
                )
                email.send()
            return HttpResponseRedirect(reverse('myrelevate:contributor:approve'))
        else:
            return HttpResponse(formset.errors)
    else:
        formset = approve_form_set(queryset=users)
    return render(request, 'approval.html', {'profiles': contributor_profiles, 'users_forms': zip(users, formset),
                                             'formset': formset})


# @login_required()
# def denied(request):
#     denied_contributors_ids = DeniedContributors.objects.values_list('contributor_id', flat=True)
#     contributor_profiles = ContributorProfile.objects.filter(id__in=denied_contributors_ids)
#     users = User.objects.filter(contributor_profile=denied_contributors_ids)
#     denied_form_set = modelformset_factory(DeniedContributors, form=DeniedContributorForm, extra=0)
#
#     if request.method == 'POST':
#         formset = denied_form_set(request.POST)
#         if formset.is_valid():
#             formset.save()
#         else:
#             return HttpResponse(formset.errors)
#     return HttpResponseRedirect(reverse('myrelevate:contributor:approve'))
