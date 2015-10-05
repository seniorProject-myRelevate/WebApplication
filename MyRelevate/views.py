from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout

from .forms import RegistrationForm, LoginForm
from .models import UserProfile
from django.contrib.auth import authenticate, login


def index(request):
    if request.method == 'POST':
        login_view(request)
    else:
        form = LoginForm()
        return render(request, 'index.html', {'form': form})


def register_user(request):
    pass
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('MyRelevate:index'))
    else:
        form = RegistrationForm()
    return render(request, "register.html", {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('%s is logged in.' % username)
            else:
                return HttpResponse('%s\'s account is deactivated.')
        else:
            return HttpResponse('Invalid Login.')
    else:
        form = LoginForm()
        return render(request, 'index.html', {'form': form})


def logout_view(request):
    logout(request)
    HttpResponseRedirect(reverse('myrelevate:index'))
