from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=50)
    asin = models.CharField(max_length=15)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    publisher = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @models.permalink
    def get_absolute_url(self):
        return ('product', (), { 'product_id': self.id })
    
    def __unicode__(self):
        return u"Product: %s" % self.name


class CartItem(models.Model):
    cart_id = models.CharField(max_length=50, db_index=True)
    product = models.ForeignKey('shop.Product', unique=False)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def total(self):
        return self.quantity * self.product.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def __unicode__(self):
        return u"Cart Item: %s" % self.name
    
