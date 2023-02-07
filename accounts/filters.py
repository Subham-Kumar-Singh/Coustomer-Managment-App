import django_filters


# we have imported this for the date filtering
from django_filters import DateFilter,CharFilter

from .models import *

class OrderFilter(django_filters.FilterSet):
	# here gte means greater than or equals to and lte means leass than or equals to
	start_date=DateFilter(field_name='date_created',lookup_expr='gte')
	end_date=DateFilter(field_name='date_created',lookup_expr='lte')
	
	# here icontains means ignore the case-senstivity
	note=CharFilter(field_name='note',lookup_expr='icontains')
	class Meta:
		model=Order
		fields='__all__'
		exclude=['customer','date_created']