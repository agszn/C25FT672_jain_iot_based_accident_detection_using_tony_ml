from django.conf import settings
from django.core.mail import send_mail

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import AccidentEvent
from .serializers import AccidentEventSerializer


@api_view(['GET', 'POST'])
def accident_alert_view(request):
    """
    GET  -> Return accident history (latest events).
    POST -> Receives accident alert JSON from NodeMCU, saves it, and sends email.
    """

    # 1️⃣ GET = history / safety check
    if request.method == 'GET':
        # You can limit results; e.g. last 50 events
        events = AccidentEvent.objects.order_by('-created_at')[:50]
        serializer = AccidentEventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2️⃣ POST = save + email
    data = request.data.copy()

    # Map NodeMCU JSON keys to our model fields (if names differ)
    payload = {
        "impact": data.get("impact"),
        "distance": data.get("distance"),
        "vibration": data.get("vibration"),
        "device_id": data.get("device_id", None),
        "raw_message": data.get("message", None),
    }

    serializer = AccidentEventSerializer(data=payload)
    if not serializer.is_valid():
        return Response(
            {"error": "Invalid data", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    event = serializer.save()

    # Build email content
    subject = "🚨 Accident Detected!"
    lines = [
        f"An accident was detected in Belgaum by device: {event.device_id or '8456'}",
        "",
        f"Impact: {event.impact}",
        f"Distance: {event.distance} cm" if event.distance is not None else "Distance: N/A",
        f"Vibration: {event.vibration}",
        "",
        f"Raw message: {event.raw_message or 'N/A'}",
        "",
        f"Time: {event.created_at}",
    ]
    message = "\n".join(lines)

    recipients = getattr(settings, 'ACCIDENT_ALERT_RECIPIENTS', [])
    # Fallback: if no list provided, try sending to DEFAULT_FROM_EMAIL
    if not recipients and getattr(settings, 'DEFAULT_FROM_EMAIL', None):
        recipients = [settings.DEFAULT_FROM_EMAIL]

    if recipients:
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                fail_silently=False,
            )
        except Exception as e:
            # Email failed, but we still keep the event
            return Response(
                {
                    "status": "saved_but_email_failed",
                    "error": str(e),
                    "event_id": event.id,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return Response(
        {
            "status": "ok",
            "event_id": event.id,
        },
        status=status.HTTP_201_CREATED,
    )
