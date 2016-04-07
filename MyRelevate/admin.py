from django.contrib import admin

from .models import ContributorProfile, Subscriber


# Register your models.py here.

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email',)
    inlines = []

    def email(self, instance):
        return instance.email

admin.site.register(ContributorProfile)
admin.site.register(Subscriber, SubscriberAdmin)
