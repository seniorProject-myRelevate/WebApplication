from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from SeniorProject import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import sendgrid
import os


class Subscriber(models.Model):
    email = models.EmailField(unique=True, null=False, blank=False)


# class Article(models.Model):
#     title = models.CharField(max_length=100)
#     content = models.TextField()  # check if this requires bounding for security purposes
#     publishDate = models.DateField()
#     updateDate = models.DateField()


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
    #user = models.OneToOneField(User, primary_key=True)
    #adviser = models.ForeignKey(Advisers, null=True, blank=True)
    credential = models.CharField(max_length=5, choices=DEGREES)
    program = models.CharField(max_length=255, null=False, blank=False)
    biography = models.CharField(max_length=255, null=False, blank=False)
    # research and clinical interests
    interests = models.CharField(max_length=255, null=True, blank=True)
    # profile_image = models.ImageField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    cv = models.FileField(upload_to='user_profiles/cv', null=True, blank=True)
    accept_terms = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    # articles = models.ForeignKey(Article, null=True, blank=True)


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser,
                          last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    is_staff = models.BooleanField(default=False)
    is_active = \
        models.BooleanField(default=True,
                            help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField(default=timezone.now)
    confirmed = models.BooleanField(default=False)
    is_contributor = models.BooleanField(default=False)
    contributor_profile = models.OneToOneField(ContributorProfile, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.email

    def get_contributor_profile(self):
        if self.is_contributor:
            return self.contributor_profile
        raise ValueError('User is not a contributor')

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(settings.SECRET_KEY, expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(settings.SECRET_KEY)
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        self.save()
        return True

    # Below are helper functions that are not associated with any particular route
    def send_email(self, subject, html, sender='noreply@myrelevate.com'):
        client = sendgrid.SendGridClient(os.environ['SendGridApiKey'])
        message = sendgrid.Mail()

        message.add_to(self.email)
        message.set_from(sender)
        message.set_subject(subject)
        message.set_html(html)

        client.send(message)


class Advisers(models.Model):
    #user = models.ForeignKey(ContributorProfile, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True, null=False, blank=False)
    #email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)


# DemographicData Database Model
# class DemographicData(models.Model):
#     EDUCATION = (
#         (-1, ''),
#         (0, 'Completed high school/GED'),
#         (1, 'Some college no longer attending'),
#         (2, 'Some college currently attending'),
#         (3, 'Graduated with bachelors'),
#         (4, 'Graduated with bachelors'),
#         (5, 'Graduated with PhD'),
#         (6, 'Did not complete high school'),
#     )
#
#     EMPLOYMENT_STATUS = (
#         (-1, ''),
#         ('p', 'part time'),
#         ('f', 'full time'),
#         ('n', 'not employed'),
#         ('s', 'student'),
#     )
#
#     SEX = (
#         (-1, ''),
#         ('f', 'female'),
#         ('m', 'male'),
#         ('t', 'transgender'),
#         ('q', 'queer'),
#     )
#
#     # probably should pull lots of this info from someone elses db
#     RACE = (
#         (-1, ''),
#         ('a', 'asian'),
#         ('b', 'black'),
#         ('h', 'hispanic/latino'),
#         ('w', 'white'),
#     )
#
#     RELATIONSHIP_STATUS = (
#         (-1, ''),
#         ('s', 'single'),
#         ('c', 'casually dating'),
#         ('r', 'seriously dating'),
#         ('o', 'committed'),
#         ('e', 'engaged'),
#         ('m', 'married'),
#         ('j', 'just talking'),
#     )
#
#     SALARY = (
#         (-1, ''),
#         (0, 'Below $10,000'),
#         (1, '$10,000 - $30,000'),
#         (2, '$30,000 - $50,000'),
#         (3, '$50,000 - $80,000'),
#         (4, '$80,000 - $100,000'),
#         (5, '$100,000+'),
#     )
#
#     SEXUAL_PREFERENCE = (
#         (-1, ''),
#         ('m', 'men'),
#         ('b', 'men and women'),
#         ('w', 'women'),
#         ('o', 'otheruser = models.ForeignKey(User)'),
#     )
#
#     RELIGION = (
#         (-1, ''),
#         ('c', 'christianity'),
#         ('j', 'judaism'),
#         ('i', 'islam'),
#         ('b', 'buddhism'),
#         ('h', 'hinduism'),
#         ('a', 'atheism'),
#         ('g', 'agnostic'),
#         ('n', 'none'),
#         ('o', 'other'),
#     )
#
#     AGREEMENT = (
#         (-1, ''),
#         (1, 'strongly disagree'),
#         (2, 'disagree'),
#         (3, 'neither agree nor disagree'),
#         (4, 'agree'),
#         (5, 'strongly agree'),
#     )
#
#     FREQUENCY = (
#         (-1, ''),
#         ('n', 'never'),
#         ('r', 'rarely'),
#         ('s', 'sometimes'),
#         ('o', 'often'),
#         ('f', 'frequently'),
#     )
#
#     # birthday to derive age
#     birthday = models.DateField(auto_now=False)
#     education = models.IntegerField(choices=EDUCATION)
#     employmentStatus = models.CharField(max_length=1, choices=EMPLOYMENT_STATUS)
#     familySize = models.IntegerField()
#     gender = models.CharField(max_length=1, choices=SEX)
#     # sex = models.CharField(max_length=1)
#     relationshipStatus = models.CharField(max_length=1, choices=RELATIONSHIP_STATUS)
#
#     # postal code to derive location
#     postalCode = models.CharField(max_length=32)
#     race = models.CharField(max_length=2)
#     salary = models.IntegerField(choices=SALARY)
#     sexual_orientation = models.CharField(max_length=1)
#
#     FAMILYSIZE = ((i for i in range(101)),)
#
#     user = models.ForeignKey(User)
#     # birthday to derive age
#     sex = models.CharField(max_length=1, choices=SEX, default=-1)
#     sexualPreference = models.CharField(max_length=1, choices=SEXUAL_PREFERENCE, default=-1)
#
#     religion = models.CharField(max_length=1, choices=RELIGION, default=-1)
#     religiousInfluence = models.CharField(max_length=1, choices=AGREEMENT, default=-1)
#
#     # personal relationship experiences
#     addictive = models.CharField(max_length=1, choices=FREQUENCY, default=-1)
#     violence = models.CharField(max_length=1, choices=FREQUENCY, default=-1)
#     breakups = models.CharField(max_length=1, choices=FREQUENCY, default=-1)
#     verbalEmotionalAbuse = models.CharField(max_length=1, choices=FREQUENCY, default=-1)
#     infidelity = models.CharField(max_length=1, choices=FREQUENCY, default=-1)
#
#     # Others relationship experiences
#     addictiveOther = models.CharField(max_length=1, choices=FREQUENCY, default=-1)
#     violenceOther = models.CharField(max_length=1, choices=FREQUENCY, default=-1)
#     breakupsOther = models.CharField(max_length=1, choices=FREQUENCY, default=-1)
#     verbalEmotionalAbuseOther = models.CharField(max_length=1, choices=FREQUENCY, default=-1)
#     infidelityOther = models.CharField(max_length=1, choices=FREQUENCY, default=-1)
#
#     # metrics
#     cyclicRelationships = models.BooleanField(default=-1)
#     timesCycled = models.IntegerField(default=-1)
#     timesMarried = models.IntegerField(default=-1)  # needs bounding options set
#     biologicalChildren = models.IntegerField(default=-1)
#     adoptedChildren = models.IntegerField(default=-1)
#     stepChildren = models.IntegerField(default=-1)
#     lengthOfCurrentRelationship = models.IntegerField(default=-1)
#
#     currentRelationshipHappiness = models.CharField(max_length=1, choices=AGREEMENT, default=-1)
#     gettingDivorced = models.NullBooleanField()


# # table of tags for use in adding new tags
# class Tag(models.Model):
#     tagName = models.CharField(max_length=100)
#
#
# # table for linking tags to articles
# class TagTable(models.Model):
#     article = models.ForeignKey(Article)
#     tag = models.ForeignKey(Tag)
