from django.urls import path
from . import views
urlpatterns = [
    path('', views.AidRequestListCreateView.as_view()),
    path('<uuid:id>/', views.AidRequestDetailView.as_view()),
    path('<uuid:id>/status/', views.AidRequestStatusView.as_view()),
]
