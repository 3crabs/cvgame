import random
import sys

from PySide2 import QtCore, QtWidgets


# window
class MyWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.resize(300, 300)

        # create button
        self.button = QtWidgets.QPushButton("Click me!")
        # create label
        self.text = QtWidgets.QLabel("Hello World")
        # label in center
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        # label vbox
        self.layout = QtWidgets.QVBoxLayout()
        # add label in vbox
        self.layout.addWidget(self.text)
        # add button in vbox
        self.layout.addWidget(self.button)
        # all layout in window
        self.setLayout(self.layout)

        # add button handler
        self.button.clicked.connect(self.magic)

    def magic(self):
        self.text.setText(random.choice(self.hello))


if __name__ == "__main__":
    # create app
    app = QtWidgets.QApplication([])

    # create window
    widget = MyWidget()
    # run window
    widget.show()

    # exit
    sys.exit(app.exec_())
