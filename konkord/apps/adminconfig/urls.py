from django.conf.urls import url
import adminconfig.views

urlpatterns = [
    url(
        r'^restart-engine/(\w+)/$',
        adminconfig.views.restart_engine, name="admin_config_restart_engine"),
    url(
        r'^admin/config/$',
        adminconfig.views.config_index, name="admin_config_index"),
    url(
        r'^admin/config/(\w+)/$',
        adminconfig.views.config_form, name="admin_config_form"),
]
