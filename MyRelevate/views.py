import os

import sendgrid
from django.http import JsonResponse
from django.shortcuts import render

from .forms import SubscribeForm


def index(request):
    """
    index method-- the first page a user will see after our landing page. allows users to login, thats pretty much it.
                    if there is an error on this page it's probably for testing
    :param request: shouldnt need to mess with this
    :return: renders a given html page, with the given data in the context dictionary below
    """
    return render(request, 'index.html', {'user': request.user})


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
            # send_email('Thank you for subscribing', '5642c87f-4552-4a00-8b95-f17857ae9e88', dict,
            #           form.cleaned_data['email'])
            return JsonResponse(status=200, data={'message': 'Thank you for subscribing!'})
        else:
            t = dict(form.errors.items())
            return JsonResponse(status=406, data={'message': t['email'][0]})
    elif request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        return render(request, 'subscribe.html', {'subscribeForm': SubscribeForm()})


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
