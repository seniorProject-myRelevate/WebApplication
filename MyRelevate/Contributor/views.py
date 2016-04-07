import os

import sendgrid
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

from .forms import ContributorForm


# @login_required()
# def Articles(request):
#     if not request.user.is_contributor:
#         return HttpResponseRedirect(reverse('myrelevate:index'))
#     if request.method == 'POST':
#         form = ArticleForm(request.POST)
#         if form.is_valid():
#             form.save(email=request.user.email)
#             messages.success(request, 'Article Posted!')
#         else:
#             messages.ERROR(request, 'Article NOT posted!')
#     return render(request, 'Articles.html', {'form': ArticleForm()})

def index(request):
    if not request.user.is_contributor:
        return HttpResponseRedirect(reverse('myrelevate:index'))
    return render(request, 'articles.html', {'form': None})


@login_required()
def create(request):
    pass


@login_required()
def update(request):
    pass


@login_required()
def remove(request):
    pass

def contributors(request):
    """
    jeremy plz document
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = ContributorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(email=request.user.email)
            # profile = ContributorProfile(cv=request.FILES['cv'])
            # user.contributor_profile = profile
            # profile.save()
            # user.save()
            return HttpResponseRedirect(reverse('myrelevate:index'))
        else:
            return HttpResponse(form.errors)
    else:
        # contributors = get_user_model().objects.exclude(contributorProfile__isnull=True)
        contributorForm = ContributorForm()
    return render(request, 'contributors.html', {'contributors': contributors, 'contributorForm': contributorForm})


def contributor_profile(request):
    """
    jeremy plz document
    :param request:
    :return:
    """
    if request.method == 'POST':
        user = get_user_model().objects.get(email=request.user.email)
        form = ContributorForm(request.POST, request.FILES, instance=user.contributor_profile)
        if form.is_valid():
            # profile = ContributorProfile(cv=request.FILES['cv'])
            form.save(email=request.user.email)
            # return HttpResponseRedirect(reverse('myrelevate:index'))
            return HttpResponseRedirect(reverse('myrelevate:contributor_profile'))
        else:
            return HttpResponse(form.errors)
    else:
        user = get_user_model().objects.get(email=request.user.email)
        profile = user.get_contributor_profile()
    return render(request, 'contributorprofile.html', {'contributorProfile': profile,
                                                       'contributorForm':
                                                           ContributorForm(instance=user.contributor_profile)})