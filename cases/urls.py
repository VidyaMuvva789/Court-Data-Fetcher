from django.urls import path
from . import views

urlpatterns=[
    path('',views.search_case,name='search_case'),
]