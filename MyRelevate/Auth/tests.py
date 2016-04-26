from django.test import TestCase

from forms import RegistrationForm


class TestRegistrationForm(TestCase):
    def test_RegistrationForm(self):
        # Valid Data
        self.assertTrue(RegistrationForm(data={'email': 'test@test.com', 'first_name': 'My', 'last_name': 'relevate',
                                               'password1': 'MyR3l3v4t3', 'password2': 'MyR3l3v4t3'}).is_valid())

        # Invalid Data
        self.assertFalse(
            RegistrationForm(data={'username': 'test@test.com', 'first_name': 'My', 'last_name': 'relevate',
                                   'password1': 'MyR3l3v4t3', 'password2': 'MyR3l3v4t3'}).is_valid())

        self.assertFalse(RegistrationForm(data={'email': 'test.com', 'first_name': 'My', 'last_name': 'relevate',
                                                'password1': 'MyR3l3v4t3', 'password2': 'MyR3l3v4t3'}).is_valid())
