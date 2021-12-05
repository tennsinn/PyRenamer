import os
import time
import re
from typing import *

class Renamer():
    def __init__(self):
        self.init()

    def init(self):
        self.renp = ''
        self.rens = []
        self.refs = []
        self.nrefs = []
        self.ext = False
        self.prefix = ''
        self.suffix = ''
        self.spr = ' '
        self.start = False
        self.log = ''

    @staticmethod
    def validate_dir(path:str):
        if not os.path.exists(path):
            raise Exception("Dir does not exist!")
        if not os.path.isdir(path):
            raise Exception("Path is not a directory!")

    @staticmethod
    def validate_file(path:str):
        if not os.path.exists(path):
            raise Exception("File does not exist!")
        if not os.path.isfile(path):
            raise Exception("Path is not a file!")

    @staticmethod
    def filter_name(name:str):
        name = re.sub(r'[\\/:*?"<>|]+', "_", name)
        return name

    def get_names_from_dir(self, path:str):
        self.validate_dir(path)
        dirs = os.listdir(path)
        names = [self.filter_name(file) for file in dirs if os.path.isfile(os.path.join(path, file))]
        names.sort()
        return names

    def get_names_from_file(self, path:str):
        self.validate_file(path)
        names = []
        with open(path, 'r', encoding="utf-8") as f:
            for name in f.readlines():
                self.filter_name(name)
                names.append(name.strip())
        return names

    def get_names_from_text(self, text:str):
        text = self.filter_name(text)
        text = text.strip('\n').strip('\r')
        names = re.split('[\r\n]', text)
        return names

    def set_renp(self, renp:str):
        self.renp = renp

    def set_rens(self, rens:list):
        self.rens = rens

    def set_refs(self, refs:list):
        self.nrefs = self.refs = refs

    def set_ext(self, ext:Union[bool,str]):
        if isinstance(ext, str):
            ext = self.filter_name(ext)
            ext = ext.strip('.')
        self.ext = ext

    def set_prefix(self, prefix:str=None):
        self.prefix = self.filter_name(prefix)

    def set_suffix(self, suffix:str=None):
        self.suffix = self.filter_name(suffix)

    def set_spr(self, spr:str=' '):
        self.spr = self.filter_name(spr)

    def set_start(self, num:Union[bool,int,str]=0, fill:Union[bool,int,str]=False):
        self.start = str(num)
        if fill:
            self.start = self.start.zfill(int(fill))

    def get_order(self, i:Union[int,str]):
        return str(int(self.start)+int(i)).zfill(len(self.start))

    def add_ext(self):
        if not self.ext:
            self.nrefs = [ref+os.path.splitext(ren)[-1] for ren, ref in zip(self.rens, self.nrefs)]
        elif isinstance(self.ext, str):
            self.nrefs = [ref+'.'+self.ext for ref in self.nrefs]

    def add_order(self):
        if self.start:
            self.nrefs = [self.get_order(i)+self.spr+self.nrefs[i] for i in range(0, len(self.nrefs))]

    def add_prefix(self):
        if self.prefix:
            self.nrefs = [self.prefix+self.spr+ref for ref in self.nrefs]

    def add_suffix(self):
        if self.suffix:
            for i in range(0, len(self.nrefs)):
                base, ext = os.path.splitext(self.nrefs[i])
                self.nrefs[i] = base+self.spr+self.suffix+ext

    def rename(self):
        self.add_ext()
        self.add_order()
        self.add_prefix()
        self.add_suffix()
        self.set_log()
        self.write_log('Rename_Path', renp)
        os.chdir(self.renp)
        for ren, nref in zip(self.rens, self.nrefs):
            try:
                os.rename(ren, nref)
            except OSError:
                status = 'Existed'
            except:
                status = 'Error'
            else:
                status = 'Succeed'
            finally:
                self.write_log(status, ren+' -> '+nref)

    def set_log(self):
        if not os.path.exists('logs'):
            os.mkdir('logs')
        self.log = os.path.dirname(__file__)+'/logs/'+time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())+'.log'

    def write_log(self, key:str, val:str):
        with open(self.log, 'a', encoding='utf-8') as f:
            f.write(key+'='+val+'\n')

    def rollback(self, log):
        pass


if __name__ == '__main__':
    r = Renamer()
    renm = input('Rename Mode [dir / file / text]: ')
    renp = input('Rename Path: ').replace('\\', '/')
    r.set_renp(renp)
    if 'dir' == renm:
        rens = r.get_names_from_dir(renp)
    elif 'file' == renm:
        rens = r.get_names_from_file(input('Rename File: '))
    else:
        rens = r.get_names_from_text(input('Rename Text: '))
    r.set_rens(rens)
    refm = input('Reference Mode [dir / file / text]: ')
    if 'dir' == refm:
        refs = r.get_names_from_dir(input('Reference Path: ').replace('\\', '/'))
    elif 'file' == refm:
        refs = r.get_names_from_file(input('Reference Path: ').replace('\\', '/'))
    else:
        refs = r.get_names_from_text(input())
    r.set_refs(refs)
    r.set_prefix(input('Prefix: '))
    r.set_suffix(input('Suffix: '))
    flag = input('Replace ext? [y/n]: ')
    if 'y' == flag:
        ext = input('New ext: ')
        if '' == ext:
            r.set_ext(True)
        else:
            r.set_ext(ext)
    flag = input('Auto Increment? [y/n]: ')
    if 'y' == flag:
        num = input('Start Number: ')
        fill = input('Zero Fill: ')
        r.set_start(num, fill)
    r.set_spr(input('Separator: '))
    r.rename()
