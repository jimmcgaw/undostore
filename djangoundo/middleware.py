from djangoundo.undo import DJANGO_UNDO_SESSION_KEY

class UndoResetMiddleware(object):
    """ 'Undo' Ajax operations exists on some pages; we should clear out this value in the session
    after the user has clicked through to a fresh new page.
    
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.is_ajax():
            request.session[DJANGO_UNDO_SESSION_KEY] = {}