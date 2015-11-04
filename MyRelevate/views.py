from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm, ContributorRequestForm
from .models import UserProfile, ContributorProfile


def index(request):
    if request.method == 'POST':
        login_view(request)
    else:
        return render(request, 'index.html', {'user': request.user})


def register_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('myrelevate:index'))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, authenticate(username=request.POST['username'], password=request.POST['password1']))
            return HttpResponseRedirect(reverse('myrelevate:index'))
    else:
        pass
    return render(request, "register.html", {'form': RegistrationForm(), 'contribForm': ContributorRequestForm()})


def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('myrelevate:index'))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('myrelevate:index'))
            else:
                return HttpResponse('%s\'s account is deactivated.')
        else:
            return HttpResponse('Invalid Login.')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('myrelevate:index'))


def contributors(request):
    if request.method == 'POST':
        form = ContributorRequestForm(request.POST, request.FILES)
        if form.is_valid():
            contributor_profile = ContributorProfile(cv=request.FILES['cv'])
            user = UserProfile.objects.get(user=request.user)
            contributor_profile.save()
            user.contributorProfile = contributor_profile
            user.save()
            form.save()
            return HttpResponseRedirect(reverse('myrelevate:index'))
        else:
            return HttpResponse(form.errors)
    else:
        contributors = UserProfile.objects.exclude(contributorProfile__isnull=True)
        contribForm = ContributorRequestForm()
    return render(request, 'contributors.html', {'contributors': contributors, 'contribForm': contribForm})


def user_profile(request):
    profile = UserProfile.objects.all()
    return render(request, 'userprofile.html', {'profile': profile})
