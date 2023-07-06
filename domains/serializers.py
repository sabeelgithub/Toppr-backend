from rest_framework import serializers
from .models import *

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'

class TutorialSerializer(serializers.ModelSerializer):
    domain = serializers.CharField(source='domain.domain_name')
    domain_id = serializers.IntegerField(source='domain.id')
    class Meta:
        model = Tutorial
        fields = ['id','tutorial_name','created_at','updated_at','domain','domain_id']

class PostTutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields = '__all__'

class Sub_TutorialSerializer(serializers.ModelSerializer):
    domain = serializers.CharField(source='domain.domain_name')
    domain_id = serializers.IntegerField(source='domain.id')
    tutorial = serializers.CharField(source='tutorial.tutorial_name')
    tutorial_id = serializers.IntegerField(source='tutorial.id')
    class Meta:
        model = Sub_tutorial
        fields = ['id','sub_tutorial_name','description','tutorial','tutorial_id','domain','domain_id']

class PostSubTutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sub_tutorial
        fields = '__all__'