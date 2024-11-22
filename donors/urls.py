from django.urls import path
from . import views

urlpatterns = [
    path('', views.DonorListView.as_view(), name='donor-list'),
    path('<int:pk>/', views.DonorDetailView.as_view(), name='donor-detail'),
    path('create/', views.DonorCreateView.as_view(), name='donor-create'),
    path('<int:pk>/update/', views.DonorUpdateView.as_view(), name='donor-update'),
]