from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic
from .forms import OrderMessageForm
from .models import Vehicle, VehicleModel, Service, Order, OrderLine



# Create your views here.
from django.http import HttpResponse

def index(request):
    
    num_vehicles = Vehicle.objects.all().count()
   
    num_vehicle_model = VehicleModel.objects.all().count()

    num_service = Service.objects.all().count()

    num_order = Order.objects.all().count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_vehicles' :  num_vehicles,
        'num_vehicle_models' : num_vehicle_model,
        'num_service' : num_service,
        'num_order' : num_order,
        'num_visits' : num_visits,

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
    paginate_by = 6
    template_name = 'Petras_Garage/order_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            qs = qs.filter(
                Q(date__icontains=query) |
                Q(vehicle__customer__icontains=query) |
                Q(vehicle__license_plate__icontains=query) |
                Q(vehicle__vin_code__istartswith=query) |
                Q(vehicle__model__model__icontains=query)
            )
        return qs

class OrderDetailView(generic.DetailView, generic.edit.FormMixin):
    model = Order
    template_name = 'Petras_Garage/order_detail.html'
    # total_price = sum(entry.price for entry in order.order_entries.all())
    # context_object_name = 'order'
    form_class = OrderMessageForm
 
    # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
    #     context =  super().get_context_data(**kwargs)
    #     context['total_price'] = sum(entry.price for entry in self.get_object().order_entries.all())
    #     return context

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['order'] = self.get_object()
        initial['messenger'] = self.request.user
        return initial
    
    def post(self, request,  *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form:Any) -> HttpResponse:
        form.instance.order = self.get_object()
        form.instance.messenger = self.request.user
        form.save()

    def get_success_url(self) -> str:
        return reverse('order_detail', kwargs={'pk':self.get_object().pk})


class UserOrderInstanceListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'Petras_Garage/user_order_list.html'
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(vehicle__service_receiver= self.request.user)
        return qs    
    
    
    
    # def get_queryset(self) -> QuerySet[Any]:
    #     qs = super().get_queryset()
    #     qs = qs.filter(service_receiver=self.request.service_receiver)
    #     return qs
    
