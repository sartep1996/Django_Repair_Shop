from django.urls import path
from . import views




urlpatterns = [
    path('', views.index, name='index'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('order/', views.OrderView.as_view(), name='order_list' ),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name= 'order_detail' ),
    path('my-orders/', views.UserOrderInstanceListView.as_view(), name='my_orders'),
]