from rest_framework import serializers
from .models import *


# taking users domain purchase during login time

class DomainAlreadyPurchasedSerializer(serializers.ModelSerializer):
    domain_id = serializers.IntegerField(source='domain.id')
    class Meta:
        model = Domain_purchase
        fields = ['domain_id']

# purchasing domains
class DomainPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Domain_purchase
        fields= '__all__'


# get domain purchases list
class DomainListingSerializer(serializers.ModelSerializer):
    domain_name = serializers.CharField(source='domain.domain_name')
    domain_id = serializers.IntegerField(source='domain.id')
    user_name = serializers.CharField(source='user.username')
    user_id = serializers.IntegerField(source='user.id')

    class Meta:
        model = Domain_purchase
        fields = ['id','order_id','domain_name','domain_id','price','user_name','user_id','created_at']

# Rating serializer
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating 
        fields = '__all__'  

# Listing Ratings in admin side
class RatingListSerializer(serializers.ModelSerializer):
    expert_name = serializers.CharField(source='expert.user.username')
    domain_name = serializers.CharField(source='domain.domain_name')
    class Meta:
        model = Rating
        fields = ['id','expert_name','domain_name','count'] 

class GetRatingPerticularDomainRatingSerializer(serializers.ModelSerializer):
    domain_id = serializers.IntegerField(source='domain.id')
    domain_name = serializers.CharField(source='domain.domain_name')
    expert_name = serializers.CharField(source='expert.user.username')
    expert_id = serializers.IntegerField(source='expert.id')
    class Meta:
        model = Rating 
        fields = ['domain_id','domain_name','expert_name','expert_id','count']   


# subscribing serializer

class SubscribingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


# get Subscription list to admin
class SubscriptionListingSerializer(serializers.ModelSerializer):
    domain_name = serializers.CharField(source='domain.domain_name')
    client_name = serializers.CharField(source='client.user.username')
    expert_name = serializers.CharField(source='expert.user.username')
    class Meta:
        model = Subscription
        fields = ['id','order_id','expert_name','client_name','domain_name','amount','duration','admin_share','expert_share','subscription_date','status','expire_on','terminated']



# taking users subscription during login time

class AlreadySubscribedSerializer(serializers.ModelSerializer):
    domain_id = serializers.IntegerField(source='domain.id')
    domain_name = serializers.CharField(source='domain.domain_name')
    expert_id = serializers.IntegerField(source='expert.id')
    expert_name = serializers.CharField(source='expert.user.username')
    class Meta:
        model = Subscription
        fields = ['domain_id','domain_name','expert_id','expert_name']


class MySubscriptionSerializer(serializers.ModelSerializer):
    domain_name = serializers.CharField(source='domain.domain_name')
    client_name = serializers.CharField(source='client.user.username')
    expert_name = serializers.CharField(source='expert.user.username')
    expert_id = serializers.CharField(source='expert.id')
    expert_poto = serializers.ImageField(source='expert.profile_poto')
    client_poto = serializers.ImageField(source='client.profile_poto')
    class Meta:
        model = Subscription
        fields = ['id','order_id','expert_name','client_name','domain_name','amount','duration','admin_share','expert_share','subscription_date','status','expire_on','expert_id','expert_poto','client_poto','terminated']