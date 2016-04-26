from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class ConfirmedMiddleware(object):
    def process_request(self, request):
        """
        makes user confirm their account if they have not done so.
        checks if user is authenticated, not confirmed, and if they arent confirming, it redirects them so they will.
        Confirming the user email must be done before the user may use the site.
        :param request:
        :return:
        """
        if request.user.is_authenticated() and not request.user.confirmed and \
                (request.path != reverse('myrelevate:auth:new_confirm') and
                         request.path != reverse('myrelevate:auth:confirm')):
            return HttpResponseRedirect(reverse('myrelevate:auth:new_confirm'))
