from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name):
        user = self.model(username=email, first_name=first_name,
                          last_name=last_name)
        return user


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
        ('e', 'employed'),
        ('n', 'not employed'),
        ('s', 'self employed'),
    )

    GENDER = (
        ('f', 'female'),
        ('m', 'male'),
        ('t', 'transgender'),
    )

    #probably should pull lots of this info from someone elses DB.
    RACE = (
        ('a', 'asian'),
        ('b', 'black'),
        ('h', 'hispanic/latino'),
        ('w', 'white'),
    )

    RELATIONSHIP_STATUS = (
        ('e', 'engaged'),
        ('m', 'married'),
        ('r', 'relationship'),
        ('s', 'single'),
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
    # birthday to derive age
    birthday = models.DateField(auto_now=False)
    education = models.IntegerField(choices=EDUCATION)
    employmentStatus = models.CharField(max_length=1, choices=EMPLOYMENT_STATUS)
    familySize = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER)
    # sex = models.CharField(max_length=1)
    relationshipStatus = models.CharField(max_length=1, choices=RELATIONSHIP_STATUS)

    # postal code to derive location
    postalCode = models.CharField(max_length=32)
    race = models.CharField(max_length=2)
    salary = models.IntegerField(choices=SALARY)
    sexual_orientation = models.CharField(max_length=1)


#base model for article
class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User)
    content = models.TextField()#check if this requires bounding for security purposes
    publishDate = models.DateField()
    updateDate = models.DateField()


#table of tags for use in adding new tags
class Tag(models.Model):
    tagName = models.CharField(max_length=100)


#table for linking tags to articles
class TagTable(models.Model):
    article = models.ForeignKey(Article)
    tag = models.ForeignKey(Tag)
