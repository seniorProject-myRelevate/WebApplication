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
    url(r'^(?i)contributors/$', views.contributors, name='contributors'),
    url(r'^(?i)userprofile/$', views.user_profile, name='user_profile'),
    url(r'^(?i)contributorprofile', views.contributor_profile, name='contributor_profile'),
    url(r'^(?i)articles', views.articles, name='articles'),

    # moving to a more modular setup in the near future
    # url(r'^articles/', include('MyRelevate.articles.urls', namespace='articles')),

]
