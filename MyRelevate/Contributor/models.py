from django.db import models
from ..models import User


class ContributorProfile(models.Model):
    class Meta:
        db_table = 'contributor_profile'
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
    credential = models.CharField(max_length=5, choices=DEGREES)
    adviser_email = models.EmailField(max_length=254, unique=False, null=False, blank=False)
    adviser_first_name = models.CharField(max_length=255, null=False, blank=False)
    adviser_last_name = models.CharField(max_length=255, null=False, blank=False)
    institution = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False)
    city = models.CharField(max_length=255, null=False, blank=False)
    state = models.CharField(max_length=255, null=False, blank=False)
    zipcode = models.CharField(max_length=5, null=False, blank=False)
    program = models.CharField(max_length=255, null=False, blank=False)
    biography = models.TextField(null=False, blank=False)
    # research and clinical interests
    interests = models.TextField(null=True, blank=True)
    # profile_image = models.ImageField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    cv = models.FileField(upload_to='user_profiles/cv', null=True, blank=True)
    accept_terms = models.BooleanField(default=False)
    expertise_topics = models.ManyToManyField('MyRelevate.Topics')
    adviser = models.ForeignKey('MyRelevate.Advisers')


class Pending(models.Model):
    class Meta:
        db_table = 'pending_contributors'
    user = models.ForeignKey(User, null=True, blank=True)


class Denied(models.Model):
    class Meta:
        db_table = 'denied_contributors'
    contributor = models.ForeignKey(ContributorProfile, null=True, blank=True)
    reason1 = models.TextField(null=False, blank=False)
    reason2 = models.TextField(null=False, blank=False)
    reason3 = models.TextField(null=False, blank=False)
    reason4 = models.TextField(null=False, blank=False)
    reason5 = models.TextField(null=False, blank=False)
