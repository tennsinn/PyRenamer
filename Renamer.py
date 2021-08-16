import os

class Renamer():
	def __init__(self):
		pass

	def get_files_in_path(self, path):
		flist = os.listdir(path)
		flist.sort()
		return flist

	def rename_ref(self):
		path_ren = input("Path Rename: ")
		flist_ren = self.get_files_in_path(path_ren)
		len_ren = len(flist_ren)
		path_ref = input("Path Ref: ")
		flist_ref = self.get_files_in_path(path_ref)
		len_ref = len(flist_ref)
		for i in range(min(len_ren,len_ref)):
			ext = os.path.splitext(flist_ren[i])[1]
			base = os.path.splitext(flist_ref[i])[0]
			os.rename(path_ren+'/'+flist_ren[i], path_ren+'/'+base+ext)
