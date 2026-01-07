from django.urls import path
from .views import *

urlpatterns = [
    path('sensor-data/', sensor_data, name='sensor_data'),
    path('sensor_dashboard/', sensor_dashboard, name='sensor_dashboard'),
    path('analytics/', data_analytics, name='data_analytics'),
]

