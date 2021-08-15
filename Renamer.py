import os

def rename_ref():
	path_ren = input("Path Rename: ")
	flist_ren = os.listdir(path_ren)
	flist_ren.sort()
	len_ren = len(flist_ren)
	path_ref = input("Path Ref: ")
	flist_ref = os.listdir(path_ref)
	flist_ref.sort()
	len_ref = len(flist_ref)
	for i in range(min(len_ren,len_ref)):
		ext = os.path.splitext(flist_ren[i])[1]
		base = os.path.splitext(flist_ref[i])[0]
		os.rename(path_ren+'/'+flist_ren[i], path_ren+'/'+base+ext)

if __name__ == '__main__':
	rename_ref()
