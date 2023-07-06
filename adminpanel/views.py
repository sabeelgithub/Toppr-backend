from django.shortcuts import render
from domains.models import Domain,Tutorial,Sub_tutorial
from .serializers import * 
from domains.serializers import DomainSerializer,TutorialSerializer,PostTutorialSerializer,Sub_TutorialSerializer,PostSubTutorialSerializer
from accounts.models import Client,CustomUser,Expert
from rest_framework.views import APIView
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework import generics
from  rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from order.models import Domain_purchase,Rating,Subscription
from order.serializers import DomainListingSerializer,RatingSerializer,SubscriptionListingSerializer,RatingListSerializer
import datetime
import calendar





# Create your views here.
        
# clients
class ClientsList(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    # get clients list
    def get(self,request):
        
       
        try:
            clients = Client.objects.filter(user__is_client=True).order_by('-id')
            serializer = ClientsListSerializer(clients,many=True)
            return Response({'payload':serializer.data,'message':'success'})       
        except Exception as e:
            return Response({'error':e})
    
    # blocking and unblocking mechanism of clients
    def patch(self,request):
        try:
            user = CustomUser.objects.get(id=request.data['id'])
            username = user.username
            if request.data['status'] == True:
                user.is_block = False
                user.save()
                return Response({'message':f'{username} is Unblocked'})
            if request.data['status'] == False:
                user.is_block = True
                user.save()
                return Response({'message':f'{username} Blocked'})

        except Exception as e:
            return Response({'error':e})

        
# experts
class ExpertsList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    
    # get experts list
    def get(self,request):
        try:
            experts = Expert.objects.filter(user__is_expert=True,user__is_verified='true').order_by('-id')
            serializer = ExpertsListSerializer(experts,many=True)
            return Response({'payload':serializer.data,'message':'success'})

        except Exception as e:
            return Response({'error':e})

    # blocking and unblocking mechanism of expets   
    def patch(self,request):
        try:
            user = CustomUser.objects.get(id=request.data['id'])
            username = user.username
            if request.data['status'] == True:
                user.is_block = False
                user.save()
                return Response({'message':f'{username} is Unblocked'})
            if request.data['status'] == False:
                user.is_block = True
                user.save()
                # handling his subscription
                subscribe = Subscription.objects.filter(expert__user__id=request.data['id'],status=True)
                if subscribe:
                    for i in subscribe:
                        i.status = False
                        i.terminated = True
                        current_date = datetime.date.today()
                        teached = current_date-i.subscription_date
                        salary = i.salary
                        days = i.duration*30
                        single_day_salary = salary/days
                        expert_amount = teached.days*single_day_salary
                        client_amount = salary-expert_amount
                        expert = Expert.objects.get(id=i.expert.id)
                        if expert.wallet is None:
                            expert.wallet = int(expert_amount)
                        else:
                            expert.wallet += int(expert_amount)
                        expert.save()
                        client = Client.objects.get(id=i.client.id)
                        print(client)
                        if client.wallet is None:
                            client.wallet = int(client_amount)
                        else:
                            client.wallet += int(client_amount)
                        client.save()
                        i.salary = 0
                        i.save()
                    return Response({'message':f'{username} is blocked and all his subscription are cancelled'})
                return Response({'message':f'{username} is blocked'})       
        except Exception as e:
            return Response({'error':e})
        

# pending experts handle
class PendingExperts(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self,request):
        try:
            experts = Expert.objects.filter(user__is_verified='false').order_by('-id')
            serializer = PendingExpertSerializer(experts,many=True)
            return Response({'payload':serializer.data,'message':'checking'})

        except Exception as e:
            return Response({'error':e})
        

# get single pending experts
class PendingSingleExpert(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    def get(self,request,id):
        try:
            user = Expert.objects.get(user__id =id)
            serializer = PendingExpertSerializer(user)
            return Response({'payload':serializer.data,'message':'checking'})
        except Exception as e:
            return Response({'error':e})
    def patch(self,request,id):
        try:
            user = CustomUser.objects.get(id=id)
            if request.data['type'] == 'add':
                user.is_verified = 'true'
                user.save()
                rating_serializer = RatingSerializer(data=request.data)               
                if not rating_serializer.is_valid():
                    return Response({'message':rating_serializer.errors})
                rating_serializer.save() 
                return Response({'status':250,'message':f'{user} is added to expert'})
            if request.data['type'] == 'delete':
                user.is_verified = 'rejected'
                user.save()
                return Response({'status':500,'message':f'{user} is rejected'})
        except Exception as e:
            return Response({'error':e})
        

# get domain list
class Domains(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    #listing domains
    def get(self,request):
        try:
            domain = Domain.objects.all().order_by('-id')
            serializer = DomainSerializer(domain,many=True)
            return Response({'payload':serializer.data})
        except Exception as e:
            return Response({'error':e})
    
    #delete domain
    def delete(self,request):
        try:
            id = request.GET.get('id')
            domain = Domain.objects.get(id=id)
            if request.query_params['status'] == 'false':
                domain.blocked = True
                domain.save()
                return Response({'status':200,'message':f'Domain {domain} is Blocked'})
            elif request.query_params['status'] == 'true':
                domain.blocked = False
                domain.save()
                return Response({'status':200,'message':f'Domain {domain} is Unblocked'})
            else:
                return Response({'error':'something went wrong'})
         
        except Exception as e:
            return Response({'error':e})
    # add domain
    def post(self,request):
        try:
            domain_name = request.data['domain_name']
            serializer = DomainSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'status':300,'error':serializer.errors,'message':'something went wrong'})
            serializer.save()
            return Response({'status':200,'message':f'Domain {domain_name} is added successfully'})
        except Exception as e:
            return Response({'error':e})
        
    # edit domain
    def patch(self,request):
        try:
            instance = Domain.objects.get(id=request.data['id'])
            serializer = DomainSerializer(instance=instance,data=request.data)       
            if not serializer.is_valid():
                return Response({'error':serializer.errors,'message':'somthing for serializer'})   
            serializer.save()
            return Response({'status':200,'message':f'domain {instance} is updated successfully'})
        except Exception as e:
            return Response({'error':e})
    

class Tutorials(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    # get tutorial
    def get(self,request):
        try:
            tutorials = Tutorial.objects.all().order_by('-id')
            serializer = TutorialSerializer(tutorials,many=True)
            return Response({'status':200,'payload':serializer.data})
        except Exception as e:
            return Response({'error':e})
    # delete tutorial   
    def delete(self,request):
        try:
            id = request.GET.get('id')
            tutorial = Tutorial.objects.get(id=id)
            tutorial.delete()
            return Response({'status':200,'message':f'Tutorial {tutorial} deleted successfully'})
        except Exception as e:
            return Response({'error':e})
    # add tutorial
    def post(self,request):
        try:
            domain = Domain.objects.get(domain_name=request.data['domain'])
            data = request.data.copy()
            data['domain']= domain.id
            serializer = PostTutorialSerializer(data=data)
            if not serializer.is_valid():
                return Response({'status':300,'error':serializer.errors,'message':'something for serializer'})
            serializer.save()
            tutorial=serializer.data['tutorial_name']
            return Response({'status':200,'message':f'{tutorial} added successfully'})
        except Exception as e:
            return Response({'error':e})
    # edit tutorial
    def patch(self,request):
        try:         
            tutorial = Tutorial.objects.get(id=request.data['id'])
            serializer = PostTutorialSerializer(instance=tutorial,data=request.data)
            if not serializer.is_valid():
                return Response({'status':300,'error':serializer.errors,'message':'somthing for serializer'})   
            serializer.save()
            return Response({'status':200,'message': f'{tutorial} updated successfully'})
        except Exception as e:
            return Response({'error':e})
        

class SubTutorials(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    # get tutorial
    def get(self,request):
        try:
            sub_tutorials = Sub_tutorial.objects.all().order_by('-id')
            serializer = Sub_TutorialSerializer(sub_tutorials,many=True)
            return Response({'payload':serializer.data,'status':200,'message':'checking'})
        except Exception as e:
            return Response({'error':e})
    # delete sub-tutorial  
    def delete(self,request):
        try:
            id = request.GET.get('id')
            sub_tutorial = Sub_tutorial.objects.get(id=id)
            sub_tutorial.delete()
            return Response({'status':200,'message':f'{sub_tutorial} is deleted'})
        except Exception as e:
            return Response({'error':e})
    # add new sub tutorial
    def post(self,request):
        try:
            sub_tutorial = request.data['sub_tutorial_name']
            serializer = PostSubTutorialSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'error':serializer.errors,'message':'somthing for serialize'})
            serializer.save()   
            return Response({'status':200,'message':f'{sub_tutorial} is added successfully' })
        except Exception as e:
            return Response({'error':e})
    # edit sub-tutorial   
    def patch(self,request):
        try:
            sub_tutorial = Sub_tutorial.objects.get(id=request.data['id'])
            serializer = PostSubTutorialSerializer(instance=sub_tutorial,data=request.data)
            if not serializer.is_valid():
                return Response({'error':serializer.errors,'message':'something for serializer'})
            serializer.save()
            return Response({'status':200,'message':f'{sub_tutorial} updated successfully'})
        except Exception as e:
            return Response({'error':e})

class getRating(APIView):
    # listing experts rating in admin side
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    def get(self,request):
        try:
            ratings = Rating.objects.filter(expert__user__is_block=False)
            serializer = RatingListSerializer(ratings,many=True)
            return Response({'status':200,'payload':serializer.data})
        except Exception as e:
            return Response({'error':e})
       



class Order_Domains(APIView):
    # listing domain orders in admin side
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    def get(self,request):
        try:
            domain_orders = Domain_purchase.objects.all()
            serializer = DomainListingSerializer(domain_orders,many=True)
            return Response({'status':200,'payload':serializer.data})
        except Exception as e:
            return Response({'error':e})
        

class SubscriptionList(APIView):
    # listing subscriptions in admin side
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    def get(self,request):
        try:
            subscriptions = Subscription.objects.all()
            serializer = SubscriptionListingSerializer(subscriptions,many=True)
            return Response({'message':'checking','payload':serializer.data})
        except Exception as e:
            return Response({'error':e})


class Dashboard(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    # dashboard details
    def get(self,request):
        try:
            experts = Expert.objects.filter(user__is_verified='true').count()
            clients = Client.objects.all().count()
            domain_purchase = Domain_purchase.objects.all()
            total_domain_amount = 0
            subscriptions = Subscription.objects.all()
            total_subscription_amount = 0
            subscriptions_profilt = 0
            if domain_purchase and subscriptions:      
                for i in domain_purchase:
                    total_domain_amount += i.price
                for i in subscriptions:
                    total_subscription_amount += i.amount
                subscriptions_profilt = total_subscription_amount * 0.30
                total_earnings = total_domain_amount + total_subscription_amount
                total_profilt = total_domain_amount + subscriptions_profilt
                return Response({'message':200,'total_domain_amount':total_domain_amount,'total_subscription_amount':total_subscription_amount,'subscriptions_profilt':subscriptions_profilt,'total_earnings':total_earnings,'total_profilt':total_profilt,'experts':experts,'clients':clients})
                    
            if domain_purchase: 
                for i in domain_purchase:
                    total_domain_amount += i.price
                total_earnings = total_domain_amount 
                total_profilt = total_domain_amount 
                return Response({'message':200,'total_domain_amount':total_domain_amount,'total_earnings':total_earnings,'total_profilt':total_profilt,'experts':experts,'clients':clients})
            
            return Response({'status':200,'clients':clients,'experts':experts})
        except Exception as e:
            return Response({'error':e})
        
class Bargraph(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    # for dashboard bar graph
    def get(self,request):
        try:
            today = datetime.date.today()
            year = today.year
            months = []
            earnings = []
            profits = []
            for month in range(1,13):
                current_month_name = calendar.month_name[month]
                domain_purchase = Domain_purchase.objects.filter(created_at__year=year,created_at__month=month)
                subscription = Subscription.objects.filter(subscription_date__year=year,subscription_date__month=month)
                if domain_purchase and subscription :
                    months.append(current_month_name)
                    total_domain_purchase = 0
                    total_subscription = 0
                    profit_subscription = 0 
                    for i in domain_purchase:
                        total_domain_purchase += i.price    
                    for i in subscription:
                      total_subscription += i.amount  
                    for i in subscription:
                      profit_subscription += i.admin_share
                    earnings.append(total_domain_purchase+total_subscription)
                    profits.append(total_domain_purchase+profit_subscription)
                    
                if domain_purchase and not subscription:
                    months.append(current_month_name)
                    total_domain_purchase = 0
                    for i in domain_purchase:
                        total_domain_purchase += i.price
                    earnings.append(total_domain_purchase)
                    profits.append(total_domain_purchase)
                    
                if subscription and not domain_purchase:
                    months.append(current_month_name)
                    total_subscription = 0
                    profit_subscription = 0 
                    for i in subscription:
                      total_subscription += i.amount
                    for i in subscription:
                      profit_subscription += i.admin_share
                    earnings.append(total_subscription)
                    profits.append(profit_subscription)

            return Response({'message':200,'months':months,'earnings':earnings,'profits':profits})             
        except Exception as e:
            return Response({'error':e})
        

class Roundgraph(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    # for dashboard round graph
    def get(self,request):
        try:
            count = []
            non_terminated_subscription_count = Subscription.objects.filter(terminated=False).count()
            count.append(non_terminated_subscription_count)
            terminated_subscription_count = Subscription.objects.filter(terminated=True).count()
            count.append(terminated_subscription_count)
            return Response({'message':'200','count':count})
        except Exception as e:
            return Response({'error':e})

    




    
        
    
    





