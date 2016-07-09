from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import ContributorForm, CredentialForm, AreaOfExpertiseForm, BiographyForm, InterestForm, ContactForm, \
    ApprovalContributorForm, ApprovalUpdateUserForm

from ..models import Topics
from .models import ContributorProfile


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
    if request.method == 'POST':
        form = ContributorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(email=request.user.email)
            return HttpResponseRedirect(reverse('myrelevate:index'))
        else:
            return HttpResponse(form.errors)
    else:
        contributorForm = ContributorForm()
    return render(request, 'application.html', {'contributorForm': contributorForm})


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
            form.save(email=request.user.email)

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
                                                       'expertiseForm': AreaOfExpertiseForm(instance=profile),
                                                       'biographyForm': BiographyForm(instance=profile),
                                                       'interestForm': InterestForm(instance=profile),
                                                       'contactForm': ContactForm(instance=profile)})


@login_required()
def updateCredentials(request):
    if request.method == 'POST':
        form = CredentialForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid:
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def updateAreaOfExpertise(request):
    if request.method == 'POST':
        form = AreaOfExpertiseForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid:
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def updateBiography(request):
    if request.method == 'POST':
        form = BiographyForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid:
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def updateInterest(request):
    if request.method == 'POST':
        form = InterestForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid:
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def updateContact(request):
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
def approve(request,id):
    user = get_user_model().objects.get(email=id)
    if request.method == 'POST':
        form = ApprovalContributorForm(request.POST, request.FILES, instance=user.contributor_profile)
        form2 = ApprovalUpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save(email=request.user.email)
            return HttpResponseRedirect(reverse('myrelevate:contributor_profile'))
        else:
            return HttpResponse(form.errors)
    else:
        user = get_user_model().objects.get(email=id)
        profile = user.get_contributor_profile()
    return render(request, 'approvalcontributorprofile.html', {'contributorProfile': profile,
                                                       'approvalContributorForm': ApprovalContributorForm(instance=profile),
                                                       'approvalUpdateUserForm': ApprovalUpdateUserForm(instance=profile),
                                                               })


