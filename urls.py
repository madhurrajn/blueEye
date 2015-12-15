from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^blueEye/', include('blueEye.urls', namespace="blueEye")),
    url(r'^admin/', include(admin_site.urls)),
]

admin.site.site_header='My Admin'
