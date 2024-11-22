from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore
from django.views.generic import RedirectView # type: ignore

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='dashboard/'), name='home'),  # Redirect root to dashboard
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('events/', include('events.urls')),
    path('donors/', include('donors.urls')),
    path('donations/', include('donations.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)