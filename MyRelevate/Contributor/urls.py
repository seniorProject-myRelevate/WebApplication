from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?i)/$', views.index, name="index"),
    url(r'^(?i)create/$', views.create, name="create"),
    url(r'^(?i)update/$', views.update, name="update"),
    # url(r'^(?i)remove/$', views.remove, name="remove"),


    url(r'^(?i)contributors/$', views.contributors, name='contributors'),
    # url(r'^(?i)contributorprofile', views.contributor_profile, name='contributor_profile'),
    # url(r'^(?i)application/$', views.application, name='application'),
    url(r'^user/(?P<email>[/^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+])/$', views.user_detail),

]
