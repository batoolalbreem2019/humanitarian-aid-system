from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer, UserRegisterSerializer

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

class UserStatusView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        new_status = request.data.get('status')
        if new_status not in ['ACTIVE','SUSPENDED','PENDING']:
            return Response({'error':'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        user.status = new_status
        user.save()
        return Response(UserSerializer(user).data)
