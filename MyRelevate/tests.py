import datetime
import re
import random
import models
from django.test import TestCase

class UserModelTests(TestCase):
    def setUp(self):
        models.User.objects.create(email       = "fbar@gmail.com",
                                   first_name  = "Alex",
                                   last_name   = "Beahm",
                                   joined_date = datetime.datetime.now(),
                                   is_active   = True,
                                   confirmed   = True)
        models.User.objects.create(email       = "fbar",
                                   first_name  = "Thisnameiswaytoolongbecauseitisgreaterthanfiftycharactersandcontainsnumbersandspecialcharacters3344$$",
                                   last_name   = "Thislastnameisalsowaytoolongbecauseitisgreaterthanfiftycharactersandcontainsnumbersandspecialcharacters55%^  F",
                                   joined_date = datetime.datetime(2011,1,1,0,0,0,0),
                                   is_active   = False,
                                   confirmed   = False)

        models.User.objects.get(email = "fbar@gmail.com").set_password("password")
        models.User.objects.get(email = "fbar").set_unusable_password()

    def test_ValidEmail(self):
        """
        Regex is used to just check if the e-mail is in a correct format
        """
        goodUser = models.User.objects.get(email = "fbar@gmail.com").email
        badUser  = models.User.objects.get(email = "fbar").email

        self.assertIsInstance(goodUser,unicode)
        self.assertIsInstance(badUser, unicode)
        """
        Regex tests basic email format: ___@___.___
        """
        self.assertTrue(re.match(r"[^@]*@[^@]*\.[^@]{3}", goodUser))
        self.assertFalse(re.match(r"[^@]*@[^@]*\.[^@]{3}", badUser))

    def test_ValidFirstName(self):
        goodUserName = models.User.objects.get(email = "fbar@gmail.com").first_name
        badUserName  = models.User.objects.get(email = "fbar").first_name
        maxChars     = 50

        self.assertIsInstance(goodUserName,unicode)
        self.assertIsInstance(badUserName, unicode)
        """
        Regex to match a basic name with no extraneous numbers or special characters
        """
        self.assertTrue(re.match(r"^[A-Za-z/-]*$",goodUserName))
        self.assertTrue(len(goodUserName) <= maxChars and len(goodUserName) > 0)
        self.assertFalse(re.match(r"^[A-Za-z/-]*$", badUserName))
        self.assertFalse(len(badUserName) < maxChars)

    def test_ValidLastName(self):
        goodUserLast = models.User.objects.get(email = "fbar@gmail.com").last_name
        badUserLast  = models.User.objects.get(email = "fbar").last_name
        maxChars     = 50

        self.assertIsInstance(goodUserLast,unicode)
        self.assertIsInstance(badUserLast, unicode)
        """
        Regex to match a basic name with no extraneous numbers or special characters
        """
        self.assertTrue(re.match(r"^[A-Za-z/-]*$",goodUserLast))
        self.assertTrue(len(goodUserLast) <= maxChars and len(goodUserLast) > 0)
        self.assertFalse(re.match(r"^[A-Za-z/-]*$",badUserLast))
        self.assertFalse(len(badUserLast) < maxChars)

    def test_ValidDate(self):
        goodUserDate = models.User.objects.get(email = "fbar@gmail.com").joined_date
        badUserDate  = models.User.objects.get(email = "fbar").joined_date

        self.assertIsInstance(goodUserDate, datetime.datetime)

        """Will be changed to a time where the site will actually go live for accuracy"""

        dateOfProduction = datetime.datetime(2015,9,22)
        goodUserDate     = goodUserDate.replace(tzinfo=None)
        badUserDate      = badUserDate.replace(tzinfo=None)
        self.assertTrue(dateOfProduction < goodUserDate)
        self.assertFalse(dateOfProduction > badUserDate)

    def test_ValidPassword(self):
        goodUser = models.User.objects.get(email = "fbar@gmail.com")
        badUser  = models.User.objects.get(email = "fbar")
        goodUser.set_password("password")
        badUser.set_unusable_password()

        self.assertTrue(goodUser.has_usable_password())
        self.assertFalse(badUser.has_usable_password())
        self.assertTrue(goodUser.check_password("password"))
        self.assertFalse(badUser.check_password("password"))


class DemographicModelTests(TestCase):
    def setUp(self):
        models.DemographicData.objects.create(birthday           = datetime.datetime(1994,1,1,0,0,0,0),
                                              education          = random.randint(0,6),
                                              employmentStatus   = 'e',
                                              familySize         = random.randint(0,15),
                                              gender             = 'm',
                                              relationshipStatus = 's',
                                              postalCode         = "66503",
                                              race               = 'w',
                                              salary             = random.randint(0,5),
                                              sexual_orientation = 'w')

        models.DemographicData.objects.create(birthday           = datetime.datetime.now(),
                                              education          = 7,
                                              employmentStatus   = 'z',
                                              familySize         = 16,
                                              gender             = 'z',
                                              relationshipStatus = 'z',
                                              postalCode         = "ZIPCODE",
                                              race               = 'z',
                                              salary             = 6,
                                              sexual_orientation = 'z')

    """
    Used to find the option within the tuples in option lists
    """
    def findInTuple(self, character, options):
        for x in options:
            if(x[0] == character):
                return True
        return False

    def test_ValidBirthday(self):
        goodDate       = models.DemographicData.objects.get(postalCode = "66503").birthday
        badDate        = models.DemographicData.objects.get(postalCode = "ZIPCODE").birthday
        """
        Assuming nobody lives forever and also not a baby and using this, setting up some age limits for testing
        """
        dateOfOldAge   = datetime.date(1899,7,6)
        dateOfYoungAge = datetime.date(2001,9,23)

        self.assertIsInstance(goodDate,datetime.date)
        self.assertTrue(dateOfOldAge < goodDate)
        self.assertTrue(dateOfYoungAge > goodDate)
        self.assertFalse(dateOfYoungAge > badDate)

    def test_ValidEducation(self):
        goodEdu = models.DemographicData.objects.get(postalCode = "66503").education
        badEdu  = models.DemographicData.objects.get(postalCode = "ZIPCODE").education

        self.assertIn(goodEdu, models.DemographicData.EDUCATION[goodEdu])
        self.assertTrue(badEdu >= len(models.DemographicData.EDUCATION))

    def test_ValidEmployment(self):
        goodEmploy = models.DemographicData.objects.get(postalCode = "66503").employmentStatus
        badEmploy  = models.DemographicData.objects.get(postalCode = "ZIPCODE").employmentStatus

        self.assertTrue(self.findInTuple(goodEmploy, models.DemographicData.EMPLOYMENT_STATUS))
        self.assertFalse(self.findInTuple(badEmploy, models.DemographicData.EMPLOYMENT_STATUS))

    def test_ValidFamily(self):
        goodFamily = models.DemographicData.objects.get(postalCode = "66503").familySize
        badFamily  = models.DemographicData.objects.get(postalCode = "ZIPCODE").familySize

        """
        Setting arbitrary family limit at 15 for now, will probably change
        """
        self.assertTrue(goodFamily >= 0 and goodFamily <= 15)
        self.assertTrue(badFamily < 0 or badFamily > 15)

    def test_ValidGender(self):
        goodGen = models.DemographicData.objects.get(postalCode = "66503").gender
        badGen  = models.DemographicData.objects.get(postalCode = "ZIPCODE").gender

        self.assertTrue(self.findInTuple(goodGen, models.DemographicData.GENDER))
        self.assertFalse(self.findInTuple(badGen, models.DemographicData.GENDER))

    def test_ValidRelationship(self):
        goodRel = models.DemographicData.objects.get(postalCode = "66503").relationshipStatus
        badRel  = models.DemographicData.objects.get(postalCode = "ZIPCODE").relationshipStatus

        self.assertTrue(self.findInTuple(goodRel, models.DemographicData.RELATIONSHIP_STATUS))
        self.assertFalse(self.findInTuple(badRel, models.DemographicData.RELATIONSHIP_STATUS))

    def test_ValidPostalCode(self):
        goodPost = models.DemographicData.objects.get(postalCode = "66503").postalCode
        badPost  = models.DemographicData.objects.get(postalCode = "ZIPCODE").postalCode

        """
        Regex just checks for validity in zip code format either XXXXX-XXXX or XXXXX, where X is an integer
        """
        self.assertTrue(re.match(r"^[0-9]{5}-[0-9]{4}$|^[0-9]{5}$",goodPost))
        self.assertFalse(re.match(r"^[0-9]{5}-[0-9]{4}$|^[0-9]{5}$",badPost))

    def test_ValidRace(self):
        goodRace = models.DemographicData.objects.get(postalCode = "66503").race
        badRace  = models.DemographicData.objects.get(postalCode = "ZIPCODE").race

        self.assertTrue(self.findInTuple(goodRace, models.DemographicData.RACE))
        self.assertFalse(self.findInTuple(badRace, models.DemographicData.RACE))

    def test_ValidSalary(self):
        goodSalary = models.DemographicData.objects.get(postalCode = "66503").salary
        badSalary  = models.DemographicData.objects.get(postalCode = "ZIPCODE").salary

        self.assertIn(goodSalary, models.DemographicData.SALARY[goodSalary])
        self.assertFalse(badSalary < len(models.DemographicData.SALARY))

    def test_ValidSexualOrientation(self):
        goodSex = models.DemographicData.objects.get(postalCode = "66503").sexual_orientation
        badSex  = models.DemographicData.objects.get(postalCode = "ZIPCODE").sexual_orientation

        self.assertTrue(self.findInTuple(goodSex, models.DemographicData.SEXUAL_PREFERENCE))
        self.assertFalse(self.findInTuple(badSex, models.DemographicData.SEXUAL_PREFERENCE))


class ArticleModelTests(TestCase):
    def setUp(self):
        testUser = models.User.objects.create(email       = "fbar@gmail.com",
                                              first_name  = "Alex",
                                              last_name   = "Beahm",
                                              joined_date = datetime.datetime.now(),
                                              is_active   = True,
                                              confirmed   = True)
        models.Article.objects.create(title       = "SomeTitle",
                                      author      = testUser,
                                      content     = "Test content for the article",
                                      publishDate = datetime.datetime.now(),
                                      updateDate  = datetime.datetime.now())
        models.Article.objects.create(title       = "",
                                      author      = testUser,
                                      content     = "",
                                      publishDate = datetime.datetime.now(),
                                      updateDate  = datetime.datetime(2014,1,1))


    def test_ValidTitle(self):
        goodTitle = models.Article.objects.get(title = "SomeTitle").title
        badTitle  = models.Article.objects.get(title = "").title

        self.assertIsInstance(goodTitle,unicode)
        self.assertIsInstance(badTitle, unicode)
        self.assertTrue(len(goodTitle) > 0)
        self.assertFalse(len(badTitle) > 0)

    def test_ValidAuthor(self):
        goodUser = models.Article.objects.get(title = "SomeTitle").author
        self.assertIsInstance(goodUser, models.User)

    def test_ValidContent(self):
        goodContent = models.Article.objects.get(title = "SomeTitle").content
        badContent  = models.Article.objects.get(title = "").content

        self.assertIsInstance(goodContent,unicode)
        self.assertIsInstance(badContent, unicode)
        self.assertGreater(len(goodContent), 0)
        self.assertEqual(len(badContent), 0)

    def test_ValidDateInstances(self):
        goodPDate = models.Article.objects.get(title = "SomeTitle").publishDate
        badPDate  = models.Article.objects.get(title = "SomeTitle").publishDate
        goodUDate = models.Article.objects.get(title = "SomeTitle").updateDate
        badUDate  = models.Article.objects.get(title = "SomeTitle").updateDate

        self.assertIsInstance(goodPDate,datetime.date)
        self.assertIsInstance(goodUDate,datetime.date)
        self.assertFalse(badPDate < badUDate)
        self.assertTrue(goodPDate == goodUDate)


class TagModelTests(TestCase):
    def setUp(self):
        models.Tag.objects.create(tagName = "testTag")
        models.Tag.objects.create(tagName = "")

    def test_ValidTagName(self):
        goodTag = models.Tag.objects.get(tagName = "testTag").tagName
        badTag  = models.Tag.objects.get(tagName = "").tagName

        self.assertIsInstance(goodTag,unicode)
        self.assertIsInstance(badTag, unicode)
        self.assertGreater(len(goodTag), 0)
        self.assertFalse(len(badTag) > 0)


class TagTableModelTests(TestCase):
    def setUp(self):
        testUser    = models.User.objects.create(email      = "fbar@gmail.com",
                                                first_name  = "Alex",
                                                last_name   = "Beahm",
                                                joined_date = datetime.datetime.now(),
                                                is_active   = True,
                                                confirmed   = True)
        testArticle = models.Article.objects.create(title       = "SomeTitle",
                                                    author      = testUser,
                                                    content     = "Test content for the article",
                                                    publishDate = datetime.datetime.now(),
                                                    updateDate  = datetime.datetime.now())
        testTag     = models.Tag.objects.create(tagName = "testTag")

        models.TagTable.objects.create(article = testArticle, tag = testTag)

    def test_ValidArticle(self):
        goodArticle = models.TagTable.objects.get().article

        self.assertIsInstance(goodArticle, models.Article)

    def test_ValidTag(self):
        goodTag = models.TagTable.objects.get().tag

        self.assertIsInstance(goodTag, models.Tag)

