from django.urls import path
from .views import *


urlpatterns = [
    path('clients/',ClientsList.as_view()),
    path('experts/',ExpertsList.as_view()),
    path('pending-experts/',PendingExperts.as_view()),
    path('single-pending-expert/<id>/',PendingSingleExpert.as_view()),
    path('domains/',Domains.as_view()),
    path('tutorials/',Tutorials.as_view()),
    path('sub-tutorials/',SubTutorials.as_view()),
    path('rating/',getRating.as_view()),
    path('domain-purchase/',Order_Domains.as_view()),
    path('subscriptions/',SubscriptionList.as_view()),
    path('dashboard/',Dashboard.as_view()),
    path('bargraph/',Bargraph.as_view()),
    path('roundedgraph/',Roundgraph.as_view()),

  
]