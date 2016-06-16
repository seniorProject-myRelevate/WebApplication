from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model

from .models import Article


class ArticleForm(forms.ModelForm):
    # title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}))

    class Meta:
        model = Article
        fields = ['title', 'content', 'isPublished']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'content': forms.Textarea(),
            }

    def save(self, commit=True, email=None):
        article = super(ArticleForm, self).save(commit=False)
        if commit:
            article.contributor_id = get_user_model().objects.get(email=email).contributor_profile.pk
            if article.isPublished:
                article.publishDate = datetime.now()
            article.save()
            return article
