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
    """
    index method-- the first page a user will see after our landing page. allows users to login, thats pretty much it.
                    if there is an error on this page it's probably for testing
    :param request: shouldnt need to mess with this
    :return: renders a given html page, with the given data in the context dictionary below
    """
    if request.method == 'POST':
        login_view(request)
    else:
        return render(request, 'index.html', {'user': request.user})


def register_user(request):
    """
    Allows new users to register for an account if they aren't authenticated and their for is valid.
    Logs user in after accont is created.
    :param request:
    :return: returns a new page, or redirects user to index page.
    """
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
    """
    allows user to login if they arent authenticated.
    :param request:
    :return: renders login page or redirects user to index page
    """
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
    """
    logs user out, this is basically the default django method, see their documentation for any questions.
    :param request:
    :return: redirects user to index page
    """
    logout(request)
    messages.success(request, 'You have logged out.')
    return HttpResponseRedirect(reverse('myrelevate:index'))


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


@login_required
def application(request):
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
    return render(request, 'application.html', {'contributors': contributors, 'contributorForm': contributorForm})



def contributor_profile(request):
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
    """
    really just a test page. it isnt really anything yet.
    :param request:
    :return:
    """
    profile = get_user_model().objects.all()
    return render(request, 'userprofile.html', {'profile': profile})


def subscribe(request):
    """
    allows non-users to subscribe for email updates, regular users are already subscribed.
    :param request:
    :return: returns json data, or renders the subscribe page.
    """
    if request.is_ajax() and request.method == 'POST' and request.user.is_anonymous():
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            send_email('Thank you for subscribing', '5642c87f-4552-4a00-8b95-f17857ae9e88', dict,
                       form.cleaned_data['email'],)
            return JsonResponse(status=200, data={'message': 'Thank you for subscribing'})
        else:
            t = dict(form.errors.items())
            return JsonResponse(status=400, data={'message': t['email'][0]})
    elif request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        return render(request, 'subscribe.html', {'subscribeForm': SubscribeForm()})


@login_required()
def new_confirm(request):
    """
    renders page so user can confirm their account.
    :param request:
    :return:
    """
    if request.user.confirmed:
        return HttpResponseRedirect(reverse('myrelevate:index'))
    return render(request, 'confirm.html', {'user': request.user})


@login_required()
def confirm(request):
    """
    confirms user account. (can combine this with the 'new_confirm' functionality later.
    :param request:
    :return: redirects to index page.
    """
    if request.user.confirmed:
        return HttpResponseRedirect(reverse('myrelevate:index'))
    else:
        get_user_model().objects.get(email=request.user.email).new_confirm()
        messages.success(request, 'Thank you for confirming your account!')
        return HttpResponseRedirect(reverse('myrelevate:index'))


# Below are helper functions that are not associated with any particular route
def send_email(subject, template_id, substitution, to_email):
    """
    sends email via sendgrid's awesome API. See their documentation for questions.
    :param subject: subject line of would-be email
    :param template_id: template id of would-be email
    :param substitution: subsitution tags of the given template
    :param to_email: place where email is to be sent
    :return: None,
    """
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

    client.send(message)


def get_unsubscribes():
    """
    i was testing sendgrids email unsubscribe button, dont pay attention to this.
    :return:
    """
    client = sendgrid.SendGridClient(os.environ['SendGridApiKey'])
    l = sendgrid.SendGridAPIClient(apikey=os.environ['SendGridApiKey']).suppressions
    print l.get()
