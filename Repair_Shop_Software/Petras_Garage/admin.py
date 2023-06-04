from django.contrib import admin
from . import models

# Register your models here.

from .models import VehicleModel, Vehicle, Order, Service, OrderLine

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'vehicle_model', 'vin_code', 'client')
    list_filter = ('vehicle_model', )
    search_fields = ('license_plate', 'vin_code')

class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ('maker', 'model')

class OrderLineInLine(admin.TabularInline):
    model = models.OrderLine
    extra = 0


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('service', 'order', 'quantity', 'price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('date', 'vehicle', 'sum')
    inlines = [OrderLineInLine]
 

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(VehicleModel, VehicleModelAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)