from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?i)/$', views.index, name="index"),
    url(r'^(?i)advisers/$', views.advisers, name="advisers"),
    url(r'^(?i)approve/$', views.approve, name="approve"),
    url(r'^(?i)create/$', views.create, name="create"),
    url(r'^(?i)update/$', views.update, name="update"),
]
