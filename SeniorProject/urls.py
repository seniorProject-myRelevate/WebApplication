from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('MyRelevate.urls', namespace='myrelevate')),
    url(r'^admin/', include(admin.site.urls)),
]
