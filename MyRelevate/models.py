from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    """
    Basic User Class
    """

    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    joined_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.email


# DemographicData Database Model
class DemographicData(models.Model):
    EDUCATION = (
        (0, 'Completed high school/GED'),
        (1, 'Some college no longer attending'),
        (2, 'Some college currently attending'),
        (3, 'Graduated with bachelors'),
        (4, 'Graduated with bachelors'),
        (5, 'Graduated with PhD'),
        (6, 'Did not complete high school'),
    )

    EMPLOYMENT_STATUS = (
        ('p', 'part time'),
        ('f', 'full time'),
        ('n', 'not employed'),
        ('s', 'student'),
    )

    SEX = (
        ('f', 'female'),
        ('m', 'male'),
        ('t', 'transgender'),
        ('q', 'queer'),
    )

    # probably should pull lots of this info from someone elses DB.
    RACE = (
        ('a', 'asian'),
        ('b', 'black'),
        ('h', 'hispanic/latino'),
        ('w', 'white'),
        ('i', 'native american/alaskan'),
        ('o', 'other'),
    )

    RELATIONSHIP_STATUS = (
        ('s', 'single'),
        ('c', 'casually dating'),
        ('r', 'seriously dating'),
        ('o', 'committed'),
        ('e', 'engaged'),
        ('m', 'married'),
        ('j', 'just talking'),
    )

    SALARY = (
        (0, 'Below $10,000'),
        (1, '$10,000 - $30,000'),
        (2, '$30,000 - $50,000'),
        (3, '$50,000 - $80,000'),
        (4, '$80,000 - $100,000'),
        (5, '$100,000+'),
    )

    SEXUAL_PREFERENCE = (
        ('m', 'men'),
        ('b', 'men and women'),
        ('w', 'women'),
        ('o', 'otheruser = models.ForeignKey(User)'),
    )

    RELIGION = (
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
        (1, 'strongly disagree'),
        (2, 'disagree'),
        (3, 'neither agree nor disagree'),
        (4, 'agree'),
        (5, 'strongly agree'),
    )

    FREQUENCY = (
        ('n', 'never'),
        ('r', 'rarely'),
        ('s', 'sometimes'),
        ('o', 'often'),
        ('f', 'frequently'),
    )

    user = models.ForeignKey(User)
    # birthday to derive age
    birthday = models.DateField(auto_now=False)
    education = models.IntegerField(choices=EDUCATION)
    employmentStatus = models.CharField(max_length=1, choices=EMPLOYMENT_STATUS)
    familySize = models.IntegerField()
    sex = models.CharField(max_length=1, choices=SEX)
    relationshipStatus = models.CharField(max_length=1, choices=RELATIONSHIP_STATUS)

    # postal code to derive location
    postalCode = models.CharField(max_length=32)
    race = models.CharField(max_length=2)
    salary = models.IntegerField(choices=SALARY)
    sexualPreference = models.CharField(max_length=1, choices=SEXUAL_PREFERENCE)

    religion = models.CharField(max_length=1, choices=RELIGION)
    religiousInfluence = models.IntegerField(choices=AGREEMENT)

    # personal relationship experiences
    addictive = models.CharField(max_length=1, choices=FREQUENCY)
    violence = models.CharField(max_length=1, choices=FREQUENCY)
    breakups = models.CharField(max_length=1, choices=FREQUENCY)
    verbalEmotionalAbuse = models.CharField(max_length=1, choices=FREQUENCY)
    infidelity = models.CharField(max_length=1, choices=FREQUENCY)

    # Others relationship experiences
    addictiveOther = models.CharField(max_length=1, choices=FREQUENCY)
    violenceOther = models.CharField(max_length=1, choices=FREQUENCY)
    breakupsOther = models.CharField(max_length=1, choices=FREQUENCY)
    verbalEmotionalAbuseOther = models.CharField(max_length=1, choices=FREQUENCY)
    infidelityOther = models.CharField(max_length=1, choices=FREQUENCY)

    # metrics
    cyclicRelationships = models.BooleanField()
    timesCycled = models.IntegerField()
    timesMarried = models.IntegerField()  # needs bounding options set
    biologicalChildren = models.IntegerField()
    adoptedChildren = models.IntegerField()
    stepChildren = models.IntegerField()
    lengthOfCurrentRelationship = models.IntegerField()

    currentRelationshipHappiness = models.IntegerField(choices=AGREEMENT)
    gettingDivorced = models.BooleanField()


# base model for article
class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User)
    content = models.TextField()  # check if this requires bounding for security purposes
    publishDate = models.DateField()
    updateDate = models.DateField()


# table of tags for use in adding new tags
class Tag(models.Model):
    tagName = models.CharField(max_length=100)


# table for linking tags to articles
class TagTable(models.Model):
    article = models.ForeignKey(Article)
    tag = models.ForeignKey(Tag)
