from django.db import models

class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    impact = models.FloatField()
    vibration = models.BooleanField()
    distance = models.FloatField()
    prediction = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.timestamp} | {self.prediction}"
