from django.db import models
from accounts.models import *

# Create your models here.


class Domain(models.Model):
    domain_name = models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=1000)
    price = models.IntegerField()
    image = models.ImageField(upload_to='domain/image',default='upload_photo')
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)
    blocked = models.BooleanField(default=False)

    def __str__(self):  
        return f'{self.domain_name}' 

class Tutorial(models.Model):
    tutorial_name = models.CharField(max_length=100)
    domain = models.ForeignKey(Domain,on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('tutorial_name', 'domain')

    def __str__(self):  
        return f'{self.tutorial_name}' 

class Sub_tutorial(models.Model):
    sub_tutorial_name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    tutorial = models.ForeignKey(Tutorial,on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('sub_tutorial_name', 'tutorial')

    def __str__(self):  
        return f'{self.sub_tutorial_name}' 











