from django.contrib import admin
from . import models

# Register your models here.

from .models import VehicleModel, Vehicle, Order, Service, OrderLine

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'vehicle_model', 'vin_code', 'service_receiver')
    list_filter = ('vehicle_model',)
    search_fields = ('license_plate', 'vin_code')

class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ('maker', 'model')

class OrderLineInLine(admin.TabularInline):
    model = models.OrderLine
    extra = 0


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('service', 'order', 'quantity', 'price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('date', 'vehicle', 'sum', 'service_receiver', 'due_to_finish_repair')
    inlines = [OrderLineInLine]
 

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

class OrderMessageAdmin(admin.ModelAdmin):
    list_display = ('sent_at', 'order', 'messenger', 'content')




admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(VehicleModel, VehicleModelAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)