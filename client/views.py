from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import APIView
from accounts.models import Expert,Client,CustomUser
from accounts.serializers import EditProfileSerializer,ClientSerializerPost
from domains.models import Domain,Tutorial,Sub_tutorial
from adminpanel.serializers import ExpertsListSerializer
from domains.serializers import DomainSerializer,TutorialSerializer,Sub_TutorialSerializer
from  rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from order.serializers import DomainPurchaseSerializer,RatingSerializer,GetRatingPerticularDomainRatingSerializer,SubscribingSerializer
from order.models import Rating,Subscription,Domain_purchase,Slot
from datetime import timedelta
from django.utils import timezone
from background_task import background
from adminpanel.serializers import ClientsListSerializer,ExpertsListSerializer
from order.serializers import DomainListingSerializer,MySubscriptionSerializer
from datetime import date
from expert.serializers import ListingSlotSerializer
import math


# Create your views here.




class Tutorials(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # get tutorial
    def get(self,request):
        try:
            tutorials = Tutorial.objects.all().order_by('-id')
            serializer = TutorialSerializer(tutorials,many=True)
            return Response({'status':200,'payload':serializer.data})
        except Exception as e:
            return Response({'error':e})
        

class SubTutorials(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # get tutorial
    def get(self,request):
        try:
            sub_tutorials = Sub_tutorial.objects.all().order_by('-id')
            serializer = Sub_TutorialSerializer(sub_tutorials,many=True)
            return Response({'payload':serializer.data,'status':200,'message':'checking'})
        except Exception as e:
            return Response({'error':e})


# domain purchase 

class Domain_Purchasing(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            serializer = DomainPurchaseSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'error':serializer.errors})
            serializer.save()
            return Response({'status':200,'message':'success'})
        except Exception as e:
            return Response({'error':e})


# get single domain with domain_name came from front-end

class Single_Domain(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            domain_name = request.GET.get('domain_name')
            domain = Domain.objects.get(domain_name=domain_name)
            serializer = DomainSerializer(domain)
            return Response({'status':200,'payload':serializer.data})
        except Exception as e:
            return Response({'error':e})

# get experts for each perticular domain

class getExpertsToPerticularDomain(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            # print(request.query_params)
            domain_name = request.GET.get('domain_name')
            domain = Domain.objects.get(domain_name=domain_name)
            experts = Expert.objects.filter(domain=domain.id,user__is_block=False,user__is_verified='true') 
            subscribe = Subscription.objects.filter(status=True,domain=domain.id)
            # filter experts which have subscription more than 7
            filter_experts = Expert.objects.none() 
            for i in experts:
                for j in subscribe:
                    if i.id == j.expert.id:
                        count = Subscription.objects.filter(status=True,expert=i.id).count()
                        print(count)
                        if count > 6:
                            break
                        else:
                            instance = Expert.objects.filter(id=i.id)
                            filter_experts = filter_experts | instance
                            break
                else:          
                    instance = Expert.objects.filter(id=i.id)   
                    filter_experts = filter_experts | instance
            serializer = ExpertsListSerializer(filter_experts,many=True)
            rating = Rating.objects.filter(domain=domain.id)
            rating_serializer = GetRatingPerticularDomainRatingSerializer(rating,many=True)
            return Response({'status':200,'payload':serializer.data,'rating':rating_serializer.data})
        except Exception as e:
            return Response({'error':e})
        

# get single Experts to single expert page
class getSingleExpertDetails(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            # fetching experts details
            id = request.GET.get('id')
            expert = Expert.objects.get(id=id)
            rating = Rating.objects.get(expert__id=id)
            expert_serializer = ExpertsListSerializer(expert)
            rating_serializr = GetRatingPerticularDomainRatingSerializer(rating)
            current_date = date.today()
            slots = Slot.objects.filter(expert=expert.id,day=current_date)
            client_booked_slot = Slot.objects.filter(booked=True,client__user__id=request.GET.get('user_id'),day=current_date,expert=request.GET.get('id'))
            print(client_booked_slot,'cgh')
            if slots and client_booked_slot:
                slots_serializer = ListingSlotSerializer(slots,many=True) # all experts slots for perticular day
                client_booked_slot_serializer = ListingSlotSerializer(client_booked_slot,many=True)
                return Response({'status':200,'payload':expert_serializer.data,'rating':rating_serializr.data,'slots':slots_serializer.data,'client_already_booked_slot':client_booked_slot_serializer.data})
            if slots:
                slots_serializer = ListingSlotSerializer(slots,many=True)
                return Response({'status':200,'payload':expert_serializer.data,'rating':rating_serializr.data,'slots':slots_serializer.data})
            return Response({'status':200,'payload':expert_serializer.data,'rating':rating_serializr.data})
        except Exception as e:
            return Response({'error':e})

@background(schedule=60*60*24)  # Run the task every 24 hours (1 day)
def update_subscription_status(subscription_id):
    try:
        subscribed = Subscription.objects.get(id=subscription_id)
        subscribed.status = False
        subscribed.save()
    except Subscription.DoesNotExist:
        pass  

@background(schedule=60*60*24)  # Run the task every 24 hours (1 day) 
def update_subscription_amount(subscription_id):
    try:
        subscribed = Subscription.objects.get(id=subscription_id)
        exp = subscribed.expert
        id = exp.id
        expert = Expert.objects.get(id=id)
        if expert.wallet is None:
            expert.wallet = subscribed.salary
        else:
            expert.wallet += subscribed.salary
        expert.save()
        subscribed.salary = 0
        subscribed.save()
    except Subscription.DoesNotExist:
        pass  

#  subscribing
class Subscribe(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            admin_share = int(request.data['amount'] * 0.30)
            expert_share = int(request.data['amount'] - admin_share)
            expert = Expert.objects.get(id=request.data['expert'])
            client = Client.objects.get(user=request.data['client'])
            data = request.data.copy()
            data['client'] = client.id
            data['admin_share'] = admin_share
            data['expert_share'] = expert_share
            data['salary'] = expert_share
            serializer = SubscribingSerializer(data=data)
            if not serializer.is_valid():
                return Response({'error':serializer.errors})
            serializer.save()
            month=serializer.data['duration']
            id = serializer.data['id']
            subscribed = Subscription.objects.get(id=serializer.data['id'])
            duration = subscribed.duration
            # expiration_date = timezone.now() + timedelta(minutes=2)
            expiration_date = timezone.now() + timedelta(days=30*duration)
            subscribed.expire_on = expiration_date
            subscribed.save()
            update_subscription_status(schedule=expiration_date, subscription_id=subscribed.id)
            update_subscription_amount(schedule=expiration_date, subscription_id=subscribed.id)
            return Response({'status':200,'message':f'You are successfully Subscribed {expert} for {month} months'})
        except Exception as e:
            return Response({'error':e})
        


class ClientProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # get profile
    def get(self,request):
        try:
            id = request.GET.get('id')
            if request.query_params['person'] == 'client':
                client = Client.objects.get(user=id)
                client_serializer = ClientsListSerializer(client)
                purchased_domains = Domain_purchase.objects.filter(user=id).order_by('-id')
                subscribed = Subscription.objects.filter(client=client.id).order_by('-id')
                if purchased_domains and subscribed:
                    domain_serializer = DomainListingSerializer(purchased_domains,many=True)
                    subscribed_serializer = MySubscriptionSerializer(subscribed,many=True)
                    return Response({'status':200,'payload':client_serializer.data,'MyDomains':domain_serializer.data,'MyTeachers':subscribed_serializer.data})
                if purchased_domains:
                    domain_serializer = DomainListingSerializer(purchased_domains,many=True)
                    return Response({'status':200,'payload':client_serializer.data,'MyDomains':domain_serializer.data})
                return Response({'status':200,'payload':client_serializer.data})
            return Response({'error':'something happened'})
        except Exception as e:
            return Response({'error':e})
    # update profile  
    def patch(self,request):
        try:
            instance = CustomUser.objects.get(id=request.data['id'])
            Registration_serializer = EditProfileSerializer(instance=instance,data=request.data)
            if not Registration_serializer.is_valid():
                return Response({'error':Registration_serializer.errors,'message':'something for Registration serializer'})
            Registration_serializer.save()   
            data = request.data.copy()
            data['user'] = instance.id
            cl_instance = Client.objects.get(user=instance.id)
            client_serializer = ClientSerializerPost(instance=cl_instance,data=data)
            if not client_serializer.is_valid():
                return Response({'error':client_serializer.errors,'message':'something for Registration serializer'})
            client_serializer.save()
            return Response({'status':200,'message':'Your profile Updated succesfully'})
        except Exception as e:
            return Response({'error':e})
    

class SlotBooking(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # slot booking
    def patch(self,request):
        try:
            client = Client.objects.get(user=request.data['user_id'])
            slot = Slot.objects.get(id=request.data['id'])
            slot.client = client
            slot.booked = True
            slot.save()
            booked_slot = Slot.objects.get(id=request.data['id'])
            slot_serializer = ListingSlotSerializer(booked_slot)
            return Response({'status':200,'message':'Slot booked successfully,waiting for you time','booked_slot':slot_serializer.data})
        except Exception as e:
            return Response({'error':e})
        
class SubmitRating(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            rating = Rating.objects.get(expert=request.data['expert'])
            new_count = math.floor(((rating.count + request.data['count'])/(rating.number_of_person + 1)))
            rating.count = new_count
            rating.number_of_person += 1
            rating.save()
            return Response({'status':200,'message':f'Your rating for {rating} recorded successfully'})
        except Exception as e:
            return Response({'error':e})



   
    
        




