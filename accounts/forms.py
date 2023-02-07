from django.forms import ModelForm
from .models import Order

# we have imported this for the date filtering
from django_filters import DateFilter

#  I Named it OrderForm because i have imported Order from model just added a Form into it 

class OrderForm(ModelForm):
	class Meta:
		# done this because i wanted to add the fields that are in Order class
		model=Order
		# '__all__' means that go and create a form that contains all the fields of order class model
		# and if we want some of the fields from class order then we would have used list ["customer","product"]
		fields='__all__'

		exclude=['customer','date_created']