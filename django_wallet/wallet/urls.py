from django.urls import path
from .views import *
from django.contrib.auth import login, logout
from django.conf import settings
from django.conf.urls.static import static

app_name = 'wallet'


urlpatterns = [
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('notifications/', notifications, name='notifications'),
    path('wallet', wallet, name='wallet'),
    path('deposit/', deposit, name='deposit'),
    path('apply/<str:code>/', apply_offer, name='apply_offer'),
    path('withdraw/', withdraw, name='withdraw'),
    path('kyc/', kyc_view, name='kyc'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)