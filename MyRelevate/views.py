import os

import sendgrid
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import RegistrationForm, LoginForm, ContributorForm, SubscribeForm
from .models import ContributorProfile, Subscriber
from django.contrib.auth import get_user_model


def index(request):
    if request.method == 'POST':
        login_view(request)
    else:
        confirmed = None
        if request.user.is_authenticated():
            user = get_user_model().objects.get(email=request.user.email)
            if not user.confirmed:
                confirmed = user.generate_confirmation_token()
        return render(request, 'index.html', {'user': request.user, 'token': confirmed})


def register_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('myrelevate:index'))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, authenticate(email=request.POST['email'], password=request.POST['password1']))
            return HttpResponseRedirect(reverse('myrelevate:index'))
    else:
        pass
    return render(request, "register.html", {'form': RegistrationForm(), 'contribForm': ContributorForm()})


def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('myrelevate:index'))
    if request.method == 'POST':
        username = request.POST['email']
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
        # user = get_user_model().objects.get(email=request.user.email)
        # form = ContributorForm(request.POST, request.FILES, instance=user.contributor_profile)
        form = ContributorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(email=request.user.email)
            # profile = ContributorProfile(cv=request.FILES['cv'])
            # user.contributor_profile = profile
            # profile.save()
            # user.save()
            return HttpResponseRedirect(reverse('myrelevate:index'))
        else:
            return HttpResponse(form.errors)
    else:
        pass
    return render(request, 'contributors.html', {'contributors': contributors, 'contributorForm': ContributorForm()})


def contributor_profile(request):
    if request.method == 'POST':
        user = get_user_model().objects.get(email=request.user.email)
        form = ContributorForm(request.POST, request.FILES, instance=user.contributor_profile)
        if form.is_valid():
            # profile = ContributorProfile(cv=request.FILES['cv'])
            form.save(email=request.user.email)
            # return HttpResponseRedirect(reverse('myrelevate:index'))
            return HttpResponseRedirect(reverse('myrelevate:contributor_profile'))
        else:
            return HttpResponse(form.errors)
    else:
        user = get_user_model().objects.get(email=request.user.email)
        profile = user.get_contributor_profile()
    return render(request, 'contributorprofile.html', {'contributorProfile': profile,
                                                       'contributorForm':
                                                           ContributorForm(instance=user.contributor_profile)})


def user_profile(request):
    profile = get_user_model().objects.all()
    return render(request, 'userprofile.html', {'profile': profile})


def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            Subscriber.objects.get(email=request.POST[''])
            print request.POST
            form.save()
        else:
            print form.errors
        return render(request, 'subscribe.html', {'subscribeForm': SubscribeForm()})
    else:
        return render(request, 'subscribe.html', {'subscribeForm': SubscribeForm()})


@login_required()
def confirm(request, token=None):
    user = get_user_model().objects.get(user=request.user)
    if user.confirmed:
        return HttpResponseRedirect(reverse('myrelevate:index'))
    if user.confirm(token):
        return HttpResponse("thank you for confirming your account")
    else:
        return HttpResponse("something went wrong")


# Below are helper functions that are not associated with any particular route
def send_email():
    client = sendgrid.SendGridClient(os.environ['SendGridApiKey'])
    message = sendgrid.Mail()

    message.add_to("lbreck93@gmail.com")
    message.set_from("noreply@myrelevate.com")
    message.set_subject("Test email from MyRelevate")
    message.set_html("Using sendgrid we are able to send you emails... pretty cool eh?")

    client.send(message)
