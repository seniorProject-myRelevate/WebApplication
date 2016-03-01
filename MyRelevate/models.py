from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User


# class Usertest(AbstractBaseUser):
#     """
#     Basic User Class
#     """
#
#     email = models.EmailField(unique=True, db_index=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     joined_date = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)
#     confirmed = models.BooleanField(default=False)
#
#     USERNAME_FIELD = 'email'
#
#     def __unicode__(self):
#         return self.email

class Subscriber(models.Model):
    db_table = "myrelevate_subscriber"
    email = models.EmailField(unique=True, null=False, blank=False)


class Article(models.Model):
    db_table = "myrelevate_article"
    title = models.CharField(max_length=100)
    content = models.TextField()  # check if this requires bounding for security purposes
    publishDate = models.DateField()
    updateDate = models.DateField()


class ContributorProfile(models.Model):
    db_table = "myrelevate_contributorprofile"
    biography = models.CharField(max_length=255, null=True, blank=True)
    # should be multichoice.
    area_of_expertise = models.CharField(max_length=255, choices=None, null=True, blank=True)
    # profile_image = models.ImageField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    cv = models.FileField(upload_to='user_profiles/cv', null=True, blank=True)
    articles = models.ForeignKey(Article, null=True, blank=True)


class UserProfile(models.Model):
    db_table = "myrelevate_userprofile"
    user = models.OneToOneField(User)
    contributorProfile = models.OneToOneField(ContributorProfile, null=True)

    def __unicode__(self):
        return self.user.username


# DemographicData Database Model
class DemographicData(models.Model):
    db_table = "myrelevate_demographicdata"
    EDUCATION = (
        (-1, ''),
        (0, 'Completed high school/GED'),
        (1, 'Some college no longer attending'),
        (2, 'Some college currently attending'),
        (3, 'Graduated with bachelors'),
        (4, 'Graduated with bachelors'),
        (5, 'Graduated with PhD'),
        (6, 'Did not complete high school'),
    )

    EMPLOYMENT_STATUS = (
        (-1, ''),
        ('p', 'part time'),
        ('f', 'full time'),
        ('n', 'not employed'),
        ('s', 'student'),
    )

    SEX = (
        (-1, ''),
        ('f', 'female'),
        ('m', 'male'),
        ('t', 'transgender'),
        ('q', 'queer'),
    )

    # probably should pull lots of this info from someone elses db
    RACE = (
        (-1, ''),
        ('a', 'asian'),
        ('b', 'black'),
        ('h', 'hispanic/latino'),
        ('w', 'white'),
    )

    RELATIONSHIP_STATUS = (
        (-1, ''),
        ('s', 'single'),
        ('c', 'casually dating'),
        ('r', 'seriously dating'),
        ('o', 'committed'),
        ('e', 'engaged'),
        ('m', 'married'),
        ('j', 'just talking'),
    )

    SALARY = (
        (-1, ''),
        (0, 'Below $10,000'),
        (1, '$10,000 - $30,000'),
        (2, '$30,000 - $50,000'),
        (3, '$50,000 - $80,000'),
        (4, '$80,000 - $100,000'),
        (5, '$100,000+'),
    )

    SEXUAL_PREFERENCE = (
        (-1, ''),
        ('m', 'men'),
        ('b', 'men and women'),
        ('w', 'women'),
        ('o', 'otheruser = models.ForeignKey(User)'),
    )

    RELIGION = (
        (-1, ''),
        ('c', 'christianity'),
        ('j', 'judaism'),
        ('i', 'islam'),
        ('b', 'buddhism'),
        ('h', 'hinduism'),
        ('a', 'atheism'),
        ('g', 'agnostic'),
        ('n', 'none'),
        ('o', 'other'),
    )

    AGREEMENT = (
        (-1, ''),
        (1, 'strongly disagree'),
        (2, 'disagree'),
        (3, 'neither agree nor disagree'),
        (4, 'agree'),
        (5, 'strongly agree'),
    )

    FREQUENCY = (
        (-1, ''),
        ('n', 'never'),
        ('r', 'rarely'),
        ('s', 'sometimes'),
        ('o', 'often'),
        ('f', 'frequently'),
    )

    # birthday to derive age
    birthday = models.DateField(auto_now=False)
    education = models.IntegerField(choices=EDUCATION)
    employmentStatus = models.CharField(max_length=1, choices=EMPLOYMENT_STATUS)
    familySize = models.IntegerField()
    gender = models.CharField(max_length=1, choices=SEX)
    # sex = models.CharField(max_length=1)
    relationshipStatus = models.CharField(max_length=1, choices=RELATIONSHIP_STATUS)

    # postal code to derive location
    postalCode = models.CharField(max_length=32)
    race = models.CharField(max_length=2)
    salary = models.IntegerField(choices=SALARY)
    sexual_orientation = models.CharField(max_length=1)

    FAMILYSIZE = ((i for i in range(101)),)

    user = models.ForeignKey(User)
    # birthday to derive age
    sex = models.CharField(max_length=1, choices=SEX, default=-1)
    sexualPreference = models.CharField(max_length=1, choices=SEXUAL_PREFERENCE, default=-1)

    religion = models.CharField(max_length=1, choices=RELIGION, default=-1)
    religiousInfluence = models.CharField(max_length=1, choices=AGREEMENT, default=-1)

    # personal relationship experiences
    addictive = models.CharField(max_length=1, choices=FREQUENCY, default=-1)
    violence = models.CharField(max_length=1, choices=FREQUENCY, default=-1)
    breakups = models.CharField(max_length=1, choices=FREQUENCY, default=-1)
    verbalEmotionalAbuse = models.CharField(max_length=1, choices=FREQUENCY, default=-1)
    infidelity = models.CharField(max_length=1, choices=FREQUENCY, default=-1)

    # Others relationship experiences
    addictiveOther = models.CharField(max_length=1, choices=FREQUENCY, default=-1)
    violenceOther = models.CharField(max_length=1, choices=FREQUENCY, default=-1)
    breakupsOther = models.CharField(max_length=1, choices=FREQUENCY, default=-1)
    verbalEmotionalAbuseOther = models.CharField(max_length=1, choices=FREQUENCY, default=-1)
    infidelityOther = models.CharField(max_length=1, choices=FREQUENCY, default=-1)

    # metrics
    cyclicRelationships = models.BooleanField(default=-1)
    timesCycled = models.IntegerField(default=-1)
    timesMarried = models.IntegerField(default=-1)  # needs bounding options set
    biologicalChildren = models.IntegerField(default=-1)
    adoptedChildren = models.IntegerField(default=-1)
    stepChildren = models.IntegerField(default=-1)
    lengthOfCurrentRelationship = models.IntegerField(default=-1)

    currentRelationshipHappiness = models.CharField(max_length=1, choices=AGREEMENT, default=-1)
    gettingDivorced = models.NullBooleanField()


# table of tags for use in adding new tags
class Tag(models.Model):
    db_table = "myrelevate_tag"
    tagName = models.CharField(max_length=100)


# table for linking tags to articles
class TagTable(models.Model):
    db_table = "myrelevate_tagtable"
    article = models.ForeignKey(Article)
    tag = models.ForeignKey(Tag)
