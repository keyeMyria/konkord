from django.contrib import admin
from .models import DeliveryService, DeliveryServiceRelation, DeliveryOffice, City
from django.conf import settings
from .jobs import update_cities
from django.utils.translation import ugettext_lazy as _


class DeliveryOfficeInline(admin.TabularInline):
    model = DeliveryOffice
    extra = 0


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'identificator', 'delivery_service', 'active']
    inlines = [DeliveryOfficeInline]


@admin.register(DeliveryService)
class DeliveryServiceAdmin(admin.ModelAdmin):

    def schedule_update_cities_job(self):
        task_manager = settings.ACTIVE_TASK_QUEUE
        task_manager.schedule(update_cities, repeat=24 * 60)

    schedule_update_cities_job.short_description = _(
        'Schedule update cities job')

admin.site.register(DeliveryServiceRelation)
admin.site.register(DeliveryOffice)
