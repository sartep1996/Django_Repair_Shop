from django.contrib.auth import get_user_model
from django import forms
from . import models
from Petras_Garage.models import Vehicle
from .models import Reservation


User = get_user_model()

class DateInput(forms.DateInput):
     input_type = 'date'


class UserUpdateForm(forms.ModelForm):
     email = forms.EmailField()

     class Meta:
         model = User
         fields = ("first_name", "last_name", "username", "email")


class ProfileUpdateForm(forms.ModelForm):
     class Meta:
         model = models.Profile
         fields = ("picture",)



# class OrderInstanceForm(forms.ModelForm):
#      class Meta:
#           model = model.Order

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['license_plate', 'vin_code', 'note', 'condition', 'vehicle_model', 'photo', 'service_receiver']


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['vehicle', 'reservation_date']
        widgets = {
            'reservation_date': DateInput(attrs={'type': 'date'})
        }

