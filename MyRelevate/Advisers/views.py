from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import AdviserApplicationForm, UpdateAvailableForm

from models import Advisers


def index(request):
    if not request.user.is_contributor:
        return HttpResponseRedirect(reverse('myrelevate:index'))
    return render(request, 'index.html', {'form': None})


@login_required()
def advisers(request):
    advisers = Advisers.objects.all()
    return render(request, 'advisers.html')


@login_required()
def approve(request):
    pass


@login_required()
def create(request):
    if request.method == 'POST':
        form = AdviserApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myrelevate:index'))
        else:
            return HttpResponse(form.errors)
    else:
        adviser_form = AdviserApplicationForm()
    return render(request, 'adviser_application.html', {'adviser_form': adviser_form})


@login_required()
def update(request):
    if request.method == 'POST':
        form = UpdateAvailableForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            pass
    return HttpResponseRedirect(reverse('myrelevate:advisers:update'))
