from rest_framework import serializers
from .models import *
from accounts.models import *



# client list serializer   
class ClientsListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    phone = serializers.IntegerField(source='user.phone')
    status = serializers.BooleanField(source='user.is_block')
    id = serializers.IntegerField(source='user.id')
    class Meta:
        model = Client
        fields = ['username','email','phone','status','id','profile_poto','wallet']

# expert list serializer
class ExpertsListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    phone = serializers.IntegerField(source='user.phone')
    status = serializers.BooleanField(source='user.is_block')
    user_id = serializers.IntegerField(source='user.id')
    domain_id = serializers.IntegerField(source='domain.id')
    domain = serializers.CharField(source='domain.domain_name')
    class Meta:
        model = Expert
        fields = ['id','username','email','phone','domain_id','domain','status','user_id','profile_poto','wallet']


# pending experts serializer
class PendingExpertSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    phone = serializers.IntegerField(source='user.phone')
    user_id = serializers.IntegerField(source='user.id')
    domain_id = serializers.IntegerField(source='domain.id')
    domain = serializers.CharField(source='domain.domain_name')
    class Meta:
        model = Expert
        fields = ['id','username','email','phone','user_id','domain_id','domain','certificate','profile_poto']