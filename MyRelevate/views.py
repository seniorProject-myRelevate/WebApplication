from django.shortcuts import render
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .forms import RegistrationForm, LoginForm
from .models import User
from django.contrib.auth import authenticate, login


def index(request):
    pass
    return render(request, 'index.html')


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


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                HttpResponse('%s is logged in.' % email)
            else:
                HttpResponse('%s\'s account is deactivated.')
        else:
            HttpResponse('Invalid Login.')
    else:
        form = LoginForm()
        return render(request, 'index.html', {'form': form})
