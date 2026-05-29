from rest_framework import generics
from .models import Donation
from .serializers import DonationSerializer

class DonationListCreateView(generics.ListCreateAPIView):
    queryset = Donation.objects.all().order_by('-donated_at')
    serializer_class = DonationSerializer

class DonationDetailView(generics.RetrieveAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    lookup_field = 'id'
