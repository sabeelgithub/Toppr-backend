from rest_framework import serializers
from order.models import Slot


class AddSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'

class ListingSlotSerializer(serializers.ModelSerializer):
    expert_id = serializers.IntegerField(source='expert.id')
    expert_name = serializers.CharField(source='expert.user.username')
    class Meta:
        model = Slot
        fields = ['id','start_time','end_time','day','booked','expert_id','expert_name']

class BookedSlotSerializer(serializers.ModelSerializer):
    expert_id = serializers.IntegerField(source='expert.id')
    expert_name = serializers.CharField(source='expert.user.username')
    client_id = serializers.IntegerField(source='client.id')
    client_name = serializers.CharField(source='client.user.username')
    class Meta:
        model = Slot
        fields = ['id','start_time','end_time','day','booked','expert_id','expert_name','client_id','client_name']