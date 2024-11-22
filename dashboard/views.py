from django.views.generic import TemplateView # type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin # type: ignore
from django.db.models import Sum, Count, Avg, Q # type: ignore
from django.db.models.functions import TruncMonth, TruncWeek # type: ignore
from django.utils import timezone # type: ignore
from django.core.cache import cache # type: ignore
from donations.models import Donation
from events.models import Event
from donors.models import Donor
from datetime import datetime, timedelta
import json

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Basic statistics
        context['total_donations'] = self.get_cached_total_donations()
        context['top_donors'] = self.get_cached_top_donors()
        context['monthly_trends'] = self.get_cached_monthly_trends()
        context['recent_events'] = self.get_cached_recent_events()
        context['donation_statistics'] = self.get_donation_statistics()

        # Donation Distribution
        donation_ranges = [
            ('$0-$100', 0, 100),
            ('$101-$500', 101, 500),
            ('$501-$1000', 501, 1000),
            ('$1000+', 1001, None)
        ]
        
        distribution_data = []
        for label, min_amount, max_amount in donation_ranges:
            if max_amount is None:
                count = Donation.objects.filter(amount__gte=min_amount).count()
            else:
                count = Donation.objects.filter(
                    amount__gte=min_amount,
                    amount__lt=max_amount
                ).count()
            distribution_data.append(count)
        
        context['donation_categories'] = json.dumps([range[0] for range in donation_ranges])
        context['donation_amounts'] = json.dumps(distribution_data)

        # Payment Methods
        payment_data = Donation.objects.values('payment_method').annotate(
            count=Count('id')
        ).filter(payment_method__isnull=False).order_by('-count')
        
        context['payment_methods'] = json.dumps([pd['payment_method'] for pd in payment_data])
        context['payment_counts'] = json.dumps([pd['count'] for pd in payment_data])

        # Weekly Trends
        end_date = timezone.now()
        start_date = end_date - timedelta(weeks=12)
        weekly_data = Donation.objects.filter(
            donation_date__gte=start_date
        ).annotate(
            week=TruncWeek('donation_date')
        ).values('week').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('week')

        weekly_data = list(weekly_data)
        context['weekly_labels'] = json.dumps([data['week'].strftime('%b %d') for data in weekly_data])
        context['weekly_amounts'] = json.dumps([float(data['total']) if data['total'] else 0 for data in weekly_data])
        context['weekly_counts'] = json.dumps([data['count'] for data in weekly_data])
        
        return context

    def get_cached_total_donations(self):
        cache_key = 'total_donations'
        total = cache.get(cache_key)
        if total is None:
            total = Donation.objects.aggregate(
                total=Sum('amount'))['total'] or 0
            cache.set(cache_key, total, 3600)  # Cache for 1 hour
        return total

    def get_cached_top_donors(self):
        cache_key = 'top_donors'
        top_donors = cache.get(cache_key)
        if top_donors is None:
            top_donors = list(Donor.objects.annotate(
                total_donated=Sum('donation__amount')
            ).filter(
                total_donated__isnull=False
            ).order_by('-total_donated')[:5].values('name', 'total_donated'))
            cache.set(cache_key, top_donors, 3600)
        return top_donors

    def get_cached_monthly_trends(self):
        cache_key = 'monthly_trends'
        trends = cache.get(cache_key)
        if trends is None:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=365)
            trends = list(Donation.objects.filter(
                donation_date__gte=start_date
            ).annotate(
                month=TruncMonth('donation_date')
            ).values('month').annotate(
                total=Sum('amount')
            ).order_by('month'))
            cache.set(cache_key, trends, 3600)
        return json.dumps(trends, default=str)

    def get_cached_recent_events(self):
        cache_key = 'recent_events'
        events = cache.get(cache_key)
        if events is None:
            events = list(Event.objects.annotate(
                total_raised=Sum('donation__amount'),
                donor_count=Count('donation__donor', distinct=True)
            ).order_by('-date')[:5])
            cache.set(cache_key, events, 3600)
        return events

    def get_donation_statistics(self):
        stats = {
            'total_donors': Donor.objects.count(),
            'total_events': Event.objects.count(),
            'avg_donation': Donation.objects.aggregate(
                avg=Avg('amount'))['avg'] or 0,
            'this_month': Donation.objects.filter(
                donation_date__month=timezone.now().month,
                donation_date__year=timezone.now().year
            ).aggregate(total=Sum('amount'))['total'] or 0
        }
        return stats