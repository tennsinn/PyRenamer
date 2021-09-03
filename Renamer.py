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

	def get_names(self, path:str):
		if os.path.isdir(path):
			names = os.listdir(path)
			names.sort()
		elif os.path.isfile(path):
			names = []
			with open(path, 'r', encoding="utf-8") as f:
				for name in f.readlines():
					names.append(name.strip())
		return names

	def rename_ref(self, path_ren:str, path_ref:str):
		flist_ren = self.get_names(path_ren)
		len_ren = len(flist_ren)
		flist_ref = self.get_names(path_ref)
		len_ref = len(flist_ref)
		renlog = []
		for i in range(min(len_ren,len_ref)):
			ext = os.path.splitext(flist_ren[i])[1]
			base = os.path.splitext(flist_ref[i])[0]
			os.rename(path_ren+'/'+flist_ren[i], path_ren+'/'+base+ext)
			renlog.append((flist_ren[i], base+ext))
		return renlog

	def rename_list(self, path_ren:str, path_list:str):
		flist_ren = self.get_names(path_ren)
		len_ren = len(flist_ren)
		flist_list = self.get_names(path_list)
		len_list = len(flist_list)
		renlog = []
		for i in range(min(len_ren,len_list)):
			ext = os.path.splitext(flist_ren[i])[1]
			os.rename(path_ren+'/'+flist_ren[i], path_ren+'/'+flist_list[i]+ext)
			renlog.append((flist_ren[i], flist_list[i]+ext))
		return renlog

	def rename(self, mode:str, args:dict={}, name:str=None, err:bool=False):
		name = re.sub(r'[\\/:*?"<>|\r\n]+', "_", name) if name else None
		if 'RenameRef' == mode:
			arg_list = [('PathRen','dir','Path Rename: '), ('PathRef','dir','Path Reference: ')]
			for (key, type, memo) in arg_list:
				if key not in args:
					args[key] = input(memo)
				msg = self.validate_path(args[key], type, err)
				if msg:
					return msg
			renlog = self.rename_ref(args['PathRen'], args['PathRef'])
			self.write_log('RenameRef', name, {'PathRen':args['PathRen'], 'PathRef':args['PathRef']}, renlog)
		elif 'RenameList' == mode:
			arg_list = [('PathRen', 'dir', 'Path Rename: '), ('PathList', 'file', 'Path Namelist: ')]
			for (key, type, memo) in arg_list:
				if key not in args:
					args[key] = input(memo)
				msg = self.validate_path(args[key], type, err)
				if msg:
					return msg
			renlog = self.rename_list(args['PathRen'], args['PathList'])
			self.write_log('RenameList', name, {'PathRen':args['PathRen']}, renlog)
