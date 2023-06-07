from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from tinymce.models import HTMLField



# Create your models here.
class VehicleModel(models.Model):
    maker = models.CharField(_("Maker"), max_length=100, help_text='Enter the maker of your vehicle (ex. ford)' )
    model_ve = models.CharField(_("Vehicle_Model"), max_length=100)

    class Meta:
        verbose_name = _("Vehicle model")
        verbose_name_plural = _("Vehicle models")

    def __str__(self):
        return f"{self.maker} {self.model_ve} "

    def get_absolute_url(self):
        return reverse("vehicle_model_detail", kwargs={"pk": self.pk})


class Vehicle(models.Model):
    license_plate = models.CharField(_("license plate number"), max_length=100)
    vin_code = models.CharField(_("VIN code"), max_length=100)
    note = models.CharField(_("note"), max_length=100)
    condition = HTMLField()
    vehicle_model = models.ForeignKey(
        VehicleModel,
        verbose_name=_("Vehicle model"),
        on_delete=models.CASCADE,
        related_name='Vehicles')

    
    photo = models.ImageField(
    _("photo"), 
    upload_to='Petras_Garage/vehicle_photos', 
    null=True, 
    blank=True,
    )
    service_receiver = models.ForeignKey(
        User, 
        verbose_name=('customer'),
        on_delete = models.CASCADE,
        related_name='orders',
        null=True,
        blank=True

    )

    # models.CharField(_("automobilio modelis"), max_length=100)

    class Meta:
        verbose_name = _("vehicle")
        verbose_name_plural = _("vehicles")

    def __str__(self):
        return f"{self.license_plate}  {self.vin_code} {self.note}  {self.service_receiver}"

    def get_absolute_url(self):
        return reverse("vehicle_detail", kwargs={"pk": self.pk})
    
    def display_modelis(self):
        return  ','.join(vehicle_model.maker for vehicle_model in self.vehicle_model.all()[:3])
    
    


    
class Order(models.Model):
    date = models.DateField(_('Date'))
    vehicle = models.ForeignKey(
        Vehicle,
        verbose_name=_("Order"),
        on_delete=models.CASCADE,
        related_name='orders'
    )
    sum = models.IntegerField(_('Sum'))

    due_to_finish_repair = models.DateField(_("Due to finish repair"), null=True, blank=True, db_index=True)

    STATUS_CHOICES = [
        ("new", "New"),
        ("processing", "Processing"),
        ("complete", "Complete"),
        ("cancelled", "Cancelled"),
    ]
    status = models.CharField(
        _("Status"),
        max_length=20, 
        choices=STATUS_CHOICES, 
        default=0, 
        db_index=True)


    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"{self.date} {self.vehicle}"

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})
    
    def display_automobilis(self):
        return ','.join(vehicle.license_plate for vehicle in self.vehicle.all()[:3])

    @property
    def service_receiver(self):
        return self.vehicle.service_receiver
    
    @property
    def is_due_repair_passed(self):
        return timezone.now() > self.due_to_finish_repair


class Service (models.Model):
    name = models.CharField(_("Name"), max_length=100)
    price = models.IntegerField(_('Price'))

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self):
        return f"{self.name} {self.price}"

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
    
    def display_paslauga(self):
        return ','.join(service.name for service in self.service.all()[:3])
    



class OrderLine(models.Model):
    service = models.ForeignKey(
        Service,
        verbose_name=_('order line'),
        on_delete=models.CASCADE,
        related_name='order_lines'
    )
    order = models.ForeignKey(
        Order,
        verbose_name=_('order line'),
        on_delete=models.CASCADE,
        related_name='order_lines'
    )
    
    quantity = models.IntegerField(_('Quantity'))
    price = models.IntegerField(_('Price'))

    class Meta:
        verbose_name = _("Order line")
        verbose_name_plural = _("Order lines")

    def __str__(self):
        return f"{self.service} {self.order} {self.quantity} {self.price}"

    def get_absolute_url(self):
        return reverse("order_line_detail", kwargs={"pk": self.pk})
    
    def display_service(self):
        return ','.join(service.name for service in self.service.all()[:3])
    
    
