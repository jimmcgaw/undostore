from django.conf.urls.defaults import *

urlpatterns = patterns('undostore.shop.views',
    (r'^$', 'home', {'template_name': 'shop/home.html' }, 'home'),
    (r'^product/(?P<product_id>\d+)$', 'show_product', {'template_name': 'shop/product.html' }, 'product'),
    (r'^cart/$', 'show_cart', {'template_name': 'shop/cart.html' }, 'cart'),
    (r'^add/to/cart/$', 'add_to_cart', {}, 'add_to_cart' ),
    (r'^remove/cart/item/$', 'remove_cart_item', {}, 'remove_cart_item' ),
    (r'^restore/removed/item/$', 'restore_removed_item', {}, 'restore_removed_item' ),
)
