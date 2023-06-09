from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image
# from . import models
from django import forms
# from Petras_Garage.models import Vehicle
from django.contrib.auth.models import User




class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(), 
        verbose_name=_("user_"), 
        on_delete=models.CASCADE,
        related_name='profile',
        null=True, blank=True,
    )
    picture = models.ImageField(_("picture"), upload_to='ususer_profile/pictures')

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"pk": self.pk})


    def save(self, *args, **kwargs) -> None:
         super().save(*args, **kwargs)
         if self.picture:
            pic = Image.open(self.picture.path)
            if pic.width > 300 or pic.height > 300:
                new_size = (300, 300)
                pic.thumbnail(new_size)
                pic.save(self.picture.path)


class DateInput(forms.DateInput):
    input_type = 'date'


class Reservation(models.Model):
    
    service_receiver = models.ForeignKey(
        User, 
        verbose_name=_('customer'),
        on_delete=models.CASCADE,
        related_name='my_orders',
        null=True,
        blank=True
    )

    vehicle = models.ForeignKey(
        'Petras_Garage.Vehicle',
        verbose_name=_("vehicle"), 
        on_delete=models.CASCADE,
        related_name = 'my_vehicles',
        null=True,
        blank=True
    )

    
    reservation_date = models.DateField(verbose_name=_('date'))

    
    
    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")

    def __str__(self):
        return f'{self.service_receiver} {self.vehicle} {self.reservation_date}'

    def get_absolute_url(self):
        return reverse("Reservation_detail", kwargs={"pk": self.pk})
