from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import RegistrationForm, LoginForm, ContributorRequestForm, SubscribeForm
from .models import ContributorProfile, Subscriber


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

            user = get_user_model().objects.get(email=request.POST['email'])
            token = user.generate_confirmation_token()
            url = request.build_absolute_uri(reverse('myrelevate:confirm', kwargs={'token': token}))
            user.send_email('Please Confirm Your Account', 'Click <a href="%s">here</a> to confirm your account' % url)

            login(request, authenticate(username=request.POST['email'], password=request.POST['password1']))
            return HttpResponseRedirect(reverse('myrelevate:index'))
    return render(request, "register.html", {'form': RegistrationForm(), 'contribForm': ContributorRequestForm()})


def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('myrelevate:index'))
    if request.method == 'POST' and LoginForm(request.POST).is_valid():
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
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

@login_required
def contributors(request):
    if request.method == 'POST':
        form = ContributorRequestForm(request.POST, request.FILES)
        if form.is_valid():
            contributor_profile = ContributorProfile(cv=request.FILES['cv'])
            user = get_user_model().objects.get(email=request.email)
            contributor_profile.save()
            form.save()
            return HttpResponseRedirect(reverse('myrelevate:index'))
        else:
            return HttpResponse(form.errors)
    else:
        contributors = get_user_model().objects.exclude(contributorProfile__isnull=True)
        contribForm = ContributorRequestForm()
    return render(request, 'contributors.html', {'contributors': contributors, 'contribForm': contribForm})


def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            print request.POST['email']
            form.save()
        else:
            print form.errors
        return render(request, 'subscribe.html', {'subscribeForm': SubscribeForm()})
    else:
        return render(request, 'subscribe.html', {'subscribeForm': SubscribeForm()})


@login_required()
def confirm(request, token=None):
    user = get_user_model().objects.get(email=request.user.email)
    if user.confirmed:
        return HttpResponseRedirect(reverse('myrelevate:index'))
    if user.confirm(token):
        return HttpResponse("thank you for confirming your account")
    else:
        return HttpResponse("something went wrong")
