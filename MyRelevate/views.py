from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm, ContributorRequestForm

from .models import UserProfile


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
        contribForm = ContributorRequestForm(request.POST, request.FILES)
        if form.is_valid():

            form.save()
            return HttpResponseRedirect(reverse('myrelevate:index'))
    else:
        form = RegistrationForm()
        contribForm = ContributorRequestForm()
    return render(request, "register.html", {'form': form, 'contribForm': contribForm})


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
    contributors = UserProfile.objects.exclude(contributorProfile__isnull='')
    return render(request, 'contributors.html', {'contributors': contributors})


def user_profile(request):
    profile = UserProfile.objects.all()
    return render(request, 'userprofile.html', {'profile': profile})
