from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.forms import modelformset_factory

from .forms import ContributorForm, DegreeForm, ProgramForm, AreaOfExpertiseForm, BiographyForm, InterestForm, \
    ContactForm, AvatarForm, CVResumeForm, ApprovalUpdateUserForm

from ..models import Topics
from models import Degree, ContributorProfile, PendingContributors
from ..models import User
from ..Advisers.models import Advisers


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
    degrees = Degree.objects.all()
    advisers = Advisers.objects.filter(is_available=True)
    users = User.objects.filter(is_adviser=True)
    user = get_user_model().objects.get(email=request.user.email)

    if request.method == 'POST':
        form = ContributorForm(request.POST, request.FILES, instance=user.contributor_profile)
        if form.is_valid():
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
        if user.contributor_profile is None:
            context = {
                'contributorForm': ContributorForm(), 'degrees': degrees, 'advisers': advisers, 'users': users
            }
        else:
            contributor = ContributorProfile.objects.get(id=user.contributor_profile.id)
            context = {
                'contributorForm': ContributorForm(instance=contributor), 'contributor': contributor,
                'degrees': degrees, 'advisers': advisers, 'users': users
            }

    return render(request, 'application.html', context)


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
            return HttpResponseRedirect(reverse('myrelevate:contributor:update'))
        else:
            return HttpResponse(form.errors)
    else:
        user = get_user_model().objects.get(email=request.user.email)
        profile = user.get_contributor_profile()
        topics = Topics.objects.all()
        degrees = Degree.objects.all()
        context = {
            'contributorProfile': profile,
            'topics': topics,
            'degrees': degrees,
            'contributorForm': ContributorForm(instance=profile),
            'programForm': ProgramForm(instance=profile),
            'biographyForm': BiographyForm(instance=profile),
            'interestForm': InterestForm(instance=profile),
            'contactForm': ContactForm(instance=profile),
            'avatarForm': AvatarForm(instance=profile),
            'resumeForm': CVResumeForm(instance=profile)
        }
    return render(request, 'contributorprofile.html', context)


@login_required()
def update_degree(request):
    """
    Update the contributors completed degree field
    :param request:
    :return: Redirect to contributor profile with updated degree field
    """
    if request.method == 'POST':
        form = DegreeForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid:
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def update_area_of_expertise(request):
    """
    Update the contributors area of expertise field
    :param request:
    :return: Redirect to contributor profile with updated area of expertise field
    """
    if request.method == 'POST':
        form = AreaOfExpertiseForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid:
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def update_biography(request):
    """
    Update the contributors biography text area field
    :param request:
    :return: Redirect to contributor profile with updated biography field
    """
    if request.method == 'POST':
        form = BiographyForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid:
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def update_interest(request):
    """
    Update the contributors text area interest description
    :param request:
    :return: Redirect to contributor profile with updated interest field
    """
    if request.method == 'POST':
        form = InterestForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid:
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def update_contact(request):
    """
    Update the contributors contact information
    :param request:
    :return: Redirect to contributor profile with updated contact information
    """
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid:
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def update_program(request):
    """
    Update the contributors program of study
    :param request:
    :return: Redirect to contributor profile with updated program of study
    """
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse(form.errors)
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def update_avatar(request):
    """
    Update the contributors profile picture
    :param request:
    :return: Redirect to contributor profile with updated profile picture
    """
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=request.user.contributor_profile)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse(form.errors)
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def update_cv_resume(request):
    """
    Update the uploaded cv/resume for a contributor
    :param request:
    :return: Redirect to contributor profile with updated cv/resume
    """
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
    approve_form_set = modelformset_factory(User, form=ApprovalUpdateUserForm, extra=0)
    user_adviser_ids = Advisers.objects.values_list('id', flat=True)
    user_advisers = User.objects.filter(adviser_profile=user_adviser_ids)

    for user in users:
        if user.is_contributor:
            PendingContributors.objects.filter(contributor_id=user.contributor_profile).delete()

    if request.method == 'POST':
        formset = approve_form_set(request.POST, queryset=users)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('myrelevate:contributor:approve'))
        else:
            return HttpResponse(formset.errors)
    else:
        formset = approve_form_set(queryset=users)
        context = {
            'profiles': contributor_profiles,
            'users_forms': zip(users, formset),
            'formset': formset,
            'user_advisers': user_advisers,
        }
    return render(request, 'approval.html', context)


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
