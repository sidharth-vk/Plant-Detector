from rest_framework import serializers
from .models import PlantScan

class PlantScanHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantScan
        fields = ['id', 'image', 'disease_name', 'confidence', 'created_at']

class PlantScanDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantScan
        fields = ['id', 'image', 'disease_name', 'confidence', 'ai_suggestions', 'created_at']