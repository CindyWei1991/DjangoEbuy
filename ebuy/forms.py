from django import forms

from django.contrib.auth.models import User
from models import *
from choices import *
from django.core.validators import validate_email, RegexValidator


class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20,label = 'Username')
    password = forms.CharField(max_length = 200, label='Password', 
                                widget = forms.PasswordInput())
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 20)
    firstname = forms.CharField(max_length = 20,
                                label = 'First name')
    lastname = forms.CharField(max_length = 15,
                                label = 'Last name')
    age = forms.CharField(max_length='3')
    email = forms.CharField(max_length = 40,
                                 validators = [validate_email])
    password1 = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200, 
                                label='Confirm password',  
                                widget = forms.PasswordInput())


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        # At least 6 characters long
        if len(password1) < 6:
            raise forms.ValidationError("The password nust be at least 6 characters long.")
        first_isalpha = password1[0].isalpha()
        # At least one letter and one non-letter
        if all(c.isalpha() == first_isalpha for c in password1):
            raise forms.ValidationError("The new password must contain at least one letter and at least one digit or" \
                                        " punctuation character.")
        # Confirms that the two password fields match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return username
    def clean_age(self):
        age = self.cleaned_data.get('age')
        try:
            if int(age):
                return age
        except:
            raise forms.ValidationError('Please enter a number')

class ProfileForm(forms.ModelForm):
    class  Meta:
        model = UserProfile
        exclude = (
            'user', 'userName', 'wishList','order'
            )
        widgets = {'picture':forms.FileInput()}

class ProductForm(forms.ModelForm):
    category =forms.ChoiceField(choices =CATEGORIES, required=True)
    class Meta:
        model = Product
        exclude = (
            'content_type',
            )
        widgets = {'description':forms.Textarea}
            
# class ImageForm(forms.ModelForm):
#     image = forms.ImageField(label = "Image")
#     class Meta:
#         model = ProductImages
#         fields = ('images', )

class EditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = (
            'user',
            'content_type',
            'wishList',
            'order'
            )
    def clean_picture(self):
        image = self.cleaned_data['image']
        if not image:
            return None
        if not image.content_type or not image.content_type.endswith('pdf'):
            raise forms.ValidationError('File type is not image')
        if image.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture
    def clean_age(self):
        age = self.cleaned_data.get('age')
        try:
            if int(age):
                return age
        except:
            raise forms.ValidationError('Please enter a number')
            
class ItemAmountForm(forms.ModelForm):
    # the form to add the item to bag and specify the purchase amount
    # amount = forms.IntegerField(initial = 1)
    class Meta:
        model = Amount
        exclude = (
            'product',
            'bag',
            )
        widgets={'amount': forms.NumberInput(attrs={'min': 1, 'max': 20, 'step': 1, 'id': 'amountInput'})}
    def clean(self):
        cleaned_data = super(ItemAmountForm, self).clean()
        return cleaned_data

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        try:
            if int(amount):
                return amount
        except:
            raise forms.ValidationError('Please enter a number')
class ShareForm(forms.ModelForm):
    class Meta:
        model = SharedProduct
        exclude = (
            'user',
            'content_type'
            )
        widgets = {'text':forms.Textarea}
    def clean(self):
        cleaned_data = super(ShareForm, self).clean()
        return cleaned_data
    def clean_picture(self):
        print 'clean_picture:', 
        image = self.cleaned_data['img']
        print 'clean_picture:', image
        if not image:
            return None
        if not image.content_type or not image.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if image.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = (
            'user',
            'time',
            'product'
            )
    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        return cleaned_data

            