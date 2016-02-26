import pytest
import vcs, cdms2
from PySide import QtGui, QtCore
import BaseWindow

class DummyClass():
   def __init__(self, name):
      self.name = name

@pytest.fixture
def window():

   base = BaseWindow.BaseWindowWidget()
   return base

def save(name):
   assert name == "test"


def testSave(qtbot, window):
   base = window
   base.object = DummyClass("test")

   base.save()



