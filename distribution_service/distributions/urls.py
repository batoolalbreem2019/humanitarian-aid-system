from django.urls import path
from . import views
urlpatterns = [
    path('', views.DistributionListCreateView.as_view()),
    path('<uuid:id>/', views.DistributionDetailView.as_view()),
    path('<uuid:id>/status/', views.DistributionStatusView.as_view()),
]
