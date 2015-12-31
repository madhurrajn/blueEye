from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import CellInfo, CompareCell, busyHourDaily
from django.utils.translation import ugettext_lazy

# Register your models here.


class MyAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('blueEye admin')

    # Text to put in each page's <h1>.
    site_header = ugettext_lazy('blueEye administration')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('blue Site administration')

admin_site = MyAdminSite(name='blueadmin')

admin.site.register(CellInfo)
admin_site.register(CellInfo)
admin_site.register(CompareCell)
admin_site.register(busyHourDaily)
