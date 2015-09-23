from django.test import TestCase
import datetime
import re

from .models import User


class UserTests(TestCase):
    def setUp(self):
        User.objects.create(email="fbar@gmail.com", first_name="Alex", last_name="Beahm",
                            joined_date=datetime.datetime.now(), is_active=True, confirmed=True)
        User.objects.create(email="fbar",
                            first_name="Thisnameiswaytoolongbecauseitisgreaterthanfiftycharactersandcontainsnumbersandspecialcharacters",
                            last_name="Thislastnameisalsowaytoolongbecauseitisgreaterthanfiftycharactersandcontainsnumbersandspecialcharacters",
                            joined_date=datetime.datetime(2011,1,1,0,0,0,0), is_active=False, is_confirmed=False)

    def validEmail(self):
        """
        Regex is used to just check if the e-mail is in a correct format
        """
        goodUser = User.objects.get(email="fbar@gmail.com")
        badUser = User.objects.get(email="bar")

        self.assertTrue(re.match(r"[^@]+@[^@]+\.[^@]+", goodUser['email']))
        self.assertFalse(re.match(r"[^@]+@[^@]+\.[^@]+", badUser['email']))

    def validFirstName(self):
        goodUserName = User.objects.get(email="fbar@gmail.com")['first_name']
        badUserName = User.objects.get(email="bar")['first_name']
        maxChars = 50
        self.assertTrue(re.match(r"^[A-Za-z/-]*$"),goodUserName)
        self.assertTrue(len(goodUserName) <= maxChars and not len(goodUserName))

        self.assertFalse(re.match(r"^[A-Za-z/-]*$"), badUserName)
        self.assertFalse(len(badUserName) <= maxChars)

    def validLastName(self):
        goodUserLast = User.objects.get(email="fbar@gmail.com")
        badUserLast = User.objects.get(email="bar")

        maxChars = 50
        self.assertTrue(re.match(r"^[A-Za-z/-]*$"),goodUserLast)
        self.assertTrue(len(goodUserLast) <= maxChars and not len(goodUserLast))

        self.assertFalse(re.match(r"^[A-Za-z/-]*$"),badUserLast)
        self.assertFalse(len(badUserLast) <= maxChars)

    def validDate(self):
        goodUserDate = User.objects.get(email="fbar@gmail.com")['joined_date']
        badUserDate = User.objects.get(email="bar")['joined_date']

        self.assertIsInstance(goodUserDate, datetime)

        """Will be changed to a time where the site will actually go live for accuracya"""
        dateOfProduction = datetime.datetime(2015,9,22,0,0,0,0)

        self.assertTrue(dateOfProduction < goodUserDate)
        self.assertFalse(dateOfProduction > badUserDate)
