from django.db import models


class ContributorProfile(models.Model):
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

    accept_terms = models.BooleanField(default=False)
    address = models.CharField(max_length=255, null=False, blank=False)
    adviser_email = models.EmailField(max_length=254, unique=False, null=False, blank=False)
    adviser_first_name = models.CharField(max_length=255, null=False, blank=False)
    adviser_last_name = models.CharField(max_length=255, null=False, blank=False)
    biography = models.CharField(max_length=255, null=False, blank=False)
    credential = models.CharField(max_length=5, choices=DEGREES)
    cv = models.FileField(upload_to='user_profiles/cv', null=True, blank=True)
    institution = models.CharField(max_length=255, null=False, blank=False)
    # research and clinical interests
    interests = models.CharField(max_length=255, null=True, blank=True)
    # profile_image = models.py.ImageField(null=True, blank=True)
    program = models.CharField(max_length=255, null=False, blank=False)
    website_url = models.URLField(null=True, blank=True)