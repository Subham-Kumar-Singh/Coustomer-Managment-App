from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *


#  I Named it OrderForm because i have imported Order from model just added a Form into it 

class OrderForm(ModelForm):
	class Meta:
		# done this because i wanted to add the fields that are in Order class
		model=Order
		# '__all__' means that go and create a form that contains all the fields of order class model
		# and if we want some of the fields from class order then we would have used list ["customer","product"]
		fields='__all__'

	
class CreateUserForm(UserCreationForm):
	class Meta:
		model=User
		fields=['username','email','password1','password2',]

class CustomerForm(ModelForm):
	class Meta:
		model=Customer
		fields='__all__'
		exclude=['user']