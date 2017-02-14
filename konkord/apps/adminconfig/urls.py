from django.conf.urls import url
import adminconfig.views

# These url patterns use for admin interface
urlpatterns = [
    url(r'^admin/config/$', adminconfig.views.config_index, name="admin_config_index"),
    url(r'^admin/config/(\w+)/$', adminconfig.views.config_form, name="admin_config_form"),
]
