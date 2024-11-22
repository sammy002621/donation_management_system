from django.db import models

class Donor(models.Model):
    CONTACT_CHOICES = (
        ('email', 'Email'),
        ('phone', 'Phone'),
    )

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    preferred_contact_method = models.CharField(
        max_length=10,
        choices=CONTACT_CHOICES,
        default='email'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def total_donations(self):
        return self.donation_set.aggregate(total=models.Sum('amount'))['total'] or 0