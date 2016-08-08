from django.db import models
from ..models import ContributorProfile


class Advisers(models.Model):
    class Meta:
        db_table = 'advisers'
    accept_terms = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)


class AdviserAdvisee(models.Model):
    class Meta:
        db_table = 'adviser_advisee'
    adviser = models.ForeignKey(Advisers)
    advisee = models.ForeignKey(ContributorProfile)


class PendingAdvisers(models.Model):
    class Meta:
        db_table = 'pending_advisers'
    adviser = models.ForeignKey(Advisers)
