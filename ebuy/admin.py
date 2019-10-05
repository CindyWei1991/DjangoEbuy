from django.contrib import admin
from ebuy.models import Product, UserProfile
 
# Register your models here.
 
admin.site.register(Product)
#admin.site.register(ProductImages)
# admin.site.register(Comment)
admin.site.register(UserProfile)

