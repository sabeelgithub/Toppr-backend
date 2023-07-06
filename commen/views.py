from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import APIView
from accounts.models import Expert
from domains.models import Domain,Tutorial,Sub_tutorial
from adminpanel.serializers import ExpertsListSerializer
from domains.serializers import DomainSerializer,TutorialSerializer,Sub_TutorialSerializer

# Create your views here.

class ExpertsList(APIView):
    # get experts list
    def get(self,request):
        try:
            experts = Expert.objects.filter(user__is_expert=True,user__is_block=False,user__is_verified='true').order_by('-id')
            serializer = ExpertsListSerializer(experts,many=True)
            return Response({'payload':serializer.data,'message':'success'})
        except Exception as e:
            return Response({'error':e})
        
class Domains(APIView):
    #listing domains
    def get(self,request):
        try:
            domain = Domain.objects.filter(blocked=False).order_by('-id')
            serializer = DomainSerializer(domain,many=True)
            return Response({'payload':serializer.data})
        except Exception as e:
            return Response({'error':e})
        


        

    