from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import RegistrationForm, LoginForm, ConfirmationForm
from ..Contributor.forms import ContributorForm
from ..User.models import User

from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context


def register_user(request):
    """
    Allows new users to register for an account if they aren't authenticated and their for is valid.
    Logs user in after account is created.
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

            user_name = form.instance.first_name + form.instance.last_name
            user_email = form.instance.email

            user = User.objects.get(email=user_email)
            code = user.get_confirmation_token()

            template = get_template('confirmation.html')
            context = Context({
                'userName': user_name,
                'email': user_email,
                'code': code,
            })
            content = template.render(context)

            email = EmailMessage(
                "Confirm Your Account with MyRelevate",
                content,
                "relevate@gmail.com" + '',
                [user_email],
                headers={'Reply-To': "relevate@gmail.com"}
            )
            email.send()

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


@login_required()
def new_confirm(request):
    """
    renders page so user can confirm their account.
    :param request:
    :return:
    """
    user = get_user_model().objects.get(email=request.user.email)
    new_token = user.generate_confirmation_token()
    if request.user.confirmed:
        return HttpResponseRedirect(reverse('myrelevate:index'))
    if request.method == 'POST':
        token = request.POST['token']
        user = get_user_model().objects.get(email=request.user.email)
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            if user.confirm(token):
                messages.success(request, 'Thank you for confirming your account!')
                return HttpResponseRedirect(reverse('myrelevate:index'))
            else:
                # email code for new confirmation token
                pass
        else:
            return HttpResponse(form.errors)
    else:
        context = {
            'user': request.user,
            'form': ConfirmationForm(),
            'token': new_token,
        }
    return render(request, 'confirm.html', {'user': request.user, 'form': ConfirmationForm, 'token': new_token})


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
