from django.test import TestCase
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.contrib.sessions.backends.db import SessionStore

from djangoundo import undo

class CrashTestDummy(object):
    def __init__(self, id, name, job_description):
        self.id = id
        self.pk = id
        self.name = name
        self.job_description = job_description

class DjangoUndoTestCase(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.request.session = SessionStore()
        self.test_object = CrashTestDummy(1, "Bob", "Sit still")
        
    
    def test_undo_stow_and_retrieve(self):
        undo.stow(self.request, self.test_object)
        self.failUnless(undo.DJANGO_UNDO_SESSION_KEY in self.request.session)
        self.failUnless(self.request.session[undo.DJANGO_UNDO_SESSION_KEY][str(self.test_object.id)])
        # check that session now contains object
        
        
        object = undo.restore(self.request, self.test_object.id)
        self.failUnlessEqual(object, self.test_object)
        
    