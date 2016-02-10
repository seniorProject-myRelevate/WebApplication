import os

import sendgrid
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
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
            # user_profile = UserProfile.objects.get(user=request.user)
            # token = user_profile.generate_confirmation_token()
            # url = request.build_absolute_uri(reverse('myrelevate:confirm', kwargs={'token': token}))
            # send_email('Please Confirm Your Account', 'Click <a href="%s">here</a> to confirm your account' % url)
            login(request, authenticate(username=request.POST['email'], password=request.POST['password1']))
            return HttpResponseRedirect(reverse('myrelevate:index'))
    else:
        pass
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
    user = UserProfile.objects.get(user=request.user)
    if user.confirmed:
        return HttpResponseRedirect(reverse('myrelevate:index'))
    if user.confirm(token):
        return HttpResponse("thank you for confirming your account")
    else:
        return HttpResponse("something went wrong")


# Below are helper functions that are not associated with any particular route
def send_email(subject="Test email from MyRelevate", html="Using sendgrid we are able to send you emails... pretty cool eh?"):
    client = sendgrid.SendGridClient(os.environ['SendGridApiKey'])
    message = sendgrid.Mail()

    message.add_to("lbreck93@gmail.com")
    message.set_from("noreply@myrelevate.com")
    message.set_subject(subject)
    message.set_html(html)

    client.send(message)
