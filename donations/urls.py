from django.urls import path
from . import views

urlpatterns = [
    path('', views.DonationListView.as_view(), name='donation-list'),
    path('create/', views.DonationCreateView.as_view(), name='donation-create'),
    path('receipt/<uuid:donation_id>/', views.generate_receipt_pdf, name='generate-receipt'),
]