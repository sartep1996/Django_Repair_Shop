from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from . forms import ProfileUpdateForm, UserUpdateForm, VehicleForm, ReservationForm
from Petras_Garage.models import Vehicle
from . models import Reservation



User = get_user_model()


@login_required
@csrf_protect
def profile_update(request):
     if request.method == "POST":
         user_form = UserUpdateForm(request.POST, instance=request.user)
         profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
         if user_form.is_valid() and profile_form.is_valid():
             user_form.save()
             profile_form.save()
             messages.success(request, "Profile updated.")
             return redirect('profile')
     else:
         user_form = UserUpdateForm(instance=request.user)
         profile_form = ProfileUpdateForm(instance=request.user.profile)
     return render(request, 'user_profile/profile_update.html', {'user_form': user_form, 'profile_form': profile_form})



@login_required
def profile(request, user_id=None):
    if user_id == None:
        user = request.user
    else:
        user = get_object_or_404(get_user_model(), id=user_id)
    return render(request, 'user_profile/profile.html', {'user_': user})

@csrf_protect
def signup(request):
    if request.user.is_authenticated:
        messages.info(request, 'In order to sign up, you need to log out first')
        return redirect ('index')
    if request.method == "POST":
        error = False
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if not username or len(username) < 3 or User.objects.filter(username = username).exists():
            error = True
            messages.error(request, 'Username is too short or already exists.')
        if not email or len(email) < 3 or User.objects.filter(email=email).exists():
            error = True
            messages.error(request, 'Email is invalid or user with this email already exists.')
        if not password or not password_confirm or password != password_confirm or len(password) < 8:
            error = True
            messages.error(request, "Password must be at least 8 characters long and match.")
        if not error:
            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )

            user.set_password(password)
            user.save
            messages.success(request, "User registration successful!")
            return redirect('login')
    return render(request, 'user_profile/signup.html')

@login_required
def create_vehicle(request):
    if request.method == 'GET':
        form = VehicleForm()
        return render(request, 'user_profile/create_vehicle.html', {'form': form})
    elif request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.service_receiver = request.user
            vehicle.save()
            return redirect('vehicle_detail', pk=vehicle.pk)
        
        return render(request, 'user_profile/create_vehicle.html', {'form': form})
    
@login_required
def my_vehicles(request):
    user_vehicles = Vehicle.objects.filter(service_receiver = request.user)
    return render(request, 'user_profile/my_vehicles.html', {'user_vehicles': user_vehicles})

@login_required
def create_reservation(request):
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.service_receiver = request.user
            reservation.save()
            messages.success(request, "Reservation is created successfully!")
            return redirect ('my_reservations')
    else:
        form = ReservationForm()
        form.fields["vehicle"].queryset = Vehicle.objects.filter(service_receiver=request.user)

    return render(request, 'user_profile/create_reservation.html', {'form':form})

@login_required
def my_reservations(request):
    service_receiver_reservations = Reservation.objects.filter(service_receiver=request.user)
    return render(request, 'user_profile/my_reservations.html', {'service_receiver_reservations': service_receiver_reservations} )



            
        