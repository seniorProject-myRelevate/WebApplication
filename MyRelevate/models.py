import os

import sendgrid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from Contributor.models import ContributorProfile


class Subscriber(models.Model):
    email = models.EmailField(unique=True, null=False, blank=False)


    # Below are helper functions that are not associated with any particular route
    def send_email(self, subject, html, sender='noreply@myrelevate.com'):
        client = sendgrid.SendGridClient(os.environ['SendGridApiKey'])
        message = sendgrid.Mail()

        message.add_to(self.email)
        message.set_from(sender)
        message.set_subject(subject)
        message.set_html(html)

        client.send(message)


# DemographicData Database Model
# class DemographicData(models.py.Model):
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
#         ('o', 'otheruser = models.py.ForeignKey(User)'),
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
#     birthday = models.py.DateField(auto_now=False)
#     education = models.py.IntegerField(choices=EDUCATION)
#     employmentStatus = models.py.CharField(max_length=1, choices=EMPLOYMENT_STATUS)
#     familySize = models.py.IntegerField()
#     gender = models.py.CharField(max_length=1, choices=SEX)
#     # sex = models.py.CharField(max_length=1)
#     relationshipStatus = models.py.CharField(max_length=1, choices=RELATIONSHIP_STATUS)
#
#     # postal code to derive location
#     postalCode = models.py.CharField(max_length=32)
#     race = models.py.CharField(max_length=2)
#     salary = models.py.IntegerField(choices=SALARY)
#     sexual_orientation = models.py.CharField(max_length=1)
#
#     FAMILYSIZE = ((i for i in range(101)),)
#
#     user = models.py.ForeignKey(User)
#     # birthday to derive age
#     sex = models.py.CharField(max_length=1, choices=SEX, default=-1)
#     sexualPreference = models.py.CharField(max_length=1, choices=SEXUAL_PREFERENCE, default=-1)
#
#     religion = models.py.CharField(max_length=1, choices=RELIGION, default=-1)
#     religiousInfluence = models.py.CharField(max_length=1, choices=AGREEMENT, default=-1)
#
#     # personal relationship experiences
#     addictive = models.py.CharField(max_length=1, choices=FREQUENCY, default=-1)
#     violence = models.py.CharField(max_length=1, choices=FREQUENCY, default=-1)
#     breakups = models.py.CharField(max_length=1, choices=FREQUENCY, default=-1)
#     verbalEmotionalAbuse = models.py.CharField(max_length=1, choices=FREQUENCY, default=-1)
#     infidelity = models.py.CharField(max_length=1, choices=FREQUENCY, default=-1)
#
#     # Others relationship experiences
#     addictiveOther = models.py.CharField(max_length=1, choices=FREQUENCY, default=-1)
#     violenceOther = models.py.CharField(max_length=1, choices=FREQUENCY, default=-1)
#     breakupsOther = models.py.CharField(max_length=1, choices=FREQUENCY, default=-1)
#     verbalEmotionalAbuseOther = models.py.CharField(max_length=1, choices=FREQUENCY, default=-1)
#     infidelityOther = models.py.CharField(max_length=1, choices=FREQUENCY, default=-1)
#
#     # metrics
#     cyclicRelationships = models.py.BooleanField(default=-1)
#     timesCycled = models.py.IntegerField(default=-1)
#     timesMarried = models.py.IntegerField(default=-1)  # needs bounding options set
#     biologicalChildren = models.py.IntegerField(default=-1)
#     adoptedChildren = models.py.IntegerField(default=-1)
#     stepChildren = models.py.IntegerField(default=-1)
#     lengthOfCurrentRelationship = models.py.IntegerField(default=-1)
#
#     currentRelationshipHappiness = models.py.CharField(max_length=1, choices=AGREEMENT, default=-1)
#     gettingDivorced = models.py.NullBooleanField()


# table of tags for use in adding new tags
# class Tag(models.py.Model):
#     tagName = models.py.CharField(max_length=100)
#     tagDescription = models.py.CharField(max_length=255)
#     may need two more charfields to hold selected tagName and tagDescription
#
# # table for linking tags to Articles
# class TagTable(models.py.Model):
#     article = models.py.ForeignKey(Article)
#     tag = models.py.ForeignKey(Tag)
