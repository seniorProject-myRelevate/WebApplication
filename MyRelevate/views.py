import os

import sendgrid
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import RegistrationForm, LoginForm, ContributorForm, SubscribeForm
from .models import Subscriber


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
            login(request, authenticate(email=request.POST['email'], password=request.POST['password1']))
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect(reverse('myrelevate:index'))
        else:
            messages.error(request, 'Your account could not be created, please try again.')
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
    messages.success(request, 'You have logged out.')
    return HttpResponseRedirect(reverse('myrelevate:index'))


def contributors(request):
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

    # if request.method == 'POST':
    #    form = ContributorForm(request.POST, request.FILES)
    #    if form.is_valid():
    #        form.save(email=request.user.email)
            # profile = ContributorProfile(cv=request.FILES['cv'])
            # user.contributor_profile = profile
            # profile.save()
            # user.save()
    #        return HttpResponseRedirect(reverse('myrelevate:index'))
    #    else:
    #        return HttpResponse(form.errors)
    #else:
      # contributors = get_user_model().objects.exclude(contributorProfile__isnull=True)
    #    contributors = get_user_model().objects.all()
    #    contributorForm = ContributorForm()
    #    if 'q' in request.GET and request.GET['q']:
    #        q = request.GET['q']
           # profiles = get_user_model().objects.filter(first_name__icontains=q)
    #        profiles = contributors.filter(first_name__icontains=q)
    #        return render(request, 'contributors.html', {'contributors': contributors, 'profiles': profiles, 'query': q,
    #                                                     'contributorForm': contributorForm})
    #return render(request, 'contributors.html', {'contributors': contributors, 'contributorForm': contributorForm})


def application(request):
    if request.method == 'POST':
        form = ContributorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(email=request.user.email)
            return HttpResponseRedirect(reverse('myrelevate:index'))
        else:
            return HttpResponse(form.errors)
    else:
        contributorForm = ContributorForm()
    return render(request, 'application.html', {'contributors': contributors, 'contributorForm': contributorForm})


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
def new_confirm(request):
    if request.user.confirmed:
        return HttpResponseRedirect(reverse('myrelevate:index'))
    return render(request, 'confirm.html', {'user': request.user})


@login_required()
def confirm(request):
    if request.user.confirmed:
        return HttpResponseRedirect(reverse('myrelevate:index'))
    else:
        get_user_model().objects.get(email=request.user.email).new_confirm()
        messages.success(request, 'Thank you for confirming your account!')
        return HttpResponseRedirect(reverse('myrelevate:index'))


# Below are helper functions that are not associated with any particular route
def send_email():
    client = sendgrid.SendGridClient(os.environ['SendGridApiKey'])
    message = sendgrid.Mail()

    message.add_to("lbreck93@gmail.com")
    message.set_from("noreply@myrelevate.com")
    message.set_subject("Test email from MyRelevate")
    message.set_html("Using sendgrid we are able to send you emails... pretty cool eh?")

    client.send(message)
