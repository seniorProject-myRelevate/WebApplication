from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from models import Advisers


def index(request):
    if not request.user.is_contributor:
        return HttpResponseRedirect(reverse('myrelevate:index'))
    return render(request, 'index.html', {'form': None})


@login_required()
def advisers(request):
    return render(request, 'advisers.html')


@login_required()
def approve(request):
    pass


@login_required()
def create(request):
    pass


@login_required()
def update(request):
    pass
