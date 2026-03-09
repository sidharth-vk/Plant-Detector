from django.db import models
from django.conf import settings

class PlantScan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='plant_scans/%Y/%m/%d/')
    disease_name = models.CharField(max_length=255)
    confidence = models.FloatField()
    ai_suggestions = models.TextField() # Stores Gemini's response
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.disease_name}"