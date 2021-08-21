import os
import time
import re

class Renamer():
	def __init__(self):
		pass

	def get_files_in_path(self, path):
		flist = os.listdir(path)
		flist.sort()
		return flist

	def write_log(self, mode:str, name:str, args:dict, renlog:list):
		if not os.path.exists('logs'):
			os.mkdir('logs')
		if not name:
			name = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
		with open('logs/'+name+'.log', 'w', encoding='utf-8') as f:
			f.write('Mode='+mode+'\n')
			for key, val in args.items():
				f.write(key+'='+val+'\n')
			for (old, new) in renlog:
				f.write(old+'\t'+new+'\n')

	def rename_ref(self, path_ren:str=None, path_ref:str=None, name:str=None):
		path_ren = path_ren if path_ren else input("Path Rename: ")
		flist_ren = self.get_files_in_path(path_ren)
		len_ren = len(flist_ren)
		path_ref = path_ref if path_ref else input("Path Ref: ")
		flist_ref = self.get_files_in_path(path_ref)
		len_ref = len(flist_ref)
		name = re.sub(r'[\\/:*?"<>|\r\n]+', "_", name) if name else None
		renlog = []
		for i in range(min(len_ren,len_ref)):
			ext = os.path.splitext(flist_ren[i])[1]
			base = os.path.splitext(flist_ref[i])[0]
			os.rename(path_ren+'/'+flist_ren[i], path_ren+'/'+base+ext)
			renlog.append((flist_ren[i], base+ext))
		self.write_log('RenameRef', name, {'PathRen':path_ren, 'PathRef':path_ref}, renlog)
