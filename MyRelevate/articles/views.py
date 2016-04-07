import os

import sendgrid
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

from forms import ArticleForm


def display(request):
    if not request.user.is_contributor:
        return HttpResponseRedirect(reverse('myrelevate:index'))
    return render(request, 'articles.html', {'form': ArticleForm()})


@login_required()
def create(request):
    pass


@login_required()
def update(request):
    pass


@login_required()
def remove(request):
    pass
