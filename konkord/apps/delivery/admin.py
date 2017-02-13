from django.contrib import admin
from .models import DeliveryService, DeliveryServiceRelation, DeliveryOffice, City


class DeliveryOfficeInline(admin.TabularInline):
    model = DeliveryOffice
    extra = 0


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'identificator', 'delivery_service', 'active']
    inlines = [DeliveryOfficeInline]

admin.site.register(DeliveryService)
admin.site.register(DeliveryServiceRelation)
admin.site.register(DeliveryOffice)
