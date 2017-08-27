# pyuic5 dialog.ui > view.py
import sys

from PyQt5.QtWidgets import QDialog, QApplication
import view

class MainWindow(QDialog, view.Ui_Dialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


class Client():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.view = MainWindow()
        self.view.pushButton.setText("hahaha")
        self.view.pushButton.clicked.connect(self.click)

    def click(self):
        print("hhhhh")

    def run(self):
        self.view.show()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    client = Client()
    client.run()
