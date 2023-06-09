from django.urls import path
from . import views
from ususer_profile.views import create_vehicle, my_vehicles, create_reservation, my_reservations


urlpatterns = [
     path('signup/', views.signup, name='signup'),
     path('profile/', views.profile, name='profile'),
     path('profile/<int:user_id>/', views.profile, name='profile'),
     path('profile/update/', views.profile_update, name='profile_update'),
     path('create-vehicle/', create_vehicle, name='create_vehicle'),
     path('my-cars/', my_vehicles, name='my_vehicles'),
     path('create-reservation/', create_reservation, name='create_reservation'),
     path('my-reservations/', my_reservations, name='my_reservations')
 ]
