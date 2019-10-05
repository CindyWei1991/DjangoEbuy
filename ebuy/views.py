from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse
from mimetypes import guess_type
from django.http import Http404, HttpResponse
from django.http import HttpResponseBadRequest

from django.http import Http404, HttpResponse, HttpResponseRedirect

from django.core import serializers
import json
# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail
from django.views.generic import TemplateView
from ebuy.models import *
from ebuy.forms import *
from decimal import *
# the main page displaying the latest products and nav bar
def home(request):
    context = {}
    newproducts=Product.objects.order_by("-id")[:3]
    context["product1"] = newproducts[0]
    context["product2"] = newproducts[1]
    context["product3"] = newproducts[2]
    return render(request, 'homepage.html',context)

@login_required
@transaction.atomic
def profile(request):
    context={}
    context['user'] = request.user
    context['allshares']=SharedProduct.objects.all()

    try:
        if request.method == 'GET':
            profile_edit = UserProfile.objects.get(user=request.user)
            form = EditForm(instance=profile_edit)
            context['profile']=profile_edit
            context['editform']= form 
            curr_bag = get_object_or_404(Bag, owner = request.user)
            context['amountData'] = Amount.objects.filter(bag = curr_bag)
            
            return render(request, 'profile.html', context)
    
        profile_edit = UserProfile.objects.select_for_update().get(user=request.user)
        form = EditForm(request.POST, request.FILES,instance=profile_edit)
        if not form.is_valid():
            context['profile'] =profile_edit
            context['editform']=form 
            context['status']='error'
            curr_bag = get_object_or_404(Bag, owner = request.user)
            context['amountData'] = Amount.objects.filter(bag = curr_bag)
            return render(request, 'profile.html', context)
        form.save()
        context['message']= 'Profile updated.'
        context['profile']=  profile_edit
        context['editform']=    form
        curr_bag = get_object_or_404(Bag, owner = request.user)
        context['amountData'] = Amount.objects.filter(bag = curr_bag)
        return render(request, 'profile.html', context)
    except UserProfile.DoesNotExist:
        raise Http404("This profile does not exist")
        return render(request, 'profile.html', context)


@transaction.atomic
def register(request):
    context = {}


    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.

    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'register.html', context)
        # If we get here the form data was valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email']
                                        )
    userprofile = UserProfile(user=new_user,
                            age=form.cleaned_data['age'],
                            firstName=form.cleaned_data['firstname'],
                            lastName=form.cleaned_data['lastname'])

    newBag = Bag(owner = new_user)
    
# Mark the user as inactive to prevent login before email confirmation.
    new_user.is_active = False
    new_user.save()
    newBag.save()
    userprofile.save()
    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)

    email_body = """
Welcome to E-Buy!  Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
""" % (request.get_host(), 
        reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
                message= email_body,
                from_email="jli4@andrew.cmu.edu",
                recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'need_confirm.html', context)
    # new_user.save()
    # userprofile.save()
    # newBag.save()

    # # Logs in the new user and redirects to his/her blogs
    # new_user = authenticate(username=form.cleaned_data['username'],
    #                         # first_name = form.cleaned_data['firstname'],
    #                         # last_name = form.cleaned_data['lastname'],
    #                         password=form.cleaned_data['password1'])
    # login(request, new_user)
    # return redirect(reverse('profile'))

@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'confirmed.html')
@transaction.atomic
def see_item(request, id):
    errors = []
    context = {}
    context['form'] = ItemAmountForm()
    comments=Comment.objects.all()
    context['comments']=comments
    if not request.user.is_anonymous():
        curr_bag = get_object_or_404(Bag, owner = request.user)
        context['amountData'] = Amount.objects.filter(bag = curr_bag)
    try:
        product = get_object_or_404(Product, id = id)
        avail = True
        if product.availability <= 0:
            avail = False
        context['product'] = product
        context['avail'] =avail
        return render(request, 'item.html',context)
    except ObjectDoesNotExist:
        errors.append("Cannot find this product.")
    if errors:
        context['errors'] = errors
        return render(request, 'item.html',context)

def get_images(request, id):
    curr_product = get_object_or_404(Product, id=id)
    images = curr_product.images.all()
    if not images:
        raise Http404
    return HttpResponse(images)

def displayByCategory(request,category):
    context = {}
    products = Product.objects.filter(category=category)
    context["products"] = products
    return render(request,'categoryshow.html',context)
def displayall(request):
    context={}
    products=Product.objects.all().order_by('title')
    context['products']=products
    return render (request,'displayall.html',context)


#get the product picture from media folder
def get_img1(request, id):
    product = get_object_or_404(Product, id=id)  
    if not product.img1:
        raise Http404     
    return HttpResponse(product.img1, content_type=product.content_type)

def get_img2(request, id):
    product = get_object_or_404(Product, id=id)  
    if not product.img2:
        raise Http404     
    return HttpResponse(product.img2, content_type=product.content_type)

def get_img3(request, id):
    product = get_object_or_404(Product, id=id)  
    if not product.img3:
        raise Http404     
    return HttpResponse(product.img3, content_type=product.content_type)
def get_share_img1(request,id):
    share = get_object_or_404(SharedProduct, id=id)  
    if not share.img:
        raise Http404     
    return HttpResponse(share.img, content_type=share.content_type)

@login_required
def get_profilephoto(request,id):
    curr_user = request.user
    userprofile = get_object_or_404(UserProfile, user = curr_user)  
    if not userprofile.image:
        raise Http404  
    content_type = guess_type(userprofile.image.name)   
    return HttpResponse(userprofile.image, content_type=content_type)
def get_title_json(request):
    response_text = serializers.serialize('json', Product.objects.all())
    return HttpResponse(response_text, content_type='application/json')

def display_by_search(request):
    context={}
    title=request.POST.get('search','')
    if not request.user.is_anonymous():
        curr_bag = get_object_or_404(Bag, owner = request.user)
        amountData= Amount.objects.filter(bag = curr_bag)
        context['amountData']=amountData

    if title=='':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(title=title)
    context['products']=products
    return render(request,'searchshow.html',context)

@login_required
def add_to_bag(request, id):
    if request.method == "POST":
        form = ItemAmountForm(request.POST)
        if form.is_valid():
            product_to_add = get_object_or_404(Product, id=id)
            curr_bag = get_object_or_404(Bag, owner = request.user)
            if product_to_add in curr_bag.itemsInBag.all():
                thisAmount = Amount.objects.get(product= product_to_add, bag = curr_bag)
                thisAmount.amount = thisAmount.amount + form.cleaned_data['amount']
                thisAmount.save()
            else:
                curr_bag.itemsInBag.add(product_to_add)
                quantity = Amount.objects.create(product = product_to_add, bag = curr_bag, amount = form.cleaned_data['amount'])
                quantity.save()
            curr_bag.save()
        else:
            form = ItemAmountForm()
    return redirect(reverse('item', kwargs={'id': id}))

def myformat(x):
    return ('%.2f' % x).rstrip('0').rstrip('.')

@login_required
@transaction.atomic
def see_bag(request):
    curr_bag = get_object_or_404(Bag, owner = request.user)
    items = curr_bag.itemsInBag.all()
    amountData = Amount.objects.all().filter(bag = curr_bag)
    empty = False
    if not items:
        empty = True
    totaltemp = 0
    for eaPrice in amountData:
        totaltemp += eaPrice.product.price * eaPrice.amount
    shipping=8
    tax=totaltemp*Decimal(0.075)
    taxr=myformat(tax)
    total=totaltemp+shipping+tax
    totalr=myformat(total)
    context={"user":request.user, "bag": curr_bag, "items": items, 'amountData': amountData, 
    'empty': empty, 'totaltemp': totaltemp,'total':totalr,'shipping':shipping,
    'tax':taxr}
    return render(request, 'shoppingbag.html', context)

@login_required
def update_bag(request, id):
    try:
        productTitle = request.POST['productTitle']
        curr_bag = get_object_or_404(Bag, owner = request.user)
        product_to_update = Product.objects.get(title = productTitle)
        amount_to_update = Amount.objects.get(product= product_to_update, bag = curr_bag)
        amount_to_update.amount = request.POST["newAmount"]
        amount_to_update.save()
        return HttpResponseRedirect(reverse('bag'))
    except:
        return HttpResponse("Update failed...")

@login_required
@transaction.atomic
def delete_item(request, id):
    curr_bag = get_object_or_404(Bag, owner = request.user)
    item_to_delete = get_object_or_404(Product, id = id)
    amountData = get_object_or_404(Amount, bag = curr_bag, product = item_to_delete)
    amountData.delete()
    curr_bag.itemsInBag.remove(item_to_delete)
    items = curr_bag.itemsInBag.all()
    amountData = Amount.objects.all().filter(bag = curr_bag)
    empty = False
    if not items:
        empty = True
    total = 0
    for eaPrice in amountData:
        total += eaPrice.product.price * eaPrice.amount
    context={"user":request.user, "bag": curr_bag, "items": items, 'amountData': amountData, 'empty': empty, 'total': total}
    return render(request, 'shoppingbag.html', context)

@login_required
def profile_wishlist(request):
    curr_profile = get_object_or_404(UserProfile, user=request.user)
    if not curr_profile:
        raise Http404
    items = curr_profile.wishList.all()
    empty = False
    if not items:
        empty = True
    context={"user":request.user, "items": items, "empty": empty}
    return render(request, 'profile_wishlist.html', context)

@login_required
def profile_share(request):
    context={}
    context['user'] = request.user
    curr_bag = get_object_or_404(Bag, owner = request.user)
    context['amountData'] = Amount.objects.filter(bag = curr_bag)
    context['user'] = request.user
    context['userprofile'] = UserProfile.objects.get(user=request.user)
    context['sharedproducts']=SharedProduct.objects.filter(user=request.user)
    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['shareform'] = ShareForm()
        return render(request, 'profile_share.html', context)
    form = ShareForm(request.POST,request.FILES)
    if form.is_valid():
        newshare=SharedProduct(user=request.user,title=form.cleaned_data['title'],
                            text=form.cleaned_data['text'],img=form.cleaned_data['img'])
        newshare.save()
        return redirect(reverse('profile_share'))
    context['shareform']=form
    context['status']='error'
    return render(request, 'profile_share.html', context)

@login_required
def delete_share(request,id):
    share_delete=get_object_or_404(SharedProduct,id=id,user=request.user)
    share_delete.delete()
    return redirect(reverse('profile_share'))

@login_required
def profile_global(request):
    context={}
    context['user'] = request.user
    curr_bag = get_object_or_404(Bag, owner = request.user)
    context['amountData'] = Amount.objects.filter(bag = curr_bag)
    context['user'] = request.user
    context['userprofile'] = UserProfile.objects.get(user=request.user)
    context['allshare'] = SharedProduct.objects.all()
    return render(request,'profile_global.html',context)

@login_required
def add_to_wish(request, id):
    curr_profile = get_object_or_404(UserProfile, user=request.user)
    product_to_add = get_object_or_404(Product, id=id)
    if not curr_profile.wishList.filter(id=id):
        curr_profile.wishList.add(product_to_add)
        curr_profile.save()
    return redirect(reverse('item', kwargs={'id': id}))

@login_required
def see_wish(request):
    curr_profile = get_object_or_404(UserProfile, user=request.user)
    curr_bag = get_object_or_404(Bag, owner = request.user)
    amountData= Amount.objects.filter(bag = curr_bag)
    if not curr_profile:
        raise Http404
    my_wish = curr_profile.wishList.all()
    empty = False
    if not my_wish:
        empty = True
    context = {'wishes': my_wish, 'empty': empty, 'amountData': amountData}
    return render(request, 'wishlist.html', context)

@login_required
def remove_from_wishlist(request, id):
    curr_profile = get_object_or_404(UserProfile, user=request.user)
    product_to_remove = get_object_or_404(Product, id = id)
    if curr_profile.wishList.filter(id=id):
        curr_profile.wishList.remove(product_to_remove)
        curr_profile.save()
    return redirect(reverse('wishlist'))

@login_required
def change_to_bag(request, id):
    curr_profile = get_object_or_404(UserProfile, user=request.user)
    product_to_remove = get_object_or_404(Product, id = id)
    curr_bag = get_object_or_404(Bag, owner = request.user)
    if curr_profile.wishList.filter(id=id):
        if product_to_remove in curr_bag.itemsInBag.all():
            thisAmount = Amount.objects.get(product= product_to_remove, bag = curr_bag)
            thisAmount.amount = thisAmount.amount + 1
            thisAmount.save()
        else:
            curr_bag.itemsInBag.add(product_to_remove)
            quantity = Amount.objects.create(product = product_to_remove, bag = curr_bag, amount = 1)
            quantity.save()
        curr_profile.wishList.remove(product_to_remove)
        curr_profile.save()
        curr_bag.save()
    return redirect(reverse('wishlist'))
@login_required
def change_to_wish(request, id):
    curr_profile = get_object_or_404(UserProfile, user=request.user)
    product_to_add = get_object_or_404(Product, id=id)
    if not curr_profile.wishList.filter(id=id):
        curr_profile.wishList.add(product_to_add)
        curr_profile.save()
    curr_bag = get_object_or_404(Bag,owner=request.user)
    curr_bag.itemsInBag.remove(product_to_add)
    curr_bag.save()
    return redirect(reverse('bag'))

@login_required
def prev_orders(request):
    context={}
    userprofile=get_object_or_404(UserProfile,user=request.user)
    products=userprofile.order.all()
    comments=Comment.objects.all().order_by("-time")
    context['comments']=comments
    if request.method=='GET':
        commentform=CommentForm()
        context['commentform']=commentform
    curr_profile = get_object_or_404(UserProfile, user=request.user)
    if not curr_profile:
        raise Http404
    previous_orders = curr_profile.order.all()
    empty = False
    if not previous_orders:
        empty = True
    context['orders']=previous_orders
    context['empty']= empty
    return render(request, 'orders.html', context)
@login_required
def comment(request,id):
    context={}
    context['user']=request.user
    curr_profile = get_object_or_404(UserProfile, user=request.user)
    if not curr_profile:
        raise Http404
    previous_orders = curr_profile.order.all()
    context['orders']=previous_orders
    if request.method=='POST':
        commentform=CommentForm(request.POST)
        context['commentform']=commentform
        product=get_object_or_404(Product,id=id)
        if commentform.is_valid():
            newcomment=Comment(time=timezone.now(),
                                text=commentform.cleaned_data['text'],
                                user=request.user,
                                product=product)
            newcomment.save()
            context['commentform']=CommentForm()
            product=get_object_or_404(Product,id=id)
            comments=Comment.objects.filter(user=request.user).order_by("-time")
            context['comments']=comments
        return render(request,'orders.html',context)

def bag_to_orders(request):
    context={}
    curr_profile = get_object_or_404(UserProfile, user=request.user)
    curr_bag = get_object_or_404(Bag, owner = request.user)
    comments=Comment.objects.filter(user=request.user)
    context['comments']=comments
    for item in curr_bag.itemsInBag.all():
        curr_profile.order.add(item)
        amountData = get_object_or_404(Amount, bag = curr_bag, product = item)
        item.availability =  item.availability - amountData.amount
        item.save()
        amountData.delete()
    curr_bag.itemsInBag = []
    curr_profile.save()
    curr_bag.save()
    previous_orders = curr_profile.order.all()
    empty = False
    if not previous_orders:
        empty = True
    if request.method=='GET':
        commentform=CommentForm()
        context['commentform']=commentform
    context['orders']= previous_orders
    context['empty']= empty
    return render(request, 'orders.html', context)
