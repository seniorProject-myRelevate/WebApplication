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
