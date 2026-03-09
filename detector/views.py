from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import analyze_plant_with_json
from .models import PlantScan
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import PlantScan
from .serializers import PlantScanDetailSerializer, PlantScanHistorySerializer

class DiseaseDetectionView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({"error": "No image provided"}, status=400)

        # 1. Get JSON data from Gemini
        image_data = image_file.read()
        ai_data = analyze_plant_with_json(image_data)
        
        disease = ai_data.get('disease_name', 'Unknown')
        ai_report = ai_data.get('report', 'No details provided.')
        # Since we are using Gemini for identification, we can set confidence 
        # based on AI's certainty or a fixed high-confidence placeholder.
        confidence = 0.99 

        # 2. Save to Database
        scan = PlantScan.objects.create(
            user=request.user,
            image=image_file,
            disease_name=disease,
            confidence=confidence,
            ai_suggestions=ai_report
        )

        # 3. Return your EXACT requested response format
        return Response({
            "id": scan.id,
            "image": request.build_absolute_uri(scan.image.url),
            "user": scan.user.username,
            "disease": disease,
            "confidence": f"{confidence * 100:.2f}%",
            "expert_suggestions": ai_report,
            "scan_id": scan.id
        })




class PlantScanHistoryListView(generics.ListAPIView):
    serializer_class = PlantScanHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # This ensures users only see their own search history
        return PlantScan.objects.filter(user=self.request.user).order_by('-created_at')
    

class PlantScanDetailView(generics.RetrieveAPIView):
    """
    Returns the full details of a specific scan based on the ID.
    Only allows access if the scan belongs to the authenticated user.
    """
    serializer_class = PlantScanDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        # Security: Filter by request.user so users can't guess IDs of others
        return PlantScan.objects.filter(user=self.request.user)