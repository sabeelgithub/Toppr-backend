from django.urls import path
from .views import *


urlpatterns = [
 
    path('tutorials/',Tutorials.as_view()),
    path('sub-tutorials/',SubTutorials.as_view()),
    path('domain-purchase/',Domain_Purchasing.as_view()),
    path('single-domain/',Single_Domain.as_view()),
    path('domain-experts/',getExpertsToPerticularDomain.as_view()),
    path('single-experts/',getSingleExpertDetails.as_view()),
    path('subscribe/',Subscribe.as_view()),
    path('profile/',ClientProfile.as_view()),
    path('slot-booking/',SlotBooking.as_view()),
    path('submit-rating/',SubmitRating.as_view()),
   
  
]