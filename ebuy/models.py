from __future__ import unicode_literals
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
from choices import *
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

def getpath(instance,filename):
    return "profile/%s-%s" % (instance.id,filename) 

def get_image_filename(instance, filename):
        title = instance.title
        slug = slugify(title)
        return "post_images/%s-%s" % (slug, filename) 

class Product(models.Model):
    img1 = models.ImageField(upload_to=get_image_filename, 
                               )
    img2 = models.ImageField(upload_to=get_image_filename, 
                               )
    img3 = models.ImageField(upload_to=get_image_filename, 
                            )

    title = models.CharField(max_length=30, default="")
    description = models.TextField()
    availability = models.PositiveIntegerField(default="10", blank=True)                                                                                                                                                                                                                                                                                                                                                                                       
    price = models.DecimalField(max_digits=11, decimal_places=2)
    category = models.CharField(max_length=3, choices=CATEGORIES)
    size = models.CharField(max_length=30, default="One Size")
    color = models.CharField(max_length=30, default="")
    content_type = models.CharField(max_length=50,default='')

    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    age = models.CharField(max_length=3,default='20')
    image = models.FileField(upload_to='profile', blank=True,default='default.jpg')
    content_type = models.CharField(max_length=50,default='')
    wishList = models.ManyToManyField(Product, related_name='wishList', 
                                         blank=True)
    order = models.ManyToManyField(Product, related_name='order', blank=True)
    def __unicode__(self):
        return self.firstName + self.lastName
    def __str__(self):
        return self.__unicode__()

class Bag(models.Model):
    owner = models.ForeignKey(User, related_name='owner')
    itemsInBag = models.ManyToManyField(Product, related_name='itemsInBag', 
                                         blank=True)
    def __unicode__(self):
        return self.owner.username

class Amount(models.Model):
    product = models.ForeignKey(Product)
    bag = models.ForeignKey(Bag)
    amount = models.PositiveIntegerField(default=1, blank=True, 
           validators=[MaxValueValidator(9), MinValueValidator(1)])

def get_shared_img_path(instance, filename):
        title = instance.title
        slug = slugify(title)
        return "sharedProduct/%s-%s" % (slug, filename) 

class SharedProduct(models.Model):
    user = models.ForeignKey(User,null=True)
    img = models.FileField(upload_to=get_shared_img_path,blank=False)
    title = models.CharField(max_length=20,blank=False)
    text = models.CharField(max_length=500,blank=False)
    content_type = models.CharField(max_length=50,default='')

    def __unicode__(self):
        return self.text


class Comment(models.Model):
    text = models.CharField(max_length=500,default="",null=True)
    user = models.ForeignKey(User)
    time = models.DateTimeField()
    product=models.ForeignKey(Product,default='',null=True)
    def __unicode__(self):
        return self.text