import os

from PySide6.QtWidgets import QMainWindow, QFrame, QTabWidget, QMessageBox, QLineEdit, QPushButton, QLabel, QFileDialog
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout

from Renamer import Renamer

class QtRenamer(QMainWindow):
	def __init__(self):
		super().__init__()
		self.renamer = Renamer()
		self.initUI()

	def initUI(self):
		self.setWindowTitle('PyRenamer')
		self.setMinimumWidth(500)
		self.qtab = QTabWidget()
		self.setCentralWidget(self.qtab)

		self.qtab_ref = QFrame()
		self.qtab.addTab(self.qtab_ref, 'RefRename')

		qtab_ref_lyt = QVBoxLayout()
		self.qtab_ref.setLayout(qtab_ref_lyt)
		self.qtab_ref_pren = QtPathPicker('Path Ren:')
		qtab_ref_lyt.addWidget(self.qtab_ref_pren)
		self.qtab_ref_pref = QtPathPicker('Path Ref:')
		qtab_ref_lyt.addWidget(self.qtab_ref_pref)
		self.qtab_ref_btn = QPushButton('Start')
		qtab_ref_lyt.addWidget(self.qtab_ref_btn)
		self.qtab_ref_btn.clicked.connect(self.renameRef)

	def renameRef(self):
		if self.qtab_ref_pren.path and self.qtab_ref_pref.path:
			self.renamer.rename_ref(self.qtab_ref_pren.path, self.qtab_ref_pref.path)
		else:
			QMessageBox.warning(self, 'Warning', 'Enter the valid path!')

class QtPathPicker(QFrame):
	def __init__(self, label:str):
		super().__init__()
		self.path = ''
		self.initUI(label)

	def initUI(self, label:str):
		qlyt = QHBoxLayout()
		self.setLayout(qlyt)
		self.qlabel = QLabel(label)
		qlyt.addWidget(self.qlabel)
		self.qpath = QLineEdit()
		qlyt.addWidget(self.qpath)
		self.qbtn = QPushButton('Select')
		qlyt.addWidget(self.qbtn)
		self.qbtn.clicked.connect(self.selectPath)
		self.qpath.textChanged.connect(self.updatePath)

	def selectPath(self):
		path = QFileDialog.getExistingDirectory(self, 'Select the Path', self.path, QFileDialog.ShowDirsOnly)
		if len(path):
			self.qpath.setText(path)
	
	def updatePath(self, path:str):
		if len(path) and os.path.isdir(path) and os.path.exists(path):
			self.path = path
			self.qpath.setStyleSheet('')
		else:
			self.path = ''
			self.qpath.setStyleSheet('QLineEdit{border: 1px solid red;}')
