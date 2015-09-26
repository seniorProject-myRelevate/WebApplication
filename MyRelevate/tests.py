from django.test import TestCase
import datetime
import re
import random
import models


class UserTests(TestCase):
    def setUp(self):
        models.User.objects.create(email="fbar@gmail.com", first_name="Alex", last_name="Beahm",
                            joined_date=datetime.datetime.now(), is_active=True, confirmed=True)

        models.User.objects.create(email="fbar",
                            first_name="Thisnameiswaytoolongbecauseitisgreaterthanfiftycharactersandcontainsnumbersandspecialcharacters",
                            last_name="Thislastnameisalsowaytoolongbecauseitisgreaterthanfiftycharactersandcontainsnumbersandspecialcharacters",
                            joined_date=datetime.datetime(2011,1,1,0,0,0,0), is_active=False, is_confirmed=False)

    def validEmail(self):
        """
        Regex is used to just check if the e-mail is in a correct format
        """
        goodUser = models.User.objects.get(email="fbar@gmail.com")
        badUser = models.User.objects.get(email="bar")

        self.assertTrue(re.match(r"[^@]@[^@]\.[^@]", goodUser['email']))
        self.assertFalse(re.match(r"[^@]@[^@]\.[^@]", badUser['email']))

    def validFirstName(self):
        goodUserName = models.User.objects.get(email="fbar@gmail.com")['first_name']
        badUserName = models.User.objects.get(email="bar")['first_name']
        maxChars = 50
        self.assertTrue(re.match(r"^[A-Za-z/-]*$"),goodUserName)
        self.assertTrue(len(goodUserName) <= maxChars and not len(goodUserName))

        self.assertFalse(re.match(r"^[A-Za-z/-]*$"), badUserName)
        self.assertFalse(len(badUserName) <= maxChars)

    def validLastName(self):
        goodUserLast = models.User.objects.get(email="fbar@gmail.com")
        badUserLast = models.User.objects.get(email="bar")

        maxChars = 50
        self.assertTrue(re.match(r"^[A-Za-z/-]*$"),goodUserLast)
        self.assertTrue(len(goodUserLast) <= maxChars and not len(goodUserLast))

        self.assertFalse(re.match(r"^[A-Za-z/-]*$"),badUserLast)
        self.assertFalse(len(badUserLast) <= maxChars)

    def validDate(self):
        goodUserDate = models.User.objects.get(email="fbar@gmail.com")['joined_date']
        badUserDate = models.User.objects.get(email="bar")['joined_date']

        self.assertIsInstance(goodUserDate, datetime)

        """Will be changed to a time where the site will actually go live for accuracya"""
        dateOfProduction = datetime.datetime(2015,9,22,0,0,0,0)

        self.assertTrue(dateOfProduction < goodUserDate)
        self.assertFalse(dateOfProduction > badUserDate)


class DemographicModelTests(TestCase):
    def setUp(self):
        models.DemographicData.objects.create(birthday = datetime.datetime(1994,1,1,0,0,0,0),
                                              education = random.randint(0,6),
                                              employmentStatus = 'e',
                                              familySize = random.randint(0,15),
                                              gender = 'm',relationshipStatus = 's',
                                              postalCode = "66503",
                                              race = 'w',
                                              salary = random.randint(0,5),
                                              sexual_orientation = 'w')

        models.DemographicData.objects.create(birthday = datetime.datetime.now(),
                                              education = 7,
                                              employmentStatus = 'z',
                                              familySize = 16,
                                              gender = 'z',relationshipStatus = 'z',
                                              postalCode = "ZIPCODE",
                                              race = 'z',
                                              salary = 6,
                                              sexual_orientation = 'z')

    def validBirthday(self):
        goodDate = models.DemographicData.objects.get(postalCode = "66503").birthday
        badDate = models.DemographicData.objects.get(postalCode = "ZIPCODE").birthday

        """Assuming nobody lives forever and also not a baby and using this, setting up some age limits for testing"""
        dateOfOldAge   = datetime.datetime(1899,7,6)
        dateOfYoungAge = datetime.datetime(2001,9,23)

        self.assertIsInstance(goodDate,datetime)
        self.assertTrue(dateOfOldAge > goodDate)
        self.assertTrue(dateOfYoungAge < goodDate)

        self.assertFalse(dateOfYoungAge < badDate)

    def validEducation(self):
        goodEdu = models.DemographicData.objects.get(postalCode = "66503").education
        badEdu = models.DemographicData.objects.get(postalCode = "ZIPCODE").education

        self.assertIn(goodEdu, models.DemographicData.EDUCATION)
        self.assertNotIn(badEdu, models.DemographicData.EDUCATION)

    def validEmployment(self):
        goodEmploy = models.DemographicData.objects.get(postalCode = "66503").employmentStatus
        badEmploy = models.DemographicData.objects.get(postalCode = "ZIPCODE").employmentStatus

        self.assertIn(goodEmploy, models.DemographicData.EDUCATION)
        self.assertNotIn(badEmploy, models.DemographicData.EDUCATION)

    def validFamily(self):
        goodFamily = models.DemographicData.objects.get(postalCode = "66503").familySize
        badFamily = models.DemographicData.objects.get(postalCode = "ZIPCODE").familySize

        """Setting arbitrary family limit at 15 for now, will probably change"""
        self.assertTrue(goodFamily > 0 and goodFamily <= 15)

        self.assertTrue(badFamily < 0 or badFamily > 15)

    def validGender(self):
        goodGen = models.DemographicData.objects.get(postalCode = "66503").gender
        badGen = models.DemographicData.objects.get(postalCode = "ZIPCODE").gender

        self.assertIn(goodGen, models.DemographicData.GENDER)
        self.assertNotIn(badGen, models.DemographicData.GENDER)

    def validRelationship(self):
        goodRel = models.DemographicData.objects.get(postalCode = "66503").relationship_status
        badRel = models.DemographicData.objects.get(postalCode = "ZIPCODE").relationship_status

        self.assertIn(goodRel, models.DemographicData.RELATIONSHIP_STATUS)
        self.assertNotIn(badRel, models.DemographicData.RELATIONSHIP_STATUS)

    def validPostalCode(self):
        goodPost = models.DemographicData.objects.get(postalCode = "66503").postalCode
        badPost = models.DemographicData.objects.get(postalCode = "ZIPCODE").postalCode

        self.assertTrue(re.match(r"^[0-9]{5}-[0-9]{4}$|^[0-9]{5}$",goodPost))
        self.assertFalse(re.match(r"^[0-9]{5}-[0-9]{4}$|^[0-9]{5}$",badPost))

    def validRace(self):
        goodRace = models.DemographicData.objects.get(postalCode = "66503").race
        badRace = models.DemographicData.objects.get(postalCode = "ZIPCODE").race

        self.assertIn(goodRace, models.DemographicData.RACE)
        self.assertNotIn(badRace, models.DemographicData.RACE)

    def validSalary(self):
        goodSalary = models.DemographicData.objects.get(postalCode = "66503").salary
        badSalary = models.DemographicData.objects.get(postalCode = "ZIPCODE").salary

        self.assertIn(goodSalary, models.DemographicData.SALARY)
        self.assertNotIn(badSalary, models.DemographicData.SALARY)

    def validSexualOrientation(self):
        goodSex = models.DemographicData.objects.get(postalCode = "66503").sexual_orientation
        badSex= models.DemographicData.objects.get(postalCode = "ZIPCODE").sexual_orientation

        self.assertIn(goodSex, models.DemographicData.SEXUAL_PREFERENCE)
        self.assertNotIn(badSex, models.DemographicData.SEXUAL_PREFERENCE)


class ArticleModelTests(TestCase):
    def setUp(self):
        testUser = models.User.objects.create(email="fbar@gmail.com", first_name="Alex", last_name="Beahm",
                                   joined_date=datetime.datetime.now(), is_active=True, confirmed=True)

        models.Article.objects.create(title = "SomeTitle", author = testUser, content = "Test content for the article",
                                      publishDate = datetime.datetime.now(), updateDate = datetime.datetime.now())

        models.Article.objects.create(title = "", author = None, content = "",
                                      publishDate = datetime.datetime.now(), updateDate = datetime.datetime(2014,1,1))

    def validTitle(self):
        goodTitle = models.User.objects.get(title = "SomeTitle").title
        badTitle = models.User.objects.get(title = "").title

        self.assertTrue(len(goodTitle) > 0)
        self.assertFalse(len(goodTitle) > 0)

    def validAuthor(self):
        goodUser = models.User.objects.get(title = "SomeTitle").author
        badUser = models.User.objects.get(title = "").author

        self.assertIsInstance(goodUser, models.User)
        self.assertNotIsInstance(badUser, models.User)

    def validContent(self):
        goodContent = models.User.objects.get(title = "SomeTitle").content
        badContent = models.User.objects.get(title = "").content

        self.assertGreater(len(goodContent), 0)
        self.assertEqual(len(badContent), 0)

    def validDateInstances(self):
        goodPDate = models.User.objects.get(title = "SomeTitle").publishDate
        badPDate = models.User.objects.get(title = "SomeTitle").publishDate
        goodUDate = models.User.objects.get(title = "SomeTitle").updateDate
        badUDate = models.User.objects.get(title = "SomeTitle").updateDate

        self.assertIsInstance(goodPDate,datetime)
        self.assertIsInstance(goodUDate,datetime)

        self.assertFalse(badPDate < badUDate)
        self.assertTrue(goodPDate < goodUDate)


class TagModelTests(TestCase):
    def setUp(self):
        models.Tag.objects.create(tagName = "testTag")
        models.Tag.objects.create(tagName = "")

    def validTagName(self):
        goodTag = models.Tag.objects.get(tagName = "testTag").tagName
        badTag = models.Tag.objects.get(tagName = "").tagName
        self.assertGreater(goodTag, 0)
        self.assertFalse(badTag > 0)

class TagTableModelTests(TestCase):
    def setUp(self):
        testUser = models.User.objects.create(email="fbar@gmail.com", first_name="Alex", last_name="Beahm",
                                   joined_date=datetime.datetime.now(), is_active=True, confirmed=True)
        testArticle = models.Article.objects.create(title = "SomeTitle", author = testUser, content = "Test content for the article",
                                      publishDate = datetime.datetime.now(), updateDate = datetime.datetime.now())
        testTag = models.Tag.objects.create(tagName = "testTag")

        models.TagTable.objects.create(article = testArticle, tag = testTag)

    def validArticle(self):
        goodArticle = models.TagTable.objects.get().article

        self.assertIsInstance(goodArticle, models.Article)

    def validTag(self):
        goodTag = models.TagTable.objects.get().tag

        self.assertIsInstance(goodTag, models.Tag)