from undostore.shop.models import CartItem, Product

from djangoundo import undo

import random
import string

CART_ID_SESSION_KEY = 'cart_id'

def get_cart_id(request):
    if not request.session.get(CART_ID_SESSION_KEY, None):
        characters = unicode(string.letters + string.digits)
        cart_id = u''.join(random.sample(characters, 50))
        request.session[CART_ID_SESSION_KEY] = cart_id
    return request.session.get(CART_ID_SESSION_KEY)

def get_cart_items(request):
    return CartItem.objects.filter(cart_id=get_cart_id(request)).select_related('product')
    

def get_cart_total(request):
    return sum([ci.total for ci in get_cart_items(request)])

def add_to_cart(request):
    """ adds product to the shopping cart; expects request to contain POST data,
    which should contain product_id
    
    """
    postdata = request.POST.copy()
    product_id = int(postdata.get('product_id', 0))
    if product_id:
        cart_id = get_cart_id(request)
        product = Product.objects.get(id=product_id)
        cart_items = get_cart_items(request)
        try:
            cart_item = CartItem.objects.get(product=product, cart_id=cart_id)
            cart_item.quantity += 1
        except CartItem.DoesNotExist:
            cart_item = CartItem()
            cart_item.product = product
            cart_item.quantity = 1
            cart_item.cart_id = cart_id
        cart_item.save()
            
def remove_cart_item(request, cart_item_id):
    item_removed = False
    product_name = u''
    try:
        cart_id = get_cart_id(request)
        cart_item = CartItem.objects.get(id=cart_item_id, cart_id=cart_id)
        product_name = cart_item.product.name
        
        # stow the cart_item object
        undo.stow(request, cart_item)
        
        cart_item.delete()
        item_removed = True
    except:
        pass
    return item_removed, product_name

def restore_cart_item(request, cart_item_id):
    cart_item = undo.restore(request, cart_item_id)
    return cart_item
