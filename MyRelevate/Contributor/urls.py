from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?i)/$', views.index, name="index"),
    url(r'^(?i)approve/$', views.approve, name="approve"),
    url(r'^(?i)create/$', views.create, name="create"),
    url(r'^(?i)update/$', views.update, name="update"),
    url(r'^(?i)update/credentials/$', views.updateCredentials, name="updateCredentials"),
    url(r'^(?i)update/expertise/$', views.updateAreaOfExpertise, name="updateAreaOfExpertise"),
    url(r'^(?i)update/biography/$', views.updateBiography, name="updateBiography"),
    url(r'^(?i)update/interest/$', views.updateInterest, name="updateInterest"),
    url(r'^(?i)update/contact/$', views.updateContact, name="updateContact"),
    # url(r'^(?i)remove/$', views.remove, name="remove"),


    url(r'^(?i)contributors/$', views.contributors, name='contributors'),
    # url(r'^(?i)contributorprofile', views.contributor_profile, name='contributor_profile'),
    # url(r'^(?i)application/$', views.application, name='application'),
    url(r'^(?i)showpdf/$', views.showpdf, name='showpdf'),

]
