import os
import time
import re

class Renamer():
	def __init__(self):
		pass

	def get_files_in_path(self, path:str):
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

	def validate_path(self, path:str, type:str='dir', err:bool=False):
		msg = ''
		if not os.path.exists(path):
			msg = 'Path does not exist!'
		elif 'dir' == type and not os.path.isdir(path):
			msg = 'Path is not a directory!'
		elif 'file' == type and not os.path.isfile(path):
			msg = 'Path is not a file!'
		if err and msg:
			raise Exception(msg)
		else:
			return msg

	def rename_ref(self, path_ren:str=None, path_ref:str=None):
		flist_ren = self.get_files_in_path(path_ren)
		len_ren = len(flist_ren)
		flist_ref = self.get_files_in_path(path_ref)
		len_ref = len(flist_ref)
		renlog = []
		for i in range(min(len_ren,len_ref)):
			ext = os.path.splitext(flist_ren[i])[1]
			base = os.path.splitext(flist_ref[i])[0]
			os.rename(path_ren+'/'+flist_ren[i], path_ren+'/'+base+ext)
			renlog.append((flist_ren[i], base+ext))
		return renlog

	def rename(self, mode:str, args:dict=None, name:str=None, err:bool=False):
		name = re.sub(r'[\\/:*?"<>|\r\n]+', "_", name) if name else None
		if 'RenameRef' == mode :
			arglist = [('PathRen','dir',"Path Rename: "), ('PathRef','dir',"Path Ref: ")]
			for (key, type, memo) in arglist:
				if key not in args:
					args[key] = input(memo)
				msg = self.validate_path(args[key], type, err)
				if msg:
					return msg
			renlog = self.rename_ref(args['PathRen'], args['PathRef'])
			self.write_log('RenameRef', name, {'PathRen':args['PathRen'], 'PathRef':args['PathRef']}, renlog)
