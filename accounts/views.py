from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import * 
from django.contrib.auth import authenticate, login
from  rest_framework_simplejwt.authentication import JWTAuthentication
from order.models import Domain_purchase,Subscription
from order.serializers import DomainAlreadyPurchasedSerializer,AlreadySubscribedSerializer
from rest_framework_simplejwt.tokens import RefreshToken





# Create your views here.

# registion finction for all including client and expert
class Register(APIView):
    def post(self,request):
        if request.data['person'] == 'client':
            serializer = RegisterSerializer(data=request.data)
            print(serializer)
            if not serializer.is_valid():
                return Response({'error':serializer.errors,'message':'something for serializer'})
            serializer.save()
            user = CustomUser.objects.get(email=request.data['email'])
            print(user)
            user.is_client = True
            user.save()
            client = Client.objects.create(user_id = user.id)
            client.save()
            return Response({'message':'success','payload':serializer.data,'status':200})
        elif request.data['person'] == 'expert':
            serializer = RegisterSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'error':serializer.errors,'message':'something for serializer'})
            serializer.save()
            user = CustomUser.objects.get(email=request.data['email'])
            user.is_expert = True
            user.is_verified = 'false'
            user.save()
            # copy data coming from request
            data = request.data.copy() 
            # Add the extra object to the data dictionary 
            data['user'] = user.id
            expert_serializer = ExpertSerializerPost(data=data)
            if not expert_serializer.is_valid():
                print(expert_serializer.errors)
                return Response({'error':expert_serializer.errors,'message':'something for expertserializer'})
            expert_serializer.save()
            return Response({'message':'success expert','payload':serializer.data,'status':200})
        else:
            return Response({'message':'something went wrong'})
        


# Login for all including client,expert and admin
class Login(APIView):
    def post(self,request):
        try:
            email = request.data['email']
            password = request.data['password']
            user = authenticate(email=email,password=password) 
            if user is not None:
                obj = CustomUser.objects.get(email=email)
                if obj.is_client == True:
                    person = 'client'
                if obj.is_expert == True:
                    person = 'expert'
                if obj.is_superuser == True:
                    person = 'admin'
                if user.is_active == True and user.is_verified=='true' and user.is_block == False:
                    username = user.username
                    login(request,user)
                    refresh = RefreshToken.for_user(user)
                    domain_orders = Domain_purchase.objects.filter(user=user.id) 
                    subscriptions = Subscription.objects.filter(client__user__id=user.id,status=True)
                    if domain_orders and subscriptions: 
                      domain_serializer = DomainAlreadyPurchasedSerializer(domain_orders,many=True)
                      subscription_serializer = AlreadySubscribedSerializer(subscriptions,many=True)
                      return Response({'message':'you are successfully logged','status':200,'refresh':str(refresh),'access':str(refresh.access_token),'username':username,'person':person,'domains':domain_serializer.data,'subscribed':subscription_serializer.data})
                    if domain_orders:
                      domain_serializer = DomainAlreadyPurchasedSerializer(domain_orders,many=True)       
                      return Response({'message':'you are successfully logged','status':200,'refresh':str(refresh),'access':str(refresh.access_token),'username':username,'person':person,'domains':domain_serializer.data})
                    
                    return Response({'message':'you are successfully logged','status':200,'refresh':str(refresh),'access':str(refresh.access_token),'username':username,'person':person})
                elif user.is_active == True and user.is_verified == 'false':
                    exists = Expert.objects.filter(user=user.id).exists()
                    if exists:
                        return Response({'message':'We are Checking Your certificate,Login After 1 Day ','status':600})
                    user.delete()
                    return Response({'message':'unfortunatly we deleted the domain you selecetd,Register again with new domain ','status':600})
                    
                elif user.is_active == True and user.is_verified == 'rejected':
                    user.delete()
                    return Response({'message':'Unfortunatly we are not moving with your Certificate,Try Again with new certificate','status':500})
                elif user.is_block==True:
                    return Response({'message':'you are blocked','status':700})
                else :
                    return Response({'message':'something happend','status':800})
            else:
                return Response({'message':'inavalid username or password','status':404})
                    
        except Exception as e:
            return Response({'error':e})
        


        



        



