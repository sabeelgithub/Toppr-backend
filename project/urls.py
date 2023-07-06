from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('adminpanel/', include('adminpanel.urls')),
    path('commen/', include('commen.urls')),
    path('client/', include('client.urls')),
    path('expert/', include('expert.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
