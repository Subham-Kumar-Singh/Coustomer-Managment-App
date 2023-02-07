from django.db import models

# Create your models here.

class Customer(models.Model):
	# in all these we have marked null=True it is because we want that the entry can be left enpty as well
	name=models.CharField(max_length=200,null=True)
	phone=models.CharField(max_length=200,null=True)
	email=models.CharField(max_length=200,null=True)
	# this date_created automatically take the time from the system
	date_created=models.DateTimeField(auto_now_add=True,null=True)

	# i have used this funtion just to show the name of the user that i have used insed of the number.
	def __str__(self):
		return self.name


# This tag class will have the tags like kitchen, outdoor or sports	
class Tag(models.Model):
	# in all these we have marked null=True it is because we want that the entry can be left enpty as well
	name=models.CharField(max_length=200,null=True)

	def __str__(self):
		return self.name


class Product(models.Model):
	CATEGORY=(
			('Indoor','Indoor'),
			('Out Door','Out Door'),
		)

# 	series=models.CharField(max_length=200)
	name=models.CharField(max_length=200,null=True)
	price=models.FloatField(null=True)
	category=models.CharField(max_length=200,null=True,choices=CATEGORY)
	description=models.CharField(max_length=200,blank=True)
	date_created=models.DateTimeField(auto_now_add=True,null=True)


	# we used this because we wanted our products to have tags such as sports,Kitchen,Summer
	tag=models.ManyToManyField(Tag)

	def __str__(self):
		return self.name


class Order(models.Model):
	STATUS=(
			('Pending','Pending'),
			('Out For Delivery','Out For Delivery'),
			('Delivered','Delivered'),

		)

	# on_delete :- Anytime we remove this order customer the this order will remain in the database with the null value for the customer


	# After using Foreignkey order have a relation with Customer and product

	customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
	product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
	date_created=models.DateTimeField(auto_now_add=True,null=True)

	# WE HAVE MADE CHOICES IN STATUS SECTION BECAUSE WE WANT IT TO TAKE A CHOICE FROM THE STATUS WHENEVER WE MAKE SOME CHANGES TO IT.
	status=models.CharField(max_length=200,null=True,choices=STATUS)  

	def __str__(self):
		return self.product.name