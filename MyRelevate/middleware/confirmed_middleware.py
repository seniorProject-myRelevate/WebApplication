from django.http import HttpResponseRedirect, HttpResponse


class ConfirmedMiddleware(object):

    def process_request(self, request):
        if request.user.is_authenticated() and not request.user.confirmed:
            return HttpResponse("Middleware")