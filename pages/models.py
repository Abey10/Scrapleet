from django.db import models
from django.contrib.auth import get_user_model

class Blog(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    

class Service(models.Model):
    service_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    rate = models.FloatField() 
    min = models.IntegerField()
    max = models.IntegerField()
    dripfeed = models.BooleanField()
    refill = models.BooleanField()
    cancel = models.BooleanField()
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.name


