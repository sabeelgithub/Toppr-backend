from rest_framework import serializers
from .models import *

# for registration
class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username','email','phone','password']

    def validate(self,data):
        if data['username']:
            for i in data['username']:
                if i.isdigit():
                    raise serializers.ValidationError({'error':'name cannot contain numbers'})
        if data['phone']:
            num = str(data['phone'])
            if len(num) > 10 :
                raise serializers.ValidationError({'error':'phone number not more than 10'})
        
        return data
    
    def create(self, validated_data):
        user = CustomUser.objects.create(email=validated_data['email'])
        user.username = validated_data['username']
        user.phone = validated_data['phone']
        user.set_password(validated_data['password'])
        user.save()
        return user


class ExpertSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Expert
        fields = '__all__'

class ClientSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class EditProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username','email','phone']


## in the case of updating profile poto
class ExpertEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expert
        fields = ['id','user','profile_poto']

## in the case of profile not updating
class ExpertEditSerializer01(serializers.ModelSerializer):
    class Meta:
        model = Expert
        fields = ['id','user']

   




        
    





  