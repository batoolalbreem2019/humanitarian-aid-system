from django.urls import path
from . import views
urlpatterns = [
    path('', views.DonationListCreateView.as_view()),
    path('<uuid:id>/', views.DonationDetailView.as_view()),
]
