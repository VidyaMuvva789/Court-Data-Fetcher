from django.urls import path
from . import views

urlpatterns=[
    path('',views.search_case,name='search_case'),
    path('order-details/', views.order_details, name='order_details'),
]
