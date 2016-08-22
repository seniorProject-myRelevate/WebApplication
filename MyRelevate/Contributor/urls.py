from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?i)/$', views.index, name="index"),
    url(r'^(?i)approve/$', views.approve, name="approve"),
    url(r'^(?i)create/$', views.create, name="create"),
    url(r'^(?i)update/$', views.update, name="update"),
    url(r'^(?i)update/degree/$', views.update_degree, name="updateDegree"),
    url(r'^(?i)upadate/program/$', views.update_program, name="updateProgram"),
    url(r'^(?i)update/expertise/$', views.update_area_of_expertise, name="updateAreaOfExpertise"),
    url(r'^(?i)update/biography/$', views.update_biography, name="updateBiography"),
    url(r'^(?i)update/interest/$', views.update_interest, name="updateInterest"),
    url(r'^(?i)update/contact/$', views.update_contact, name="updateContact"),
    url(r'^(?i)update/avatar/$', views.update_avatar, name="updateAvatar"),
    url(r'^(?i)update/resume/$', views.update_cv_resume, name="updateCVResume"),
    # url(r'^(?i)remove/$', views.remove, name="remove"),


    url(r'^(?i)contributors/$', views.contributors, name='contributors'),
]
