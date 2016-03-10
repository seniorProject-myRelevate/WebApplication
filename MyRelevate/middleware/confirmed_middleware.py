from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse


class ConfirmedMiddleware(object):

    def process_request(self, request):
        if request.user.is_authenticated() and not request.user.confirmed and\
                (request.path != reverse('myrelevate:new_confirm') and request.path != reverse('myrelevate:confirm')):
            return HttpResponseRedirect(reverse('myrelevate:new_confirm'))
