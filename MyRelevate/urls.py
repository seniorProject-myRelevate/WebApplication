from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.subscribe, name="subscribe"),
    url(r'^(?i)index/$', views.index, name="index"),
    url(r'^(?i)register/$', views.register_user, name="register_user"),
    url(r'^(?i)new_confirm/$', views.new_confirm, name="new_confirm"),
    url(r'^(?i)confirm/$', views.confirm, name="confirm"),
    url(r'^(?i)login/$', views.login_view, name="login"),
    url(r'^(?i)logout/$', views.logout_view, name="logout"),
    url(r'^(?i)userprofile/$', views.user_profile, name='user_profile'),

    # moving to a more modular setup in the near future
    url(r'^(?i)articles', include('MyRelevate.Articles.urls', namespace='articles')),
    url(r'^(?i)contributor', include('MyRelevate.Contributor.urls', namespace='contributor')),

]
