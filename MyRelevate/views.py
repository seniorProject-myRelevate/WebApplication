import os

import sendgrid
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

from .Contributor.forms import ContributorForm
from .forms import RegistrationForm, LoginForm, SubscribeForm
from MyRelevate.models import User
from MyRelevate.serializers import UserSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
            return JsonResponse(status=406, data={'message': t['email'][0]})
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

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


#pattern for request is http://www.myrelevate.com/user/<email>/
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, email):
    """
    Retrieve, update or delete a USER.
    """
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)