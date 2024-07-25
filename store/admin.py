from typing import Any
from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models




# To create our own cutom filter here is how to proceed
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    
    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]
        
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        
        



# admin.site.register(models.Product, ProductAdmin)
# the below line is equivalent to the above
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # Customizing forms
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    search_fields = ['title']
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    # To prevent extra queries for the collection title method we use the below
    list_select_related = ['collection']
    
    
    # if we want to access a partiular field of another table like title of the collection
    # we can define the below method to achieve that
    def collection_title(self, product):
        return product.collection.title
    
    # to implement sorting for this method we use the below decorator
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    
    # Creating custom actions here request represents the HTTP request and queryset 
    # represent the object the user has selected also to show a message to the user 
    # we can use the method self.message_user as below
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request, 
            f'{updated_count} products were successfully updated',
            messages.SUCCESS
            )
    

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']
    ordering = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # we use this method to tell django to give us the url of a page
        # reverse('admin:app_model_page') then to filter we gonna add a '?' 
        url = (reverse('admin:store_product_changelist') + '?collection_id=' + str(collection.id))
        return format_html('<a href="{}">{}<a>', url, collection.products_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))
    
    
    
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'order_count']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    
    # we can add lookup tags to specify the field queries as startswith, endswith etc
    # To be sure to not fall in the case sensitive query specify it by starting with 'i' which stands for case insensitive
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    
    @admin.display(ordering='order_count')
    def order_count(self, customer):
        url = reverse('admin:store_order_changelist') + '?customer_id=' + str(customer.id)
        return format_html('<a href="{}">{}<a>', url, customer.order_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(order_count=Count('order'))
    
    
class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    min_num = 1
    max_num = 10
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer_first_name']
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_per_page = 10
    list_select_related = ['customer']
    
    def customer_first_name(self, order):
        return order.customer.first_name

