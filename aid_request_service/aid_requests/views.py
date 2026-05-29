from rest_framework import generics, status
from rest_framework.response import Response
from .models import AidRequest
from .serializers import AidRequestSerializer
from .events import publish_event

class AidRequestListCreateView(generics.ListCreateAPIView):
    queryset = AidRequest.objects.all().order_by('-created_at')
    serializer_class = AidRequestSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        publish_event('AidRequestApproved', {
            'request_id':  str(instance.id),
            'user_id':     str(instance.user_id),
            'type':        instance.request_type,
            'description': instance.description,
        })

class AidRequestDetailView(generics.RetrieveUpdateAPIView):
    queryset = AidRequest.objects.all()
    serializer_class = AidRequestSerializer
    lookup_field = 'id'

class AidRequestStatusView(generics.UpdateAPIView):
    queryset = AidRequest.objects.all()
    serializer_class = AidRequestSerializer
    lookup_field = 'id'
    def patch(self, request, *args, **kwargs):
        req = self.get_object()
        new_status = request.data.get('status')
        req.status = new_status
        req.save()
        publish_event('AidRequestStatusChanged', {
            'request_id': str(req.id),
            'user_id':    str(req.user_id),
            'new_status': new_status,
        })
        return Response(AidRequestSerializer(req).data)
