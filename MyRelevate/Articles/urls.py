from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?i)$', views.index, name="display"),
    url(r'^(?i)create/$', views.create, name="create"),
    url(r'^(?i)update/$', views.update, name="update"),
    url(r'^(?i)remove/$', views.remove, name="remove"),
    url(r'^(?i)create/topic', views.articleTopics, name="articleTopics")

]
