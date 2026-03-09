from django.urls import path
from .views import DiseaseDetectionView, PlantScanDetailView, PlantScanHistoryListView

urlpatterns = [
    path('detect/', DiseaseDetectionView.as_view(), name='disease_detect'),
    path('history/', PlantScanHistoryListView.as_view(), name='scan_history'),
    path('history/<int:id>/', PlantScanDetailView.as_view(), name='scan_detail'),
]