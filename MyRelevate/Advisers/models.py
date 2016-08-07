from django.db import models
from ..models import User


class Advisers(models.Model):
    class Meta:
        db_table = 'advisers'
    userAdviser = models.ForeignKey(User, null=True, blank=True)
    accept_terms = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)


class AvailableAdvisers(models.Model):
    class Meta:
        db_table = 'available_advisers'
    adviser = models.ForeignKey(Advisers)
