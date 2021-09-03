import os
import time
import re

class Renamer():
	def __init__(self):
		pass

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

	def validate_path(self, path:str, err:bool=False):
		msg = ''
		if not os.path.exists(path):
			msg = 'Path does not exist!'
		elif not (os.path.isdir(path) or os.path.isfile(path)):
			msg = 'Path is not a directory or a file!'
		if err and msg:
			raise Exception(msg)
		else:
			return msg

	def get_names(self, path:str, ext:bool=True):
		names = []
		if os.path.isdir(path):
			files = os.listdir(path)
			if ext:
				names = files
			else:
				for file in files:
					names.append(os.path.splitext(file)[0])
			names.sort()
		elif os.path.isfile(path):
			with open(path, 'r', encoding="utf-8") as f:
				for name in f.readlines():
					names.append(name.strip())
		return names

	def rename_ref(self, path_ren:str, path_ref:str):
		flist_ren = self.get_names(path_ren)
		len_ren = len(flist_ren)
		flist_ref = self.get_names(path_ref, False)
		len_ref = len(flist_ref)
		renlog = []
		for i in range(min(len_ren,len_ref)):
			ext = os.path.splitext(flist_ren[i])[1]
			os.rename(path_ren+'/'+flist_ren[i], path_ren+'/'+flist_ref[i]+ext)
			renlog.append((flist_ren[i], flist_ref[i]+ext))
		return renlog

	def rename(self, mode:str, args:dict={}, name:str=None, err:bool=False):
		name = re.sub(r'[\\/:*?"<>|\r\n]+', "_", name) if name else None
		if 'RenameRef' == mode:
			arg_list = [('PathRen', 'Path Rename: '), ('PathRef', 'Path Reference: ')]
			for (key, memo) in arg_list:
				if key not in args:
					args[key] = input(memo).replace('\\','/')
				msg = self.validate_path(args[key], err)
				if msg:
					return msg
			renlog = self.rename_ref(args['PathRen'], args['PathRef'])
			self.write_log('RenameRef', name, {'PathRen':args['PathRen'], 'PathRef':args['PathRef']}, renlog)
