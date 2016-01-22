import sys

from PySide.QtCore import *
from PySide.QtGui import *

def on_item_changed(item):
    if not item.checkState():
        return

    i = 0

    while model.item(i):
        if not model.item(i).checkState():
            return
        i+=1

    app.quit()

app = QApplication(sys.argv)

list = QListView()
list.setWindowTitle('Example List')
list.setMinimumSize(600,400)

model = QStandardItemModel(list)

item = QStandardItem()

foods = [
    'Cookie dough', # Must be store-bought
    'Hummus', # Must be homemade
    'Spaghetti', # Must be saucy
    'Dal makhani', # Must be spicy
    'Chocolate whipped cream' # Must be plentiful
]

for food in foods:

    item = QStandardItem(food)
    item.setCheckable(True)
    model.appendRow(item)

model.itemChanged.connect(on_item_changed)

list.setModel(model)
list.show()
app.exec_()
