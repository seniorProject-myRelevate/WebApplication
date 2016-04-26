from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?i)register/$', views.register_user, name="register_user"),
    url(r'^(?i)new_confirm/$', views.new_confirm, name="new_confirm"),
    url(r'^(?i)confirm/$', views.confirm, name="confirm"),
    url(r'^(?i)login/$', views.login_view, name="login"),
    url(r'^(?i)logout/$', views.logout_view, name="logout"),
]
