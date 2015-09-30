import datetime
import re
import random
import models
from django.test import TestCase


class UserModelTests(TestCase):
    def setUp(self):
        models.User.objects.create(email="fbar@gmail.com",
                                   first_name="Alex",
                                   last_name="Beahm",
                                   joined_date=datetime.datetime.now(),
                                   is_active=True,
                                   confirmed=True)
        models.User.objects.create(email="fbar",
                                   first_name="Thisnameiswaytoolongbecauseitisgreaterthanfiftycharactersandcontainsnumbersandspecialcharacters3344$$",
                                   last_name="Thislastnameisalsowaytoolongbecauseitisgreaterthanfiftycharactersandcontainsnumbersandspecialcharacters55%^  F",
                                   joined_date=datetime.datetime(2011, 1, 1, 0, 0, 0, 0),
                                   is_active=False,
                                   confirmed=False)

        models.User.objects.get(email="fbar@gmail.com").set_password("password")
        models.User.objects.get(email="fbar").set_unusable_password()

    def test_ValidEmail(self):
        """
        Regex is used to just check if the e-mail is in a correct format
        """
        goodUser = models.User.objects.get(email="fbar@gmail.com").email
        badUser = models.User.objects.get(email="fbar").email

        self.assertIsInstance(goodUser, unicode)
        self.assertIsInstance(badUser, unicode)
        """
        Regex tests basic email format: ___@___.___
        """
        self.assertTrue(re.match(r"[^@]*@[^@]*\.[^@]{3}", goodUser))
        self.assertFalse(re.match(r"[^@]*@[^@]*\.[^@]{3}", badUser))

    def test_ValidFirstName(self):
        goodUserName = models.User.objects.get(email="fbar@gmail.com").first_name
        badUserName = models.User.objects.get(email="fbar").first_name
        maxChars = 50

        self.assertIsInstance(goodUserName, unicode)
        self.assertIsInstance(badUserName, unicode)
        """
        Regex to match a basic name with no extraneous numbers or special characters
        """
        self.assertTrue(re.match(r"^[A-Za-z/-]*$", goodUserName))
        self.assertTrue(len(goodUserName) <= maxChars and len(goodUserName) > 0)
        self.assertFalse(re.match(r"^[A-Za-z/-]*$", badUserName))
        self.assertFalse(len(badUserName) < maxChars)

    def test_ValidLastName(self):
        goodUserLast = models.User.objects.get(email="fbar@gmail.com").last_name
        badUserLast = models.User.objects.get(email="fbar").last_name
        maxChars = 50

        self.assertIsInstance(goodUserLast, unicode)
        self.assertIsInstance(badUserLast, unicode)
        """
        Regex to match a basic name with no extraneous numbers or special characters
        """
        self.assertTrue(re.match(r"^[A-Za-z/-]*$", goodUserLast))
        self.assertTrue(len(goodUserLast) <= maxChars and len(goodUserLast) > 0)
        self.assertFalse(re.match(r"^[A-Za-z/-]*$", badUserLast))
        self.assertFalse(len(badUserLast) < maxChars)

    def test_ValidDate(self):
        goodUserDate = models.User.objects.get(email="fbar@gmail.com").joined_date
        badUserDate = models.User.objects.get(email="fbar").joined_date

        self.assertIsInstance(goodUserDate, datetime.datetime)

        """Will be changed to a time where the site will actually go live for accuracy"""

        dateOfProduction = datetime.datetime(2015, 9, 22)
        goodUserDate = goodUserDate.replace(tzinfo=None)
        badUserDate = badUserDate.replace(tzinfo=None)
        self.assertTrue(dateOfProduction < goodUserDate)
        self.assertFalse(dateOfProduction > badUserDate)

    def test_ValidPassword(self):
        goodUser = models.User.objects.get(email="fbar@gmail.com")
        badUser = models.User.objects.get(email="fbar")
        goodUser.set_password("password")
        badUser.set_unusable_password()

        self.assertTrue(goodUser.has_usable_password())
        self.assertFalse(badUser.has_usable_password())
        self.assertTrue(goodUser.check_password("password"))
        self.assertFalse(badUser.check_password("password"))


class DemographicModelTests(TestCase):
    def setUp(self):
        testUser = models.User.objects.create(email="fbar@gmail.com",
                                   first_name="Alex",
                                   last_name="Beahm",
                                   joined_date=datetime.datetime.now(),
                                   is_active=True,
                                   confirmed=True)
        models.DemographicData.objects.create(user = testUser,
                                              birthday=datetime.datetime(1994, 1, 1, 0, 0, 0, 0),
                                              education=random.randint(0, 6),
                                              employmentStatus='n',
                                              familySize=random.randint(0, 15),
                                              sex = 'm',
                                              relationshipStatus='s',
                                              postalCode="66503",
                                              race='w',
                                              salary=random.randint(0, 5),
                                              sexualPreference='w',
                                              religion='c',
                                              religiousInfluence=random.randint(0, 4),
                                              addictive='n',
                                              violence='n',
                                              breakups='n',
                                              verbalEmotionalAbuse='n',
                                              infidelity='n',
                                              addictiveOther='n',
                                              violenceOther='n',
                                              breakupsOther='n',
                                              verbalEmotionalAbuseOther='n',
                                              infidelityOther='n',
                                              cyclicRelationships=False,
                                              timesCycled=0,
                                              timesMarried=0,
                                              biologicalChildren=0,
                                              adoptedChildren=0,
                                              stepChildren=0,
                                              lengthOfCurrentRelationship=0,
                                              currentRelationshipHappiness=random.randint(0, 4),
                                              gettingDivorced=False)

        models.DemographicData.objects.create(user = testUser,
                                              birthday=datetime.datetime.now(),
                                              education=7,
                                              employmentStatus='z',
                                              familySize=16,
                                              sex='z',
                                              relationshipStatus='z',
                                              postalCode="ZIPCODE",
                                              race='z',
                                              salary=6,
                                              sexualPreference='z',
                                              religion='z',
                                              religiousInfluence=-1,
                                              addictive='z',
                                              violence='z',
                                              breakups='z',
                                              verbalEmotionalAbuse='z',
                                              infidelity='z',
                                              addictiveOther='z',
                                              violenceOther='z',
                                              breakupsOther='z',
                                              verbalEmotionalAbuseOther='z',
                                              infidelityOther='z',
                                              cyclicRelationships=True,
                                              timesCycled=-1,
                                              timesMarried=-1,
                                              biologicalChildren=-1,
                                              adoptedChildren=-1,
                                              stepChildren=-1,
                                              lengthOfCurrentRelationship=-1,
                                              currentRelationshipHappiness=-1,
                                              gettingDivorced=True)


    """
    Used to find the option within the tuples in option lists
    """

    def findInTuple(self, character, options):
        for x in options:
            if x[0] == character:
                return True
        return False

    def test_ValidUsers(self):
        goodUser = models.DemographicData.objects.get(postalCode="66503").user
        otherUser = models.DemographicData.objects.get(postalCode="ZIPCODE").user
        goodUserID = models.DemographicData.objects.get(postalCode="66503").user_id
        otherUserID = models.DemographicData.objects.get(postalCode="ZIPCODE").user_id

        self.assertIsInstance(goodUser, models.User)
        self.assertIsInstance(otherUser, models.User)
        self.assertNotEqual(goodUserID, otherUserID)


    def test_ValidBirthday(self):
        goodDate = models.DemographicData.objects.get(postalCode="66503").birthday
        badDate = models.DemographicData.objects.get(postalCode="ZIPCODE").birthday
        """
        Assuming nobody lives forever and also not a baby and using this, setting up some age limits for testing
        """
        dateOfOldAge = datetime.date(1899, 7, 6)
        dateOfYoungAge = datetime.date(2001, 9, 23)

        self.assertIsInstance(goodDate, datetime.date)
        self.assertTrue(dateOfOldAge < goodDate)
        self.assertTrue(dateOfYoungAge > goodDate)
        self.assertFalse(dateOfYoungAge > badDate)

    def test_ValidEducation(self):
        goodEdu = models.DemographicData.objects.get(postalCode="66503").education
        badEdu = models.DemographicData.objects.get(postalCode="ZIPCODE").education

        self.assertIn(goodEdu, models.DemographicData.EDUCATION[goodEdu])
        self.assertTrue(badEdu >= len(models.DemographicData.EDUCATION))

    def test_ValidEmployment(self):
        goodEmploy = models.DemographicData.objects.get(postalCode="66503").employmentStatus
        badEmploy = models.DemographicData.objects.get(postalCode="ZIPCODE").employmentStatus

        self.assertTrue(self.findInTuple(goodEmploy, models.DemographicData.EMPLOYMENT_STATUS))
        self.assertFalse(self.findInTuple(badEmploy, models.DemographicData.EMPLOYMENT_STATUS))

    def test_ValidFamily(self):
        goodFamily = models.DemographicData.objects.get(postalCode="66503").familySize
        badFamily = models.DemographicData.objects.get(postalCode="ZIPCODE").familySize

        """
        Setting arbitrary family limit at 15 for now, will probably change
        """
        self.assertTrue(goodFamily >= 0 and goodFamily <= 15)
        self.assertTrue(badFamily < 0 or badFamily > 15)

    def test_ValidSex(self):
        goodSex = models.DemographicData.objects.get(postalCode="66503").sex
        badSex = models.DemographicData.objects.get(postalCode="ZIPCODE").sex

        self.assertTrue(self.findInTuple(goodSex, models.DemographicData.SEX))
        self.assertFalse(self.findInTuple(badSex, models.DemographicData.SEX))


    def test_ValidRelationship(self):
        goodRel = models.DemographicData.objects.get(postalCode="66503").relationshipStatus
        badRel = models.DemographicData.objects.get(postalCode="ZIPCODE").relationshipStatus

        self.assertTrue(self.findInTuple(goodRel, models.DemographicData.RELATIONSHIP_STATUS))
        self.assertFalse(self.findInTuple(badRel, models.DemographicData.RELATIONSHIP_STATUS))

    def test_ValidPostalCode(self):
        goodPost = models.DemographicData.objects.get(postalCode="66503").postalCode
        badPost = models.DemographicData.objects.get(postalCode="ZIPCODE").postalCode

        """
        Regex just checks for validity in zip code format either XXXXX-XXXX or XXXXX, where X is an integer
        """
        self.assertTrue(re.match(r"^[0-9]{5}-[0-9]{4}$|^[0-9]{5}$", goodPost))
        self.assertFalse(re.match(r"^[0-9]{5}-[0-9]{4}$|^[0-9]{5}$", badPost))

    def test_ValidRace(self):
        goodRace = models.DemographicData.objects.get(postalCode="66503").race
        badRace = models.DemographicData.objects.get(postalCode="ZIPCODE").race

        self.assertTrue(self.findInTuple(goodRace, models.DemographicData.RACE))
        self.assertFalse(self.findInTuple(badRace, models.DemographicData.RACE))

    def test_ValidSalary(self):
        goodSalary = models.DemographicData.objects.get(postalCode="66503").salary
        badSalary = models.DemographicData.objects.get(postalCode="ZIPCODE").salary

        self.assertIn(goodSalary, models.DemographicData.SALARY[goodSalary])
        self.assertFalse(badSalary < len(models.DemographicData.SALARY))

    def test_ValidSexualOrientation(self):
        goodSex = models.DemographicData.objects.get(postalCode="66503").sexualPreference
        badSex = models.DemographicData.objects.get(postalCode="ZIPCODE").sexualPreference

        self.assertTrue(self.findInTuple(goodSex, models.DemographicData.SEXUAL_PREFERENCE))
        self.assertFalse(self.findInTuple(badSex, models.DemographicData.SEXUAL_PREFERENCE))

    def test_ValidReligion(self):
        goodReli = models.DemographicData.objects.get(postalCode="66503").religion
        badReli = models.DemographicData.objects.get(postalCode="ZIPCODE").religion

        self.assertTrue(self.findInTuple(goodReli, models.DemographicData.RELIGION))
        self.assertFalse(self.findInTuple(badReli, models.DemographicData.RELIGION))

    def test_ValidReligionInfluence(self):
        goodReliI = models.DemographicData.objects.get(postalCode="66503").religiousInfluence
        badReliI = models.DemographicData.objects.get(postalCode="ZIPCODE").religiousInfluence

        self.assertTrue(self.findInTuple(goodReliI, models.DemographicData.AGREEMENT))
        self.assertFalse(self.findInTuple(badReliI, models.DemographicData.AGREEMENT))

    def test_ValidAddiction(self):
        goodAdd = models.DemographicData.objects.get(postalCode="66503").addictive
        goodAddOther = models.DemographicData.objects.get(postalCode="66503").addictiveOther
        badAdd = models.DemographicData.objects.get(postalCode="ZIPCODE").addictive
        badAddOther = models.DemographicData.objects.get(postalCode="ZIPCODE").addictiveOther

        self.assertTrue(self.findInTuple(goodAdd, models.DemographicData.FREQUENCY))
        self.assertFalse(self.findInTuple(badAdd, models.DemographicData.FREQUENCY))
        self.assertTrue(self.findInTuple(goodAddOther, models.DemographicData.FREQUENCY))
        self.assertFalse(self.findInTuple(badAddOther, models.DemographicData.FREQUENCY))

    def test_ValidViolence(self):
        goodViol = models.DemographicData.objects.get(postalCode="66503").violence
        goodViolOther = models.DemographicData.objects.get(postalCode="66503").violenceOther
        badViol = models.DemographicData.objects.get(postalCode="ZIPCODE").violence
        badViolOther = models.DemographicData.objects.get(postalCode="ZIPCODE").violenceOther

        self.assertTrue(self.findInTuple(goodViol, models.DemographicData.FREQUENCY))
        self.assertFalse(self.findInTuple(badViol, models.DemographicData.FREQUENCY))
        self.assertTrue(self.findInTuple(goodViolOther, models.DemographicData.FREQUENCY))
        self.assertFalse(self.findInTuple(badViolOther, models.DemographicData.FREQUENCY))

    def test_ValidBreakups(self):
        goodBreak = models.DemographicData.objects.get(postalCode="66503").breakups
        goodBreakOther = models.DemographicData.objects.get(postalCode="66503").breakupsOther
        badBreak = models.DemographicData.objects.get(postalCode="ZIPCODE").breakups
        badBreakOther = models.DemographicData.objects.get(postalCode="ZIPCODE").breakupsOther

        self.assertTrue(self.findInTuple(goodBreak, models.DemographicData.FREQUENCY))
        self.assertFalse(self.findInTuple(badBreak, models.DemographicData.FREQUENCY))
        self.assertTrue(self.findInTuple(goodBreakOther, models.DemographicData.FREQUENCY))
        self.assertFalse(self.findInTuple(badBreakOther, models.DemographicData.FREQUENCY))

    def test_ValidEmotion(self):
        goodEmote = models.DemographicData.objects.get(postalCode="66503").verbalEmotionalAbuse
        goodEmoteOther = models.DemographicData.objects.get(postalCode="66503").verbalEmotionalAbuseOther
        badEmote = models.DemographicData.objects.get(postalCode="ZIPCODE").verbalEmotionalAbuse
        badEmoteOther = models.DemographicData.objects.get(postalCode="ZIPCODE").verbalEmotionalAbuseOther

        self.assertTrue(self.findInTuple(goodEmote, models.DemographicData.FREQUENCY))
        self.assertFalse(self.findInTuple(badEmote, models.DemographicData.FREQUENCY))
        self.assertTrue(self.findInTuple(goodEmoteOther, models.DemographicData.FREQUENCY))
        self.assertFalse(self.findInTuple(badEmoteOther, models.DemographicData.FREQUENCY))

    def test_ValidInfidelity(self):
        goodInf = models.DemographicData.objects.get(postalCode="66503").infidelity
        goodInfOther = models.DemographicData.objects.get(postalCode="66503").infidelityOther
        badInf = models.DemographicData.objects.get(postalCode="ZIPCODE").infidelity
        badInfOther = models.DemographicData.objects.get(postalCode="ZIPCODE").infidelityOther

        self.assertTrue(self.findInTuple(goodInf, models.DemographicData.FREQUENCY))
        self.assertFalse(self.findInTuple(badInf, models.DemographicData.FREQUENCY))
        self.assertTrue(self.findInTuple(goodInfOther, models.DemographicData.FREQUENCY))
        self.assertFalse(self.findInTuple(badInfOther, models.DemographicData.FREQUENCY))

    def test_ValidCyclicRelationships(self):
        goodCycle = models.DemographicData.objects.get(postalCode="66503").cyclicRelationships
        badCycle = models.DemographicData.objects.get(postalCode="ZIPCODE").cyclicRelationships

        self.assertIsInstance(goodCycle,bool)
        self.assertIsInstance(badCycle,bool)
        self.assertFalse(goodCycle)
        self.assertTrue(badCycle)

    def test_ValidTimesCycled(self):
        goodCycle = models.DemographicData.objects.get(postalCode="66503").timesCycled
        badCycle = models.DemographicData.objects.get(postalCode="ZIPCODE").timesCycled

        self.assertIsInstance(goodCycle,int)
        self.assertIsInstance(badCycle,int)
        self.assertGreaterEqual(goodCycle, 0)
        self.assertLess(badCycle, 0)

    def test_ValidTimesMarried(self):
        goodMarry = models.DemographicData.objects.get(postalCode="66503").timesMarried
        badMarry = models.DemographicData.objects.get(postalCode="ZIPCODE").timesMarried

        self.assertIsInstance(goodMarry, int)
        self.assertIsInstance(badMarry, int)
        self.assertGreaterEqual(goodMarry, 0)
        self.assertLess(badMarry, 0)

    def test_ValidBiologicalChildren(self):
        goodBio = models.DemographicData.objects.get(postalCode="66503").biologicalChildren
        badBio = models.DemographicData.objects.get(postalCode="ZIPCODE").biologicalChildren

        self.assertIsInstance(goodBio, int)
        self.assertIsInstance(badBio, int)
        self.assertGreaterEqual(goodBio, 0)
        self.assertLess(badBio, 0)

    def test_ValidAdoptedChildren(self):
        goodAdopt = models.DemographicData.objects.get(postalCode="66503").adoptedChildren
        badAdopt = models.DemographicData.objects.get(postalCode="ZIPCODE").adoptedChildren

        self.assertIsInstance(goodAdopt, int)
        self.assertIsInstance(badAdopt, int)
        self.assertGreaterEqual(goodAdopt, 0)
        self.assertLess(badAdopt, 0)

    def test_ValidStepChildren(self):
        goodStep = models.DemographicData.objects.get(postalCode="66503").stepChildren
        badStep = models.DemographicData.objects.get(postalCode="ZIPCODE").stepChildren

        self.assertIsInstance(goodStep, int)
        self.assertIsInstance(badStep, int)
        self.assertGreaterEqual(goodStep, 0)
        self.assertLess(badStep, 0)

    def test_ValidLengthOfCurrentRelationship(self):
        goodLength = models.DemographicData.objects.get(postalCode="66503").lengthOfCurrentRelationship
        badLength = models.DemographicData.objects.get(postalCode="ZIPCODE").lengthOfCurrentRelationship

        self.assertIsInstance(goodLength, int)
        self.assertIsInstance(badLength, int)
        self.assertGreaterEqual(goodLength, 0)
        self.assertLess(badLength, 0)

    def test_ValidCurrentRelationshipHappiness(self):
        goodHappy = models.DemographicData.objects.get(postalCode="66503").currentRelationshipHappiness
        badHappy = models.DemographicData.objects.get(postalCode="ZIPCODE").currentRelationshipHappiness

        self.assertIsInstance(goodHappy, int)
        self.assertIsInstance(badHappy, int)
        self.assertTrue(self.findInTuple(goodHappy,models.DemographicData.AGREEMENT))
        self.assertFalse(self.findInTuple(badHappy,models.DemographicData.AGREEMENT))


    def test_ValidDivorce(self):
        goodDiv = models.DemographicData.objects.get(postalCode="66503").gettingDivorced
        badDiv = models.DemographicData.objects.get(postalCode="ZIPCODE").gettingDivorced

        self.assertIsInstance(goodDiv,bool)
        self.assertIsInstance(badDiv,bool)
        self.assertFalse(goodDiv)
        self.assertTrue(badDiv)


class ArticleModelTests(TestCase):
    def setUp(self):
        testUser = models.User.objects.create(email="fbar@gmail.com",
                                              first_name="Alex",
                                              last_name="Beahm",
                                              joined_date=datetime.datetime.now(),
                                              is_active=True,
                                              confirmed=True)
        models.Article.objects.create(title="SomeTitle",
                                      author=testUser,
                                      content="Test content for the article",
                                      publishDate=datetime.datetime.now(),
                                      updateDate=datetime.datetime.now())
        models.Article.objects.create(title="",
                                      author=testUser,
                                      content="",
                                      publishDate=datetime.datetime.now(),
                                      updateDate=datetime.datetime(2014, 1, 1))

    def test_ValidTitle(self):
        goodTitle = models.Article.objects.get(title="SomeTitle").title
        badTitle = models.Article.objects.get(title="").title

        self.assertIsInstance(goodTitle, unicode)
        self.assertIsInstance(badTitle, unicode)
        self.assertTrue(len(goodTitle) > 0)
        self.assertFalse(len(badTitle) > 0)

    def test_ValidAuthor(self):
        goodUser = models.Article.objects.get(title="SomeTitle").author
        self.assertIsInstance(goodUser, models.User)

    def test_ValidContent(self):
        goodContent = models.Article.objects.get(title="SomeTitle").content
        badContent = models.Article.objects.get(title="").content

        self.assertIsInstance(goodContent, unicode)
        self.assertIsInstance(badContent, unicode)
        self.assertGreater(len(goodContent), 0)
        self.assertEqual(len(badContent), 0)

    def test_ValidDateInstances(self):
        goodPDate = models.Article.objects.get(title="SomeTitle").publishDate
        badPDate = models.Article.objects.get(title="SomeTitle").publishDate
        goodUDate = models.Article.objects.get(title="SomeTitle").updateDate
        badUDate = models.Article.objects.get(title="SomeTitle").updateDate

        self.assertIsInstance(goodPDate, datetime.date)
        self.assertIsInstance(goodUDate, datetime.date)
        self.assertFalse(badPDate < badUDate)
        self.assertTrue(goodPDate == goodUDate)


class TagModelTests(TestCase):
    def setUp(self):
        models.Tag.objects.create(tagName="testTag")
        models.Tag.objects.create(tagName="")

    def test_ValidTagName(self):
        goodTag = models.Tag.objects.get(tagName="testTag").tagName
        badTag = models.Tag.objects.get(tagName="").tagName

        self.assertIsInstance(goodTag, unicode)
        self.assertIsInstance(badTag, unicode)
        self.assertGreater(len(goodTag), 0)
        self.assertFalse(len(badTag) > 0)


class TagTableModelTests(TestCase):
    def setUp(self):
        testUser = models.User.objects.create(email="fbar@gmail.com",
                                              first_name="Alex",
                                              last_name="Beahm",
                                              joined_date=datetime.datetime.now(),
                                              is_active=True,
                                              confirmed=True)
        testArticle = models.Article.objects.create(title="SomeTitle",
                                                    author=testUser,
                                                    content="Test content for the article",
                                                    publishDate=datetime.datetime.now(),
                                                    updateDate=datetime.datetime.now())
        testTag = models.Tag.objects.create(tagName="testTag")

        models.TagTable.objects.create(article=testArticle, tag=testTag)

    def test_ValidArticle(self):
        goodArticle = models.TagTable.objects.get().article

        self.assertIsInstance(goodArticle, models.Article)

    def test_ValidTag(self):
        goodTag = models.TagTable.objects.get().tag

        self.assertIsInstance(goodTag, models.Tag)

class IndexViewTests(TestCase):
    def test_call_view_denies_anonymous(self):
        response = self.client.get('/url/to/view', follow=True)
        self.assertRedirects(response, '/login/')
        response = self.client.post('/url/to/view', follow=True)
        self.assertRedirects(response, '/login/')

    def test_call_view_loads(self):
        self.client.login(user='ajbeahm@ksu.edu', password='password')
        response = self.client.get('index')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_call_view_fails_blank(self):
        self.client.login(username='user', password='test')
        response = self.client.post('index', {}) # blank data dictionary
        self.assertFormError(response, 'index.html', 'some_field', 'This field is required.')

