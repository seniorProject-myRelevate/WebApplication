import os

import sendgrid
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

from .forms import RegistrationForm, LoginForm, ContributorForm, SubscribeForm


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
    if request.method == 'POST':
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
        # contributors = get_user_model().objects.exclude(contributorProfile__isnull=True)
        contributorForm = ContributorForm()
    return render(request, 'contributors.html', {'contributors': contributors, 'contributorForm': contributorForm})


def contributor_profile(request):
    #contributor =
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
    if request.is_ajax() and request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            send_email('Thank you for subscribing', '5642c87f-4552-4a00-8b95-f17857ae9e88', dict, form.cleaned_data['email'],)
            return JsonResponse(status=200, data={})
        else:
            t = dict(form.errors.items())
            return JsonResponse(data={'email_errs': t['email'][0]}, status=400)
    elif request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
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
def send_template(toEmail, fromEmail, subject, templateID, substitution):
    client = sendgrid.SendGridClient(os.environ['SendGridApiKey'])
    message = sendgrid.Mail()
    message.set_subject('App Recieved')
    message.set_html('Body')
    message.set_text('Body')
    message.add_substitution('Body', '')
    message.set_from("noreply@myrelevate.com")
    message.add_to("lbreck93@gmail.com")
    message.add_filter('templates', 'enable', 1)
    message.add_filter('templates', 'template_id', 'c08e86d4-00ac-4513-b53e-68ec373ef3d9')

    print client.send(message)


def send_email(subject, template_id, substitution, to_email):
    client = sendgrid.SendGridClient(os.environ['SendGridApiKey'])
    message = sendgrid.Mail()
    message.set_subject(subject)
    message.set_from('noreply@myrelevate.com')
    message.add_to(to_email)
    if template_id:
        message.set_html('Body')
        message.set_text('Body')
        message.add_substitution('Body', '')
        message.add_filter('templates', 'enable', 1)
        message.add_filter('templates', 'template_id', template_id)

    print client.send(message)


def get_unsubscribes():
    client = sendgrid.SendGridClient(os.environ['SendGridApiKey'])
    l = sendgrid.SendGridAPIClient(apikey=os.environ['SendGridApiKey']).suppressions
    print l.get()
