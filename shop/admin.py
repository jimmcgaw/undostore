from django.contrib import admin
from undostore.shop.models import Product

class ProductAdmin(admin.ModelAdmin):
    # sets values for how the admin site lists your products
    list_display = ('name', 'price', 'created_at', 'updated_at',)
    # which of the fields in 'list_display' tuple link to admin product page
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['-created_at']

# registers your product model with the admin site
admin.site.register(Product, ProductAdmin)
