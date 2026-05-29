from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),
    path('<uuid:id>/', views.UserDetailView.as_view()),
    path('<uuid:id>/status/', views.UserStatusView.as_view()),
]
