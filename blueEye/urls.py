from django.conf.urls import patterns, include
#from myproject.admin import admin_site
from views import empty

#urlpatterns = patterns('',
#    (r'^blueadmin/', include(blueadmin.site.urls)),
#)

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^showSchedule/$', views.showSchedule, name='showSchedule'),
    url(r'^showSchedule/change/(?P<cell_name>\w+)/(?P<pk>\d+)/$', views.changeSchedule, name='changeSchedule'),
    url(r'^showSchedule/delete/(?P<cell_name>\w+)/(?P<pk>\d+)/$', views.deleteSchedule, name='deleteSchedule'),
    url(r'^showSchedule/save/$', views.saveSchedule, name='saveSchedule'),
    url(r'^showSchedule/add/(?P<cell_name>\w+)/$', views.addSchedule, name='addSchedule'),
    url(r'^showSchedule/change/(?P<cell_name>\w+)/(?P<pk>\d+>)/$', views.showSchedule, name='showSchedule'),
    url(r'^$', views.addNewCell, name='addNewCell'),
    url(r'^empty$', empty, name='empty')
]

