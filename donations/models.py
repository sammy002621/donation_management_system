from django.db import models
import uuid

class Donation(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    donor = models.ForeignKey('donors.Donor', on_delete=models.CASCADE)
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    is_anonymous = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    donation_date = models.DateTimeField(auto_now_add=True)
    receipt_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-donation_date']

    def __str__(self):
        return f"{self.donor.name} - ${self.amount}"

    def generate_receipt_number(self):
        return f"RCP-{self.donation_date.strftime('%Y%m%d')}-{str(self.id)[:8]}"