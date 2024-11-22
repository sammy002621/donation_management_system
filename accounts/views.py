from django.contrib.auth.views import LoginView # type: ignore
from django.contrib.auth.views import LogoutView # type: ignore
from django.urls import reverse_lazy # type: ignore
from django.views.generic import CreateView, UpdateView # type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin # type: ignore
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import User

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('dashboard')

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'phone', 'address']
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        return self.request.user

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)