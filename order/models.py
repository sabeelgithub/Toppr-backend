from django.db import models
from accounts.models import Client
from domains.models import Domain
from accounts.models import CustomUser,Expert
from datetime import date

# Create your models here.

class Domain_purchase(models.Model):
    order_id = models.CharField(max_length=100)
    domain = models.ForeignKey(Domain,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True)
    price = models.IntegerField()
    created_at = models.DateField(auto_now=True)

    def __str__(self):  
        return f'{self.domain.domain_name}'
    

class Rating(models.Model):
    expert = models.ForeignKey(Expert,on_delete=models.SET_NULL,null=True)
    domain = models.ForeignKey(Domain,on_delete=models.SET_NULL,null=True)
    count = models.IntegerField(default=5)
    number_of_person = models.IntegerField(default=1,null=True)

    def __str__(self):  
        return f'{self.expert.user.username}'
    

class Subscription(models.Model):
    order_id = models.CharField(max_length=100,default=0)
    expert = models.ForeignKey(Expert,on_delete=models.SET_NULL,null=True)
    client = models.ForeignKey(Client,on_delete=models.SET_NULL,null=True)
    domain = models.ForeignKey(Domain,on_delete=models.SET_NULL,null=True)
    duration = models.IntegerField()
    amount = models.IntegerField()
    status = models.BooleanField(default=True)
    subscription_date = models.DateField(auto_now=True)
    admin_share = models.IntegerField()
    expert_share =  models.IntegerField()
    expire_on = models.DateField(null=True)
    salary = models.IntegerField(null=True)
    terminated = models.BooleanField(default=False,null=True)



    def __str__(self):  
        return f'{self.expert.user.username}'
    


class Slot(models.Model):
    expert = models.ForeignKey(Expert,on_delete=models.CASCADE)
    client = models.ForeignKey(Client,on_delete=models.CASCADE,null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.DateField(auto_now=True)
    booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Slot: {self.expert.user.username} (Start: {self.start_time}, End: {self.end_time})"





