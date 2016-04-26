from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from forms import ArticleForm
from models import Article


def index(request):
    if not request.user.is_contributor:
        return HttpResponseRedirect(reverse('myrelevate:index'))
    return render(request, 'articles.html',
                  {'articles': Article.objects.filter(contributor_id=request.user.contributor_profile.pk)})


@login_required()
def create(request):
    if not request.user.is_contributor:
        return HttpResponseRedirect(reverse('myelevate:index'))
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save(email=request.user.email)
            # messages.SUCCESS(request, 'Article posted!')
        else:
            messages.ERROR(request, form.errors)
    return render(request, 'articles.html', {'form': ArticleForm()})


@login_required()
def update(request):
    pass


@login_required()
def remove(request):
    pass


def get(request):
    pass
