from django.urls import path, include

urlpatterns = [
    path('api/distributions/', include('distributions.urls')),
]
