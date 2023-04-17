from django.contrib import admin
from store.models import Product,Category,Customer,Orders

class AdminProduct(admin.ModelAdmin):
    list_display = ['name','price','category']

admin.site.register(Product,AdminProduct)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Orders)