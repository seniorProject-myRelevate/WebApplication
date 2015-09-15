from django.db import models


# User Database Model
class User(models.Model):
    confirmed = models.BooleanField(auto_created=False)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=500)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=150)
    createdDate = models.DateField()
    lastLogin = models.DateField()


# DemographicData Database Model
class DemographicData(models.Model):

    EDUCATION = (
        (0, 'Completed high school/GED'),
        (1, 'Some college no longer attending'),
        (2, 'Some college currently attending'),
        (3, 'Graduated with bachelors'),
        (4, 'Graduated with bachelors'),
        (5, 'Graduated with PhD'),
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
        ('w', 'women'),
        ('b', 'men and women'),
        ('o', 'other'),
    )

    user = models.ForeignKey(User)
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
