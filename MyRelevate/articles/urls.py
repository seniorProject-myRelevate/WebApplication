from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?i)/$', views.display, name="display"),
    url(r'^(?i)create/$', views.create, name="create"),
    url(r'^(?i)update/$', views.update, name="update"),
    url(r'^(?i)remove/$', views.remove, name="remove"),

]