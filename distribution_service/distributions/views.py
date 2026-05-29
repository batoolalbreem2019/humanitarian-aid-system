from rest_framework import generics, status
from rest_framework.response import Response
from .models import Distribution
from .serializers import DistributionSerializer

class DistributionListCreateView(generics.ListCreateAPIView):
    queryset = Distribution.objects.all().order_by('-created_at')
    serializer_class = DistributionSerializer

class DistributionDetailView(generics.RetrieveAPIView):
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer
    lookup_field = 'id'

class DistributionStatusView(generics.UpdateAPIView):
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer
    lookup_field = 'id'
    def patch(self, request, *args, **kwargs):
        dist = self.get_object()
        dist.status = request.data.get('status', dist.status)
        dist.save()
        return Response(DistributionSerializer(dist).data)
