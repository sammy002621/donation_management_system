from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .models import Donation
from .forms import DonationForm
from donors.models import Donor
from events.models import Event

class DonationListView(LoginRequiredMixin, ListView):
    model = Donation
    template_name = 'donations/donation_list.html'
    context_object_name = 'donations'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        donor_id = self.request.GET.get('donor')
        event_id = self.request.GET.get('event')
        
        if donor_id:
            queryset = queryset.filter(donor_id=donor_id)
        if event_id:
            queryset = queryset.filter(event_id=event_id)
            
        return queryset

class DonationCreateView(LoginRequiredMixin, CreateView):
    model = Donation
    form_class = DonationForm
    template_name = 'donations/donation_form.html'
    success_url = reverse_lazy('donation-list')

    def get_initial(self):
        initial = super().get_initial()
        donor_id = self.request.GET.get('donor')
        event_id = self.request.GET.get('event')
        
        if donor_id:
            initial['donor'] = get_object_or_404(Donor, pk=donor_id)
        if event_id:
            initial['event'] = get_object_or_404(Event, pk=event_id)
            
        return initial

def generate_receipt_pdf(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    
    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="donation_receipt_{donation.id}.pdf"'
    
    # Create the PDF object using ReportLab
    p = canvas.Canvas(response, pagesize=letter)
    
    # Add content to the PDF
    p.drawString(100, 750, "Donation Receipt")
    p.drawString(100, 700, f"Receipt Number: {donation.generate_receipt_number()}")
    p.drawString(100, 675, f"Date: {donation.donation_date.strftime('%B %d, %Y')}")
    p.drawString(100, 650, f"Donor: {donation.donor.name}")
    p.drawString(100, 625, f"Amount: ${donation.amount}")
    p.drawString(100, 600, f"Payment Method: {donation.get_payment_method_display()}")
    
    if donation.event:
        p.drawString(100, 575, f"Event: {donation.event.name}")
    
    # Add footer
    p.drawString(100, 100, "Thank you for your generous donation!")
    
    # Close the PDF object
    p.showPage()
    p.save()
    
    # Mark receipt as sent
    donation.receipt_sent = True
    donation.save()
    
    return response