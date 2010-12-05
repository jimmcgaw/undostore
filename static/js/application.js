var UndoStore = {};

UndoStore.removeCartItem = function(e){
	// stop the form from submitting, handle with Ajax
	e.preventDefault();
	var form = jQuery(e.target);
	var cart_row = form.parents('tr');
	var cart_tfoot = jQuery("table#shopping_cart tfoot");
	
	jQuery.ajax({
		url: form.attr('action'),
		type: form.attr('method'),
		data: form.serialize(),
		dataType: 'json',
		success: function(json){
			if (json){
				if (json.item_removed){
					cart_row.remove();
				}
				if (json.cart_tfoot){
					cart_tfoot.html(json.cart_tfoot);
				}
			}
		},
		error: function(){ }
	});
};

UndoStore.prepareDocument = function(){
	jQuery('table#shopping_cart form.remove_item').submit(function(e){
		UndoStore.removeCartItem(e);
	});
};

jQuery(document).ready(UndoStore.prepareDocument);