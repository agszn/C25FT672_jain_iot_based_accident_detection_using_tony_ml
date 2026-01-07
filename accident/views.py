import json
import joblib
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os

from .models import SensorData

# Load TinyML model
MODEL_PATH = os.path.join(settings.BASE_DIR, 'accident', 'accident_model.pkl')
model = joblib.load(MODEL_PATH)

@csrf_exempt
def sensor_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            impact = float(data.get("impact", 0))
            vibration = int(data.get("vibration", 0))
            distance = int(data.get("distance", 100))

            # TinyML prediction
            prediction = model.predict([[impact, vibration, distance]])[0]
            status = "ACCIDENT" if prediction == 1 else "NORMAL"

            # Save to database
            SensorData.objects.create(
                impact=impact,
                vibration=bool(vibration),
                distance=distance,
                prediction=status
            )

            # Send email if accident
            if prediction == 1:
                send_mail(
                    'Accident Alert!',
                    f'Accident detected!\nImpact: {impact}\nVibration: {vibration}\nDistance: {distance}',
                    settings.EMAIL_HOST_USER,
                    settings.ACCIDENT_ALERT_RECIPIENTS,
                    fail_silently=True,
                )

            return JsonResponse({
                "impact": impact,
                "vibration": vibration,
                "distance": distance,
                "prediction": status
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)

from django.shortcuts import render

def sensor_dashboard(request):
    """
    Render all sensor readings in a template.
    """
    readings = SensorData.objects.all().order_by('-timestamp')  # latest first
    context = {
        "sensor_data": readings
    }
    return render(request, "accident/sensor_data.html", context)

from django.shortcuts import render
from .models import SensorData
from django.db.models import Avg, Max, Min, Count

def data_analytics(request):
    """
    Compute analytics from SensorData and display charts/statistics.
    """
    # Fetch all sensor data
    sensor_data = SensorData.objects.all().order_by('-timestamp')  # latest first

    # Basic statistics
    total_readings = sensor_data.count()
    avg_impact = sensor_data.aggregate(Avg('impact'))['impact__avg'] or 0
    max_impact = sensor_data.aggregate(Max('impact'))['impact__max'] or 0
    min_impact = sensor_data.aggregate(Min('impact'))['impact__min'] or 0

    avg_distance = sensor_data.aggregate(Avg('distance'))['distance__avg'] or 0
    max_distance = sensor_data.aggregate(Max('distance'))['distance__max'] or 0
    min_distance = sensor_data.aggregate(Min('distance'))['distance__min'] or 0

    accident_count = sensor_data.filter(prediction="ACCIDENT").count()
    normal_count = sensor_data.filter(prediction="NORMAL").count()

    # Prepare data for chart (last 20 readings)
    chart_data = sensor_data.order_by('-timestamp')[:20][::-1]  # reverse for chronological order
    timestamps = [reading.timestamp.strftime("%H:%M:%S") for reading in chart_data]
    impact_values = [reading.impact for reading in chart_data]
    distance_values = [reading.distance for reading in chart_data]
    vibration_values = [1 if reading.vibration else 0 for reading in chart_data]  # 1=Yes, 0=No

    context = {
        "total_readings": total_readings,
        "avg_impact": avg_impact,
        "max_impact": max_impact,
        "min_impact": min_impact,
        "avg_distance": avg_distance,
        "max_distance": max_distance,
        "min_distance": min_distance,
        "accident_count": accident_count,
        "normal_count": normal_count,
        "timestamps": timestamps,
        "impact_values": impact_values,
        "distance_values": distance_values,
        "vibration_values": vibration_values,
    }

    return render(request, "dashboard/dashboard.html", context)

