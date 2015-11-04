from django.contrib import admin

from .models import UserProfile, ContributorProfile


# Register your models here.

admin.site.register(UserProfile)
admin.site.register(ContributorProfile)
