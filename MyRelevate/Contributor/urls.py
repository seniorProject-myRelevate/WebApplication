from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?i)/$', views.index, name="index"),
    url(r'^(?i)approve/$', views.approve, name="approve"),
    url(r'^(?i)create/$', views.create, name="create"),
    url(r'^(?i)update/$', views.update, name="update"),
    url(r'^(?i)update/credentials/$', views.update_credentials, name="updateCredentials"),
    url(r'^(?i)update/expertise/$', views.update_area_of_expertise, name="updateAreaOfExpertise"),
    url(r'^(?i)update/biography/$', views.update_biography, name="updateBiography"),
    url(r'^(?i)update/interest/$', views.update_interest, name="updateInterest"),
    url(r'^(?i)update/contact/$', views.update_contact, name="updateContact"),
    # url(r'^(?i)remove/$', views.remove, name="remove"),


    url(r'^(?i)contributors/$', views.contributors, name='contributors'),
    # url(r'^(?i)contributorprofile', views.contributor_profile, name='contributor_profile'),
    # url(r'^(?i)application/$', views.application, name='application'),
    url(r'^(?i)resume/$', views.show_resume, name='showResume'),

]
