from django.db import models

class AccidentEvent(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    device_id = models.CharField(max_length=100, blank=True, null=True)

    impact = models.FloatField()
    distance = models.FloatField(blank=True, null=True)
    vibration = models.IntegerField(blank=True, null=True)

    raw_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Accident from {self.device_id or 'unknown'} @ {self.created_at}"
