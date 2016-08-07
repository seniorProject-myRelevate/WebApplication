from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.subscribe, name="subscribe"),
    url(r'^(?i)index/$', views.index, name="index"),

    # moving to a more modular setup in the near future
    url(r'^(?i)advisers/', include('MyRelevate.Advisers.urls', namespace='advisers')),
    url(r'^(?i)articles/', include('MyRelevate.Articles.urls', namespace='articles')),
    url(r'^(?i)auth/', include('MyRelevate.Auth.urls', namespace='auth')),
    url(r'^(?i)contributor/', include('MyRelevate.Contributor.urls', namespace='contributor')),
    url(r'^(?i)user/', include('MyRelevate.User.urls', namespace='user')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
