import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem, QCheckBox, QLineEdit, QComboBox
import view1

class MainWindow(QMainWindow, view1.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


class Client():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.view1 = MainWindow()

    def run(self):
        self.view1.show()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    clinet = Client()
    clinet.run()