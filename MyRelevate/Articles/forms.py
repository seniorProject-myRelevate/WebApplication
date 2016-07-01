from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model

from .models import Article
# from ..models import Topics


class ArticleForm(forms.ModelForm):
    # article_topics = forms.ModelMultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple(), label='',
    #                                                 queryset=Topics.objects.all().values_list('topicName', flat=True))

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
