from django.conf.urls import url

from . import views

urlpatterns = [
#    url(r'^$', views.subscribe, name="subscribe"),
    url(r'^$', views.index, name="index"),
    url(r'^index$', views.index, name="index"),
    url(r'^register/$', views.register_user, name="register_user"),
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^contributors/$', views.contributors, name='contributors'),
    url(r'^userprofile/$', views.user_profile, name='user_profile'),
#    url(r'^contribprofile/$', )
]
