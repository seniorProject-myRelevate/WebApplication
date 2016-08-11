from django.db import models


class Advisers(models.Model):
    class Meta:
        db_table = 'advisers'
    accept_terms = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)


class PendingAdvisers(models.Model):
    class Meta:
        db_table = 'pending_advisers'
    adviser = models.ForeignKey(Advisers)


class DeniedAdvisers(models.Model):
    class Meta:
        db_table = 'denied_advisers'
    adviser = models.ForeignKey(Advisers)
    reason = models.TextField(null=False, blank=False)
    denied = models.BooleanField(default=False)
