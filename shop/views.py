from django.shortcuts import render_to_response, get_object_or_404
from django.core import urlresolvers
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson

from undostore.shop.models import Product
from undostore.shop import cart


def home(request, template_name="shop/home.html"):
    products = Product.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def show_product(request, product_id, template_name="shop/product.html"):
    product = get_object_or_404(Product, id=product_id)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def show_cart(request, template_name="shop/cart.html"):
    cart_items = cart.get_cart_items(request)
    cart_total = cart.get_cart_total(request)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def add_to_cart(request):
    if request.method == 'POST':
        cart.add_to_cart(request)
        cart_url = urlresolvers.reverse('cart')
        return HttpResponseRedirect(cart_url)
    cart_url = urlresolvers.reverse('cart')
    return HttpResponseRedirect(cart_url)


def remove_cart_item(request):
    item_removed = False
    if request.method == 'POST':
        postdata = request.POST.copy()
        cart_item_id = postdata.get('cart_item_id', '')
        if cart_item_id:
            item_removed = cart.remove_cart_item(request, cart_item_id)
    if request.is_ajax():
        data = { 'item_removed': item_removed,
                 'cart_tfoot': render_cart_tfoot(request) }
        json = simplejson.dumps(data)
        return HttpResponse(json, content_type="application/json")
    else:
        cart_url = urlresolvers.reverse('cart')
        return HttpResponseRedirect(cart_url)


def restore_removed_item(request):
    item_restored = False
    if request.is_ajax() and request.method == 'POST':
        
        data = {}
        json = simplejson.dumps(data)
        return HttpResponse(json, content_type="application/json")
    # if we get a request to this that isn't an Ajax POST, just redirect to cart page
    cart_url = urlresolvers.reverse('cart')
    return HttpResponseRedirect(cart_url)

def render_cart_tfoot(request, template_name="shop/cart_footer.html"):
    cart_total = cart.get_cart_total(request)
    return render_to_string(template_name, locals())

