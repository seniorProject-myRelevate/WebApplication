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
<<<<<<< HEAD
            return self.email
=======
        return self.email
>>>>>>> c4bfe8e832acc437f2c1485cb6d163cc1675c7e3


# DemographicData Database Model
class DemographicData(models.Model):
<<<<<<< HEAD

=======
>>>>>>> c4bfe8e832acc437f2c1485cb6d163cc1675c7e3
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
<<<<<<< HEAD
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
=======
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
>>>>>>> c4bfe8e832acc437f2c1485cb6d163cc1675c7e3
    RACE = (
        ('a', 'asian'),
        ('b', 'black'),
        ('h', 'hispanic/latino'),
        ('w', 'white'),
<<<<<<< HEAD
    )

    RELATIONSHIP_STATUS = (
        ('e', 'engaged'),
        ('m', 'married'),
        ('r', 'relationship'),
        ('s', 'single'),
=======
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
>>>>>>> c4bfe8e832acc437f2c1485cb6d163cc1675c7e3
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
<<<<<<< HEAD
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
=======
        ('o', 'opposite sex'),
        ('s', 'same sex'),
        ('b', 'both sexes'),
        ('n', 'neither'),
    )

    RELIGION = (
        ('c','christianity'),
        ('j','judaism'),
        ('i','islam'),
        ('b','buddhism'),
        ('h','hinduism'),
        ('a','atheism'),
        ('g','agnostic'),
        ('n','none'),
        ('o','other'),
    )

    AGREEMENT = (
        (0, 'strongly disagree'),
        (1, 'disagree'),
        (2, 'neither agree nor disagree'),
        (3, 'agree'),
        (4, 'strongly agree'),
    )

    FREQUENCY = (
        ('n', 'never'),
        ('r', 'rarely'),
        ('s', 'sometimes'),
        ('o', 'often'),
        ('f', 'frequently'),
    )

    FAMILYSIZE = ((i for i in range(101)),)
        
    user = models.ForeignKey(User)
    # birthday to derive age
    birthday = models.DateField(auto_now=False)

    education = models.IntegerField(choices=EDUCATION, blank=True)
    employmentStatus = models.CharField(max_length=1, choices=EMPLOYMENT_STATUS, blank=True)
    familySize = models.IntegerField(choices=FAMILYSIZE, blank=True)
    sex = models.CharField(max_length=1, choices=SEX, blank=True)
    relationshipStatus = models.CharField(max_length=1, choices=RELATIONSHIP_STATUS, blank=True)

    # postal code to derive location
    postalCode = models.CharField(max_length=32)
    race = models.CharField(max_length=1, choices=RACE, blank=True)
    salary = models.IntegerField(choices=SALARY, blank=True)
    sexualPreference = models.CharField(max_length=1, choices=SEXUAL_PREFERENCE, blank=True)
    religion = models.CharField(max_length=1, choices=RELIGION, blank=True)
    religiousInfluence = models.IntegerField(choices=AGREEMENT, blank=True)

    # personal relationship experiences
    addictive = models.CharField(max_length=1, choices=FREQUENCY, blank=True)
    violence = models.CharField(max_length=1, choices=FREQUENCY, blank=True)
    breakups = models.CharField(max_length=1, choices=FREQUENCY, blank=True)
    verbalEmotionalAbuse = models.CharField(max_length=1, choices=FREQUENCY, blank=True)
    infidelity = models.CharField(max_length=1, choices=FREQUENCY, blank=True)

    # Others relationship experiences
    addictiveOther = models.CharField(max_length=1, choices=FREQUENCY, blank=True)
    violenceOther = models.CharField(max_length=1, choices=FREQUENCY, blank=True)
    breakupsOther = models.CharField(max_length=1, choices=FREQUENCY, blank=True)
    verbalEmotionalAbuseOther = models.CharField(max_length=1, choices=FREQUENCY, blank=True)
    infidelityOther = models.CharField(max_length=1, choices=FREQUENCY, blank=True)


    #metrics
    CYCLES = ((i for i in range(21)),)
    cyclicRelationships = models.BooleanField(default=False)
    timesCycled = models.IntegerField(choices=CYCLES)
    timesMarried = models.IntegerField(choices=CYCLES)
    CHILDREN = ((i for i in range(101)),)
    biologicalChildren = models.IntegerField(choices=CHILDREN)
    adoptedChildren = models.IntegerField(choices=CHILDREN)
    stepChildren = models.IntegerField(choices=CHILDREN)
    YEARS = ((i for i in range(101)),)
    lengthOfCurrentRelationship = models.IntegerField(choices=YEARS)
    currentRelationshipHappiness = models.CharField(max_length=1,choices=AGREEMENT, blank=True)
    gettingDivorced = models.BooleanField(default=False)



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
>>>>>>> c4bfe8e832acc437f2c1485cb6d163cc1675c7e3
class TagTable(models.Model):
    article = models.ForeignKey(Article)
    tag = models.ForeignKey(Tag)
