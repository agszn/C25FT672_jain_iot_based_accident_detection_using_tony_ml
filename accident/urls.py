from django.urls import path
from .views import accident_alert_view

urlpatterns = [
    path('accident-alert/', accident_alert_view, name='accident-alert'),
]
