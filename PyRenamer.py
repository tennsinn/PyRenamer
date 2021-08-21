import sys
from PySide6.QtWidgets import QApplication
from QtRenamer import QtRenamer

if __name__ == '__main__':
	app = QApplication(sys.argv)
	main = QtRenamer()
	main.show()
	sys.exit(app.exec())
