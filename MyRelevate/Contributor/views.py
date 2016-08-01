from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.forms import modelformset_factory

from .forms import ContributorForm, CredentialForm, AreaOfExpertiseForm, BiographyForm, InterestForm, ContactForm, \
    ApprovalUpdateUserForm

from ..models import Topics, Pending
from models import ContributorProfile
from ..models import User


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
    # available_advisers_ids = AvailableAdvisers.objects.values_list('adviser_id', flat=True)
    # available_advisers = User.objects.filter(id__in=available_advisers_ids)
    # adviser_ids = Advisers.objects.values_list('userAdviser_id', flat=True)
    if request.method == 'POST':
        form = ContributorForm(request.POST, request.FILES)
        if form.is_valid():
            user = get_user_model().objects.get(email=request.user.email)
            pending = Pending()
            contributor_profile = form.save()
            user.contributor_profile = contributor_profile
            pending.user = user
            pending.save()
            user.save()
            return HttpResponseRedirect(reverse('myrelevate:index'))
        else:
            return HttpResponse(form.errors)
    else:
        contributor_form = ContributorForm()
    return render(request, 'application.html', {'contributorForm': contributor_form})


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
            # profile = ContributorProfile(cv=request.FILES['cv'])
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
                                                       'credenrialForm': CredentialForm(instance=profile),
                                                       'biographyForm': BiographyForm(instance=profile),
                                                       'interestForm': InterestForm(instance=profile),
                                                       'contactForm': ContactForm(instance=profile)})


@login_required()
def update_credentials(request):
    if request.method == 'POST':
        form = CredentialForm(request.POST, instance=request.user.contributor_profile)
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
def remove(request):
    pass


@login_required()
def show_resume(request):
    """
    Show the contributors cv/resume
    :param request:
    :return: The cv/resume
    """
    user = get_user_model().objects.get(email=request.user.email)
    profile = ContributorProfile.objects.get(id=user.contributor_profile.pk)
    file_path = profile.cv.path
    # with open(filepath, 'rb') as pdf:
    #     response = HttpResponse(pdf.read(), content_type='application/pdf')
    #     response['Content-Disposition'] = 'inline; filename="test_cv_resume_BYRIncf.pdf"'
    pdf_data = open(file_path, 'rb').read()
    return HttpResponse(pdf_data, content_type="application/pdf")


def contributors(request):
    """
    Displays list of all contributors.
    Allows a person to search contributors based on a set of given topics
    :param request:
    :return: The requested searched data
    """
    users = get_user_model().objects.all()
    contributor_profiles = get_user_model().objects.all()
    if request.method == 'GET':
        if 'q' in request.GET and request.GET['q']:
            q = request.GET['q']
            profiles = users.filter(first_name__icontains=q)
            return render(request, 'contributors.html', {'profiles': profiles, 'query': q})
        else:
            pass
    else:
        pass
    return render(request, 'contributors.html', {'contributors': contributor_profiles})


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
    pending_user_ids = Pending.objects.values_list('user_id', flat=True)
    profile_ids = User.objects.values_list('contributor_profile_id', flat=True)
    users = User.objects.filter(id__in=pending_user_ids)
    profiles = ContributorProfile.objects.filter(id__in=profile_ids)
    approve_form_set = modelformset_factory(User, form=ApprovalUpdateUserForm, extra=0)
    for user in users:
        if user.is_contributor:
            Pending.objects.filter(user_id=user.id).delete()
    if request.method == 'POST':
        formset = approve_form_set(request.POST, queryset=users)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('myrelevate:contributor:approve'))
        else:
            print formset.errors
    else:
        formset = approve_form_set(queryset=users)
    return render(request, 'approval.html', {'profiles': profiles, 'users_forms': zip(users, formset),
                                             'formset': formset})


@login_required()
def show_approve_cv_resume(request):
    """

    :param request:
    :return:
    """
    # check to see if i can trim the query down on User to only get contributor_profiles from pending users
    pending_user_ids = Pending.objects.values_list('user_id', flat=True)
    profile_ids = User.objects.values_list('contributor_profile_id', flat=True)
    users = User.objects.filter(id__in=pending_user_ids)
    profiles = ContributorProfile.objects.filter(id__in=profile_ids)
    file_paths = []
    for user in users:
        for profile in profiles:
            if user.contributor_profile_id == profile.id:
                file_paths.insert(profile.cv.path)
    file_data = {path: open(path, 'rp') for path in file_paths}
    return HttpResponse(file_data, content_type="application/pdf")
