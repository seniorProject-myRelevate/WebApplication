from datetime import datetime

from django.db import models

from ..Contributor.models import ContributorProfile
from ..models import Topics


class Article(models.Model):
    class Meta:
        db_table = 'article'
    contributor = models.ForeignKey(ContributorProfile, on_delete=models.CASCADE)
    article_topics = models.ManyToManyField(Topics)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=400)
    isPublished = models.BooleanField(default=False)
    createdDate = models.DateField(default=datetime.now)
    publishDate = models.DateField(null=True, blank=True)
    updateDate = models.DateField(default=datetime.now)
