from django.db import models
from django.utils import timezone

class Event(models.Model):
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    )

    name = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    donation_goal = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name

    def total_donations(self):
        return self.donation_set.aggregate(total=models.Sum('amount'))['total'] or 0

    def progress_percentage(self):
        total = self.total_donations()
        return min(round((total / self.donation_goal) * 100, 2), 100) if self.donation_goal > 0 else 0

    def update_status(self):
        today = timezone.now().date()
        if self.date > today:
            self.status = 'upcoming'
        elif self.date == today:
            self.status = 'ongoing'
        else:
            self.status = 'completed'
        self.save()