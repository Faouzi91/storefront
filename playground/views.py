from django.forms import DecimalField
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.db.models import Q, F, Prefetch, Value, Func, ExpressionWrapper
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.db.models.functions import Concat
from store.models import Product, OrderItem, Order, Customer
from tags.models import Tag, TaggedItem

def say_hello(request):
    # #filter multiple objects using the AN operator
    # queryset = Product.objects.filter(inventory__lt=10, inventory__gt=100)
    # queryset = Product.objects.filter(inventory__lt=10).filter(inventory__gt=100)
    
    # # filter multiple objects using the OR '|' operator we can also use for the AN '&' operator if needed
    # # to add the negation we use the '~' operator infront of the Q object like this '~Q(inventory__gt=100)'
    # queryset = Product.objects.filter(Q(inventory__lt=10) | Q(inventory__gt=100))
    
    # # To compare two objects we can use the F object
    # queryset = Product.objects.filter(inventory=F('collection__id'))
    
    
    # # Method is for limiting the results
    # product = Product.objects.all()[5:10]
    
    # # Selecting fields to query use the double underscore '__' to query related fields
    # # For this method instead of getting a bunch of product instances, we get a bunch of dictionary objects
    # product = Product.objects.values('id', 'title', 'collection__title')
    
    # # For this method we get a bunch of tuples
    # product = Product.objects.values_list('id', 'title', 'collection__title')
    
    
    # queryset = OrderItem.objects.values('product_id').order_by('product_id')
    
    # # use the distinc method to remove duplicates
    # # queryset = OrderItem.objects.values('product_id').distinct()
    
    # queryset = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    
    # # we have the 'only' method to return instances of the object while the values return dictionary values
    # queryset = Product.objects.only('id', 'title').order_by('title')
    
    # # we have another method called the defer which is the opposite of the 'only' method which defer the selected fields to later
    # queryset = Product.objects.defer('description')

    # # to select related objects to add another field to the query we use the select_related when we have one object with '__'
    # queryset = Product.objects.select_related('collection__someOtherField').all()
    
    #     # # We use the prefetch_related when we have multiple objects
    #     # queryset = Product.objects.prefetch_related('promotions').select_related('collection').all()
    # #     queryset = Order.objects.select_related('customer').prefetch_related(
    # #     Prefetch('orderitem_set', queryset=OrderItem.objects.select_related('product'))
    # # ).order_by('-placed_at')[:5]
        
    #     queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]


    # # # Sometimes we wana compute summaries like max or average price of our products this is where we use cthe aggregate method
    # # # To rename the name of the field simply give the name of the field followed by an equal sign
    # # result = Product.objects.aggregate(max_price=Max('unit_price'), average_price=Avg('unit_price'))
    
    # queryset = Customer.objects.annotate(new_id=F('id')+ 1)
    
    # # Calling database functions
    
    # # Using the Func class
    # queryset = Customer.objects.annotate(
    #     full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
    # )
    
    # # Using the Concat function
    # queryset = Customer.objects.annotate(
    #     full_name=Concat('first_name', Value(' '), 'last_name')
    # )
    
    
    # # Working with expression wrappers, we use this when building complex expressions
    # discounted_price = ExpressionWrapper(
    #     F('unit_price') * 0.8, output_field=DecimalField())
    # queryset = Product.objects.annotate(
    #     discounted_price = discounted_price
    # )
    
    # # Custom managers check the tag models to see the implementation
    # content_type = TaggedItem.objects.get_tags_for(Product, 1)
    

    # # Executing raw sql queries. only use this method when dealing with complex queries
    # queryset = Product.objects.raw('SELECT * FROM store_product')
    
    
    # # we can also use the connection method to query data from out database
    # cursor = connection.cursor()
    # cursor.execute('SELECT * FROM store_product')
    # queryset = cursor.close()
    
    
    # another way is to use the with method. this way we dont have to close the cursor
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM store_product')
        
        
        
    return render(request, 'hello.html', {'name': 'Garbatov', 'result': list(queryset)})
