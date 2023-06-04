from django.shortcuts import render, get_object_or_404
from .models import Vehicle, VehicleModel, Service, Order, OrderLine
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q





# Create your views here.
from django.http import HttpResponse

def index(request):
    
    num_vehicles = Vehicle.objects.all().count()
   
    num_vehicle_model = VehicleModel.objects.all().count()

    num_service = Service.objects.all().count()

    num_order = Order.objects.all().count()

    context = {
        'num_vehicles' :  num_vehicles,
        'num_vehicle_models' : num_vehicle_model,
        'num_service' : num_service,
        'num_order' : num_order

    }

    return render(request, 'Petras_Garage/index.html', context=context)


def vehicle_list(request):
    qs = Vehicle.objects.all()
    query = request.GET.get('query')
    if query:
        qs = qs.filter(
            Q(vehicle_model__maker__icontains=query)|
            Q(vehicle_model__maker__icontains=query)|
            Q(license_plate__icontains=query)|
            Q(vim_code__icontains=query)|
            Q(client__icontains=query)
        )
    paginator = Paginator(qs, 5)
    page_number = request.GET.get('page', 1)  # Default to the first page if no page number is provided
    vehicle_list = paginator.get_page(page_number)
    return render(request, 'Petras_Garage/vehicles.html', {
        'vehicle_list': vehicle_list,
    })


# def vehicle_list(request):
#     return render(request, 'Petras_Garage/vehicles.html',{
#         'vehicles': Vehicle.objects.all()
       
#     })
    

def vehicle_detail(request, pk:int):
    return render(request, 'Petras_Garage/vehicle_detail.html', {
        'vehicle': get_object_or_404(Vehicle, pk=pk)
    })

class OrderView(generic.ListView):
    model = Order
    template_name = 'Petras_Garage/order_list.html'

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'Petras_Garage/order_detail.html'
