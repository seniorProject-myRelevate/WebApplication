from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model

from .models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['title', 'content', 'isPublished']

        widgets = {
            'title': forms.Textarea(attrs={'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'placeholder': 'Article'}),
            }

    def save(self, commit=True, email=None):
        article = super(ArticleForm, self).save(commit=False)
        if commit:
            if article.isPublished:
                article.publishDate = datetime.now
            user = get_user_model().objects.get(email=email)
            user.contributor_profile.article_set.set(article)
            return article