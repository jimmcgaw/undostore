import pickle

try:
    from django.conf.settings import DJANGO_UNDO_SESSION_KEY
except ImportError:
    DJANGO_UNDO_SESSION_KEY = 'undo'
    

def stow(request, object, db_commit=True):
    if DJANGO_UNDO_SESSION_KEY not in request.session:
        request.session[DJANGO_UNDO_SESSION_KEY] = {}
    pickled_object = pickle.dumps(object)
    
    undo_dict = request.session[DJANGO_UNDO_SESSION_KEY]
    object_id = str(object.id)
    undo_dict.setdefault(object_id, pickled_object)
    request.session[DJANGO_UNDO_SESSION_KEY] = undo_dict
    

def restore(request, object_id):
    undo_dict = request.session[DJANGO_UNDO_SESSION_KEY]
    pickled_object = undo_dict[object_id]
    object = pickle.loads(pickled_object)
    object.save()
    if object.pk != None:
        del undo_dict[object_id]
        request.session[DJANGO_UNDO_SESSION_KEY] = undo_dict
    return object
        