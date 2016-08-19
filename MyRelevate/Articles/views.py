from django.contrib import messages
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse

from forms import ArticleForm, ArticleTopicForm
from models import Article
from .models import Topics


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
            article = form.save(commit=False)
            article.contributor_id = get_user_model().objects.get(email=request.user.email).contributor_profile.pk
            if article.isPublished:
                article.publishDate = datetime.now()
                article.save()
                form.save_m2m()
            # messages.SUCCESS(request, 'Article posted!')
            return HttpResponseRedirect(reverse('myrelevate:articles:create'))
        else:
            return HttpResponse(form.errors)
            # messages.ERROR(request, form.errors)
    else:
        topics = Topics.objects.all()
    return render(request, 'articles.html', {'form': ArticleForm(), 'topics': topics})


@login_required()
def articleTopics(request):
    if request.method == 'POST':
        form = ArticleTopicForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:article:create'))


@login_required()
def update(request):
    pass


@login_required()
def remove(request):
    pass


def get(request):
    pass
