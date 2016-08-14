from django.db import models
from ..Advisers.models import Advisers


class ContributorProfile(models.Model):
    class Meta:
        db_table = 'contributorprofile'
    DEGREES = (
        ('-1', ''),
        ('MS', 'MS (Master of Science)'),
        ('MA', 'MA (Master of Arts)'),
        ('PhD', 'PhD (Doctor of Philosophy)'),
        ('PsyD', 'PsyD (Doctor of Psychology)'),
        ('SU', 'Student-Undergraduate'),
        ('SM', 'Student-Masters'),
        ('SPhD', 'Student-PhD'),
        ('SPsyD', 'Student-PsyD')
    )
    degree = models.CharField(max_length=5, choices=DEGREES)
    institution = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False)
    city = models.CharField(max_length=255, null=False, blank=False)
    state = models.CharField(max_length=255, null=False, blank=False)
    zipcode = models.CharField(max_length=5, null=False, blank=False)
    program = models.CharField(max_length=255, null=False, blank=False)
    biography = models.TextField(null=False, blank=False)
    interests = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='user_profiles/avatar', null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    cv = models.FileField(upload_to='user_profiles/cv', null=True, blank=True)
    accept_terms = models.BooleanField(default=False)
    expertise_topics = models.ManyToManyField('MyRelevate.Topics')
    has_adviser = models.BooleanField(default=False)
    adviser = models.ForeignKey(Advisers, null=True, blank=True)


class PendingContributors(models.Model):
    class Meta:
        db_table = 'pending_contributors'
    contributor = models.ForeignKey(ContributorProfile, null=True, blank=True)


class DeniedContributors(models.Model):
    class Meta:
        db_table = 'denied_contributors'
    contributor = models.ForeignKey(ContributorProfile, null=True, blank=True)
    reason = models.TextField(null=False, blank=False)
    denied = models.BooleanField(default=False)
