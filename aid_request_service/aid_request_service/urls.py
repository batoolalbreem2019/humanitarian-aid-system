from django.urls import path, include

urlpatterns = [
    path('api/aid-requests/', include('aid_requests.urls')),
]
