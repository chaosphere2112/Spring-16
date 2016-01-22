# Written by Robin Burchell
# No licence specified or required, but please give credit where it's due, and please let me know if this helped you.
# Feel free to contact with corrections or suggestions.
#
# We're using PySide, Nokia's official LGPL bindings.
# You can however easily use PyQt (Riverside Computing's GPL bindings) by commenting these and fixing the appropriate imports.
from PySide.QtCore import *
from PySide.QtGui import *
#from PyQt4 import *
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
import sys

# This is our model. It will maintain, modify, and present data to our view(s).
# As this is read-only, it's pretty straightforward, but it can get pretty complex.
# This is something that Qt Development Frameworks/Nokia are aware of and working on, in terms of
# better documentation, as well as a better implementation of all this, but both of those aren't
# really within the scope of this tutorial. ;)
#
# For more information on list models, take a look at:
# http://doc.trolltech.com/4.6/qabstractitemmodel.html
# but do bear in mind there are other models (like tables) available, depending on your data needs.
# Again, beyond the scope of this tutorial for now. :)
class SimpleListModel(QAbstractListModel):
 def __init__(self, mlist):
  QAbstractListModel.__init__(self)

  # Cache the passed data list as a class member.
  self._items = mlist

 # We need to tell the view how many rows we have present in our data.
 # For us, at least, it's fairly straightforward, as we have a python list of data,
 # so we can just return the length of that list.
 def rowCount(self, parent = QModelIndex()):
  return len(self._items)

 # Here, it's a little more complex.
 # data() is where the view asks us for all sorts of information about our data:
 # this can be purely informational (the data itself), as well as all sorts of 'extras'
 # such as how the data should be presented.
 #
 # For the sake of keeping it simple, I'm only going to show you the data, and one presentational
 # aspect.
 #
 # For more information on what kind of data the views can ask for, take a look at:
 # http://doc.trolltech.com/4.6/qabstractitemmodel.html#data
 #
 # Oh, and just  to clarify: when it says 'invalid QVariant', it means a null QVariant.
 # i.e. QVariant().
 #
 # 'index' is of type QModelIndex, which actually has a whole host of stuff, but we
 # only really care about the row number for the sake of this tutorial.
 # For more information, see:
 # http://doc.trolltech.com/4.6/qmodelindex.html
 def data(self, index, role = Qt.DisplayRole):
  if role == Qt.DisplayRole:
   # The view is asking for the actual data, so, just return the item it's asking for.
   return self._items[index.row()]
  elif role == Qt.BackgroundRole:
   # Here, it's asking for some background decoration.
   # Let's mix it up a bit: mod the row number to get even or odd, and return different
   # colours depending.
   # (you can, and should, more easily do this using this:
   # http://doc.trolltech.com/4.6/qabstractitemview.html#alternatingRowColors-prop
   # but I deliberately chose to show that you can put your own logic/processing here.)
   #
   # Exercise for the reader: make it print different colours for each row.
   # Implementation is up to you.
   if index.row() % 2 == 0:
    return QColor(Qt.gray)
   else:
    return QColor(Qt.lightGray)
  else:
   # We don't care about anything else, so make sure to return an empty QVariant.
   return None

# This widget is our view of the readonly list.
# Obviously, in a real application, this will be more complex, with signals/etc usage, but
# for the scope of this tutorial, let's keep it simple, as always.
#
# For more information, see:
# http://doc.trolltech.com/4.6/qlistview.html
class SimpleListView(QListView):
 def __init__(self, parent = None):
  QListView.__init__(self, parent)

# Our main application window.
# You should be used to this from previous tutorials.
class MyMainWindow(QWidget):
 def __init__(self):
  QWidget.__init__(self, None)

  # main section of the window
  vbox = QVBoxLayout()

  # create a data source:
  m = SimpleListModel(["test", "tes1t", "t3est", "t5est", "t3est"])

  # let's add two views of the same data source we just created:
  v = SimpleListView()
  v.setModel(m)
  vbox.addWidget(v)

  # second view..
  v = SimpleListView()
  v.setModel(m)
  vbox.addWidget(v)

  # bottom section of the window
  hbox = QHBoxLayout()

  # add bottom to main window layout
  vbox.addLayout(hbox)

  # set layout on the window
  self.setLayout(vbox)

# set things up, and run it. :)
if __name__ == '__main__':
 app = QApplication(sys.argv)
 w = MyMainWindow()
 w.show()
 app.exec_()
 sys.exit()
