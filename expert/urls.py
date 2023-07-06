from django.urls import path
from .views import *


urlpatterns = [
 
    path('profile/',ExpertProfile.as_view()),
    path('slots/',SlotsManage.as_view()),
  


    
]