from django.urls import path
from .views import *


urlpatterns = [
 
    path('experts/',ExpertsList.as_view()),
    path('domains/',Domains.as_view()),
    
]