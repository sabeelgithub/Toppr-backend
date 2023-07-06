from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import APIView
from  rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.models import Expert,CustomUser
from accounts.serializers import EditProfileSerializer,ExpertEditSerializer,ExpertEditSerializer01
from adminpanel.serializers import ExpertsListSerializer
from order.models import Domain_purchase,Subscription,Slot
from order.serializers import SubscriptionListingSerializer,MySubscriptionSerializer
from expert.serializers import AddSlotSerializer,ListingSlotSerializer,BookedSlotSerializer
from datetime import date
from background_task import background
from django.utils import timezone
from datetime import timedelta,datetime

# Create your views here.

class ExpertProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # getting expert profile details
    def get(self,request):
        try:
            id = request.GET.get('id')
            if request.query_params['person'] == 'expert':
                expert = Expert.objects.get(user=id)
                expert_serializer  = ExpertsListSerializer(expert)
                subscribed = Subscription.objects.filter(expert=expert.id).order_by('-id')
                current_date = date.today()
                slots = Slot.objects.filter(expert=expert.id,day=current_date)
                if subscribed and slots:
                    subscription_serializer = MySubscriptionSerializer(subscribed,many=True)
                    slot_serializer = ListingSlotSerializer(slots,many=True)
                    return Response({'status':200,'payload':expert_serializer.data,'MyStudents':subscription_serializer.data,'slots':slot_serializer.data})
                if subscribed:
                    subscription_serializer = MySubscriptionSerializer(subscribed,many=True)
                    return Response({'status':200,'payload':expert_serializer.data,'MyStudents':subscription_serializer.data})
                return Response({'status':200,'payload':expert_serializer.data})
            return Response({"error":'some wrong'})
        except Exception as e:
            return Response({'error':e})
    # for update profile
    def patch(self,request):
        try:
            instance = CustomUser.objects.get(id=request.data['user'])
            Registration_serializer = EditProfileSerializer(instance=instance,data=request.data)
            if not Registration_serializer.is_valid():
                return Response({'error':Registration_serializer.errors,'message':'something for Registration serializer'})
            Registration_serializer.save()
            exp_instance = Expert.objects.get(id=request.data['id']) 
            if  request.data['profile_poto'] == 'null':
                expert_serializer = ExpertEditSerializer01(instance=exp_instance,data=request.data)
                if not expert_serializer.is_valid():
                  return Response({'error':expert_serializer.errors,'message':'something for Expert serializer'})
                expert_serializer.save()
                return Response({'status':200,'message':'Your profile Updated successfully'})       
            else:
                expert_serializer =  ExpertEditSerializer(instance=exp_instance,data=request.data)
                if not expert_serializer.is_valid():
                    return Response({'error':expert_serializer.errors,'message':'something for Expert serializer'})
                expert_serializer.save()
                return Response({'status':200,'message':'Your profile Updated successfully'})
        except Exception as e:
            return Response({'error':e})
        
        
class SlotsManage(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # add slots
    def post(self,request):
        try:
            for i in request.data['array']:
                serializer = AddSlotSerializer(data=i)
                if not serializer.is_valid():
                    return Response({'error':serializer.errors})
                serializer.save()        
            return Response({'message':'Tokens added successfully'})            
        except Exception as e:
            return Response({'error':e})
        
    # getting booked each slot information    
    def get(self,request):
        try:
            id = request.GET.get('id')
            slot = Slot.objects.get(id=id)
            serializer = BookedSlotSerializer(slot)
            return Response({'status':200,'payload':serializer.data})     
        except Exception as e:
            return Response({'error':e})
        

