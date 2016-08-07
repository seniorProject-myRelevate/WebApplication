from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render


def index(request):
    if not request.user.is_contributor:
        return HttpResponseRedirect(reverse('myrelevate:index'))
    return render(request, 'index.html', {'form': None})


def advisers(request):
    pass


def approve(request):
    pass


def create(request):
    pass


def update(request):
    pass
