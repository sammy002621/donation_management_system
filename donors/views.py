from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Donor
from .forms import DonorForm
from .filters import DonorFilter

class DonorListView(LoginRequiredMixin, ListView):
    model = Donor
    template_name = 'donors/donor_list.html'
    context_object_name = 'donors'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = DonorFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return DonorFilter(self.request.GET, queryset=queryset).qs

class DonorDetailView(LoginRequiredMixin, DetailView):
    model = Donor
    template_name = 'donors/donor_detail.html'
    context_object_name = 'donor'

class DonorCreateView(LoginRequiredMixin, CreateView):
    model = Donor
    form_class = DonorForm
    template_name = 'donors/donor_form.html'
    success_url = reverse_lazy('donor-list')

class DonorUpdateView(LoginRequiredMixin, UpdateView):
    model = Donor
    form_class = DonorForm
    template_name = 'donors/donor_form.html'
    success_url = reverse_lazy('donor-list')