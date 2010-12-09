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
				if (json.item_removed && json.undo_row_html){
					cart_row.after(json.undo_row_html)
						.next()
						.attr('class', cart_row.attr('class'))
						.prev()
						.remove();
				}
				if (json.cart_tfoot){
					cart_tfoot.html(json.cart_tfoot);
				}
			}
		},
		error: function(){ }
	});
};

UndoStore.undoRemoveItem = function(e){
	e.preventDefault();
	
	var form = jQuery(e.target);
	var undo_row = form.parents('tr');
	var cart_tfoot = jQuery("table#shopping_cart tfoot");
	
	jQuery.ajax({
		url: form.attr('action'),
		type: form.attr('method'),
		data: form.serialize(),
		dataType: 'json',
		success: function(json){
			if (json){
				if (json.item_restored && json.cart_row_html){
					undo_row.after(json.cart_row_html)
						.next()
						.attr('class', undo_row.attr('class'))
						.prev()
						.remove();
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
	jQuery('table#shopping_cart form.remove_item').live('submit', function(e){
		UndoStore.removeCartItem(e);
	});
	
	jQuery('table#shopping_cart form.undo_remove').live('submit', function(e){
		UndoStore.undoRemoveItem(e);
	});
};

jQuery(document).ready(UndoStore.prepareDocument);