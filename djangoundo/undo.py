import pickle

try:
    from django.conf.settings import DJANGO_UNDO_SESSION_KEY
except ImportError:
    DJANGO_UNDO_SESSION_KEY = 'undo'
    

def stow(request, object):
    """
    takes a django.http.HttpRequest object and a Django model instance and stores the instance in the user's 
        request.session object. For use on a page where objects are being deleted via Ajax requests, and the user 
        interface offers an "undo" action.
    
    Objects are stored in session in a dictionary. The key used is the object's id property. The undo session 
        dictionary is not persisted between page requests, and the session is specific to each user,
        so the only way a collision of keys could occur would be on a page where the user can delete 
        more than one kind of model type.
    
    This does not modify the database; that is left up to the calling code. 
    
    """
    if DJANGO_UNDO_SESSION_KEY not in request.session:
        request.session[DJANGO_UNDO_SESSION_KEY] = {}
    pickled_object = pickle.dumps(object)
    
    undo_dict = request.session[DJANGO_UNDO_SESSION_KEY]
    object_id = str(object.id)
    undo_dict.setdefault(object_id, pickled_object)
    request.session[DJANGO_UNDO_SESSION_KEY] = undo_dict
    

def restore(request, object_id):
    if DJANGO_UNDO_SESSION_KEY not in request.session:
        request.session[DJANGO_UNDO_SESSION_KEY] = {}
    undo_dict = request.session[DJANGO_UNDO_SESSION_KEY]
    object_id = str(object_id)
    pickled_object = undo_dict[object_id]
    object = pickle.loads(pickled_object)
    object.save()
    if object.pk != None:
        del undo_dict[object_id]
        request.session[DJANGO_UNDO_SESSION_KEY] = undo_dict
    return object
        