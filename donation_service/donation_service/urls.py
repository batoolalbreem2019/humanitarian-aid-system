from django.urls import path, include

urlpatterns = [
    path('api/donations/', include('donations.urls')),
]
