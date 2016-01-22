import sys
from PySide.QtCore import Slot
from PySide.QtGui import *

# Every Qt application must have one and only one QApplication object;
# it receives the command line arguments passed to the script, as they
# can be used to customize the application's appearance and behavior
qt_app = QApplication(sys.argv)

class LayoutExample(QWidget):

    def __init__(self):

        super(LayoutExample, self).__init__()

        self.setWindowTitle('Dynamic Greeter')
        self.setMinimumWidth(400)

        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()

        self.salutations = ['Ahoy',
                            'Good day',
                            'Hello',
                            'Heyo',
                            'Hi',
                            'Salutations',
                            'Wassup',
                            'Yo']

        # Create and fill the combo box to choose the salutation
        self.salutation = QComboBox(self)
        self.salutation.addItems(self.salutations)
        # Add it to the form layout with a label
        self.form_layout.addRow('&Salutation:', self.salutation)

        # Create the entry control to specify a
        # recipient and set its placeholder text
        self.recipient = QLineEdit(self)
        self.recipient.setPlaceholderText("e.g. 'world' or 'Matey'")

        # Add it to the form layout with a label
        self.form_layout.addRow('&Recipient:', self.recipient)

        # Create and add the label to show the greeting text
        self.greeting = QLabel('', self)
        self.form_layout.addRow('Greeting:', self.greeting)

        # Add the form layout to the main VBox layout
        self.layout.addLayout(self.form_layout)

        # Add stretch to separate the form layout from the button
        self.layout.addStretch(1)

        # Create a horizontal box layout to hold the button
        self.button_box = QHBoxLayout()

        # Add stretch to push the button to the far right
        self.button_box.addStretch(1)

        # Create the build button with its caption
        self.build_button = QPushButton('&Build Greeting', self)

        # Connect the button's clicked signal to show_greeting
        self.build_button.clicked.connect(self.show_greeting)

        # Add it to the button box
        self.button_box.addWidget(self.build_button)

        # Add the button box to the bottom of the main VBox layout
        self.layout.addLayout(self.button_box)

        # Set the VBox layout as the window's main layout
        self.setLayout(self.layout)

    @Slot()
    def show_greeting(self):
        self.greeting.setText('%s, %s!' %
        (self.salutations[self.salutation.currentIndex()],
        self.recipient.text()))

    def run(self):
        self.show()
        qt_app.exec_()

app = LayoutExample()
app.run()
