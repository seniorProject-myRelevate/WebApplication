from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.forms import modelformset_factory

from .forms import AdviserApplicationForm, ApproveAdviserForm, UpdateAvailableForm

from models import Advisers, PendingAdvisers
from ..models import ContributorProfile
from ..models import User


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
    pending_adviser_ids = PendingAdvisers.objects.values_list('adviser_id', flat=True)
    users = User.objects.filter(id__in=pending_adviser_ids)
    approve_form_set = modelformset_factory(User, form=ApproveAdviserForm, extra=0)
    if request.method == 'POST':
        formset = approve_form_set(request.POST, queryset=users)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('myrelevate:advisers:approve'))
        else:
            return HttpResponse(formset.errors)
    else:
        formset = approve_form_set(queryset=users)
    return render(request, 'approve_adviser.html', {'user_forms': zip(users, formset), 'formset': formset})


@login_required()
def create(request):
    if request.method == 'POST':
        form = AdviserApplicationForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=request.user.email)
            pending = PendingAdvisers()
            adviser = form.save()
            user.adviser_profile = adviser
            pending.adviser = adviser
            pending.save()
            user.save()
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
