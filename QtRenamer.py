import os

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QMainWindow, QFrame, QRadioButton, QTabWidget, QMessageBox, QLineEdit, QPushButton, QLabel, QFileDialog, QGroupBox
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout

from Renamer import Renamer

class QtRenamer(QMainWindow):
	def __init__(self):
		super().__init__()
		self.renamer = Renamer()
		self.initUI()

	def initUI(self):
		self.setWindowTitle('PyRenamer')
		self.setMinimumWidth(600)
		self.qtab = QTabWidget()
		self.setCentralWidget(self.qtab)

		self.qtab_ref = QFrame()
		self.qtab.addTab(self.qtab_ref, 'RefRename')
		qtab_ref_lyt = QVBoxLayout()
		self.qtab_ref.setLayout(qtab_ref_lyt)
		qtab_ref_lyt2 = QHBoxLayout()

		qtab_ref_conf = QGroupBox('Config')
		qtab_ref_conf.setLayout(QVBoxLayout())
		qtab_ref_conf_dir = QRadioButton('Dir')
		qtab_ref_conf.layout().addWidget(qtab_ref_conf_dir)
		qtab_ref_conf_file = QRadioButton('File')
		qtab_ref_conf.layout().addWidget(qtab_ref_conf_file)
		qtab_ref_lyt2.addWidget(qtab_ref_conf)

		qtab_ref_path = QGroupBox('Path')
		qtab_ref_path.setLayout(QVBoxLayout())
		self.qtab_ref_pren = QtPathPicker('Path Ren:')
		qtab_ref_path.layout().addWidget(self.qtab_ref_pren)
		self.qtab_ref_pref = QtPathPicker('Path Ref:')
		qtab_ref_path.layout().addWidget(self.qtab_ref_pref)
		qtab_ref_lyt2.addWidget(qtab_ref_path)

		qtab_ref_lyt.addLayout(qtab_ref_lyt2)
		self.qtab_ref_btn = QPushButton('Start')
		qtab_ref_lyt.addWidget(self.qtab_ref_btn)

		# connect signals to slots
		self.qtab_ref_btn.clicked.connect(self.renameRef)
		qtab_ref_conf_dir.toggled.connect(self.setPathRefAllow)
		qtab_ref_conf_file.toggled.connect(self.setPathRefAllow)
		self.qtab_ref_pref.qpath.textChanged.connect(self.resetBtn)
		self.qtab_ref_pren.qpath.textChanged.connect(self.resetBtn)

		# set default UI state
		qtab_ref_conf_dir.setChecked(True)

	@Slot()
	def renameRef(self):
		if self.qtab_ref_pren.path and self.qtab_ref_pref.path:
			self.qtab_ref_btn.setText('Renaming...')
			self.renamer.rename('RenameRef', {'PathRen':self.qtab_ref_pren.path, 'PathRef':self.qtab_ref_pref.path})
			self.qtab_ref_btn.setText('Done.')
		else:
			QMessageBox.warning(self, 'Warning', 'Enter the valid path!')

	@Slot()
	def setPathRefAllow(self):
		allow = self.sender().text().lower()
		self.qtab_ref_pref.setAllow(allow)

	@Slot()
	def resetBtn(self):
		self.qtab_ref_btn.setText('Start')

class QtPathPicker(QFrame):
	def __init__(self, label:str, allow:str='dir'):
		super().__init__()
		self.path = ''
		self.allow = ''
		self.initUI(label)
		self.setAllow(allow)

	def initUI(self, label:str):
		qlyt = QHBoxLayout()
		self.setLayout(qlyt)
		self.qlabel = QLabel(label)
		qlyt.addWidget(self.qlabel)
		self.qpath = QLineEdit()
		qlyt.addWidget(self.qpath)
		self.qbtn = QPushButton()
		qlyt.addWidget(self.qbtn)
		self.qbtn.clicked.connect(self.selectPath)
		self.qpath.textChanged.connect(self.updatePath)

	def setAllow(self, allow:str):
		if allow in ['dir', 'file']:
			self.allow = allow
			self.qbtn.setText('Select '+allow.capitalize())
		else:
			QMessageBox.warning(self, "The path should be a directory('dir') or a file('file')")

	@Slot()
	def selectPath(self):
		if 'dir' == self.allow:
			path = QFileDialog.getExistingDirectory(self, 'Select a directory', self.path, QFileDialog.ShowDirsOnly)
			self.qpath.setText(path)
		else:
			path = QFileDialog.getOpenFileName(self, 'Select a file', self.path)
			self.qpath.setText(path[0])

	@Slot(str)
	def updatePath(self, path:str):
		if len(path) and os.path.exists(path) and (('dir' == self.allow and os.path.isdir(path)) or ('file' == self.allow and os.path.isfile(path))):
			self.path = path
			self.qpath.setStyleSheet('')
		else:
			self.path = ''
			self.qpath.setStyleSheet('QLineEdit{border: 1px solid red;}')
