from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from SeniorProject import settings
from ..Advisers.models import Advisers
from ..Contributor.models import ContributorProfile


class UserManager(BaseUserManager):

    class Meta:
        db_table = 'usermanager'

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser,
                          last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    is_staff = models.BooleanField(default=False)
    is_active = \
        models.BooleanField(default=True,
                            help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField(default=timezone.now)
    confirmed = models.BooleanField(default=False)
    is_adviser = models.BooleanField(default=False)
    is_contributor = models.BooleanField(default=False)
    adviser_profile = models.OneToOneField(Advisers, null=True, blank=True)
    contributor_profile = models.OneToOneField(ContributorProfile, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __unicode__(self):
        return self.email

    def get_contributor_profile(self):
        if self.is_contributor:
            return self.contributor_profile
        raise ValueError('User is not a contributor')

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(settings.SECRET_KEY, expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(settings.SECRET_KEY)
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        self.save()
        return True

    def new_confirm(self):
        if self.confirmed:
            return True
        self.confirmed = True
        self.save()
        return True
