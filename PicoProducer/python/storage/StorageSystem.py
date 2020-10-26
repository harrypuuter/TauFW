# Author: Izaak Neutelings (May 2020)
# Description: Superclass of a generic storage system with common operations like
#              ls, cp, rm, mkdir, etc. to allow for easy implementation of storage system plug-ins.
import os
from fnmatch import fnmatch # for glob pattern
from TauFW.common.tools.utils import execute
from TauFW.common.tools.file import ensuredir, rmfile
from TauFW.PicoProducer.storage.utils import LOG
import getpass, platform


class StorageSystem(object):
  
  def __init__(self,path,verb=0,ensure=False):
    self.path    = path
    self.lscmd   = 'ls'
    self.lsurl   = ''
    self.cdcmd   = 'cd'
    self.cdurl   = ''
    self.cpcmd   = 'cp'
    self.cpurl   = ''
    self.rmcmd   = 'rm -rf'
    self.rmurl   = ''
    self.mkdrcmd = 'mkdir -p'
    self.mkdrurl = ''
    self.chmdprm = '777'
    self.chmdcmd = 'chmod'
    self.chmdurl = ''
    self.haddcmd = 'hadd -f'
    self.tmpdir  = '/tmp/$USER/' # $TMPDIR # mounted temporary directory
    self.fileurl = ""
    self.verbosity = verb
    if path.startswith('/'):
      self.parent = '/'.join(path.split('/')[:3])
    else:
      self.parent = '/'+'/'.join(path.split('/')[:2])
    self.mounted  = os.path.exists(self.parent)
  
  def __str__(self):
    return self.path
  
  def __repr__(self):
    return '<%s("%s") at %s>'%(self.__class__.__name__,self.path,hex(id(self)))
  
  def execute(self,cmd,**kwargs):
    kwargs.setdefault('verb',self.verbosity)
    return execute(cmd,**kwargs)
  
  def expandpath(self,*paths,**kwargs):
    """Help function to replace variables in given path, or set default to own path."""
    #verb = kwargs.get('verb',self.verbosity)
    here  = kwargs.get('here',False)
    url   = kwargs.get('url', "")
    paths = [p for p in paths if p]
    if paths:
      path = os.path.join(*paths)
    else:
      path = self.path
    if here and path[0] not in ['/','$']:
      path = os.path.join(self.path,path)
    if url and ('$PATH' in path or path.startswith(self.parent)):
      path = url+path
    path = path.replace('$PATH',self.path)
    return path
  
  def file(self,*paths,**kwargs):
    """Ensure that a given file exists, and append a file URL if needed."""
    ensure = kwargs.get('ensure',False)
    path   = self.expandpath(*paths,here=True)
    if path.startswith(self.parent):
      path = self.fileurl + path
    if ensure:
      if not self.exists(path):
        LOG.throw(IOError,"Did not find %s."%(path))
    return path
  
  def exists(self,*paths,**kwargs):
    """Ensure that a given path exists."""
    verb = kwargs.get('verb',self.verbosity)
    path = self.expandpath(*paths,here=True)
    cmd  = "if `%s %s%s >/dev/null 2>&1`; then echo 1; else echo 0; fi"%(self.lscmd,self.lsurl,path)
    out  = self.execute(cmd,verb=verb).strip()
    return out=='1'
  
  def ensuredir(self,*paths,**kwargs):
    """Ensure path exists."""
    verb = kwargs.get('verb',self.verbosity)
    path = self.expandpath(*paths)
    if not self.exists(path,verb=verb):
      self.mkdir(path,verb=verb)
    return True
  
  def cd(self,*paths,**kwargs):
    """Change directory if mounted."""
    if self.mounted:
      #verb = kwargs.get('verb',self.verbosity)
      path = self.expandpath(*paths)
      ret  = os.chdir(path)
      #ret  = self.execute("%s %s%s"%(self.cdcmd,self.cdurl,path)).split('\n')
    return ret
  
  def ls(self,*paths,**kwargs):
    """List contents of given directory."""
    verb    = kwargs.get('verb',self.verbosity)
    dryrun  = kwargs.get('dry', False)
    filter  = kwargs.get('filter',None) # filter with glob pattern, like '*' or '[0-9]' wildcards
    path    = self.expandpath(*paths)
    retlist = self.execute("%s %s%s"%(self.lscmd,self.lsurl,path),fatal=False,dry=dryrun,verb=verb).split('\n')
    if retlist and 'No such file or directory' in retlist[0]:
      LOG.warning(retlist[0])
      retlist = [ ]
    elif filter:
      for file in retlist[:]:
        if not fnmatch(file,filter):
          retlist.remove(file)
    return retlist
  
  def getfiles(self,*paths,**kwargs):
    """Get list of files in a given path.
    Return list of files with full path name, and if needed, a file URL.
    Use the 'filter' option to filter the list of file names with some pattern."""
    verb     = kwargs.get('verb',self.verbosity)
    fileurl  = kwargs.get('url', self.fileurl)
    filter   = kwargs.get('filter',None) # filter with glob pattern, like '*' or '[0-9]' wildcards
    path     = self.expandpath(*paths)
    filelist = self.ls(path,**kwargs)
    if fileurl and path.startswith(self.parent):
      if not isinstance(fileurl,basestring):
        fileurl = self.fileurl
    else:
      fileurl = ""
    for i, file in enumerate(filelist):
      if filter and not fnmatch(file,filter): continue
      filelist[i] = fileurl+os.path.join(path,file)
    return filelist
  
  def cp(self,source,target=None,**kwargs):
    """Copy files."""
    dryrun = kwargs.get('dry', False)
    verb   = kwargs.get('verb',self.verbosity)
    source = self.expandpath(source,url=self.cpurl)
    target = self.expandpath(target,url=self.cpurl)
    return self.execute("%s %s %s"%(self.cpcmd,source,target),dry=dryrun,verb=verb)
  
  def hadd(self,sources,target,**kwargs):
    """Hadd files. Create intermediate target file if needed."""
    target  = self.expandpath(target,here=True)
    dryrun  = kwargs.get('dry',    False)
    verb    = kwargs.get('verb',   self.verbosity)
    fileurl = kwargs.get('url',    self.fileurl)
    tmpdir  = kwargs.get('tmpdir', target.startswith(self.parent) and self.cpurl!='')
    htarget = target
    if tmpdir:
      if not isinstance(tmpdir,str):
        tmpdir = self.tmpdir
      tmpdir  = ensuredir(tmpdir,verb=verb)
      htarget = os.path.join(tmpdir,os.path.basename(target))
    if isinstance(sources,basestring):
      sources = [ sources ]
    source = ""
    for i, file in enumerate(sources,1):
      fname = os.path.basename(file)
      if '$PATH' in file and fileurl and isglob(fname): # expand glob pattern
        parent = os.path.dirname(file)
        files  = self.getfiles(parent,filter=fname,url=fileurl)
        source += ' '.join(files)+' '
      else:
        source += self.expandpath(file,url=fileurl)+' '
    source = source.strip()
    if verb>=2:
      print ">>> %-10s = %r"%('sources',sources)
      print ">>> %-10s = %r"%('source',source)
      print ">>> %-10s = %r"%('target',target)
      print ">>> %-10s = %r"%('htarget',htarget)
    out = self.execute("%s %s %s"%(self.haddcmd,htarget,source),dry=dryrun,verb=verb)
    if tmpdir:
      cpout = self.cp(htarget,target,dry=dryrun,verb=verb)
      if not dryrun:
        rmfile(htarget)
    return out
  
  def rm(self,*paths,**kwargs):
    """Remove given file or director."""
    path = self.expandpath(*paths,here=True)
    verb = kwargs.get('verb',self.verbosity)
    return self.execute("%s %s%s"%(self.rmcmd,self.rmurl,path),verb=verb)
  
  def mkdir(self,dirname='$PATH',**kwargs):
    verb    = kwargs.get('verb',self.verbosity)
    dirname = self.expandpath(dirname,here=True)
    return self.execute("%s %s%s"%(self.mkdrcmd,self.mkdrurl,dirname),verb=verb)
  
  def chmod(self,file,perm=None,**kwargs):
    verb = kwargs.get('verb',self.verbosity)
    if not perm: perm = self.chmdprm
    return self.execute("%s %s %s%s"%(self.chmdcmd,perm,self.chmdurl,file),verb=verb)
  

class Local(StorageSystem):
  
  def __init__(self,path,verb=0,ensure=False):
    super(Local,self).__init__(path,verb=verb,ensure=ensure)
    if ensure:
      self.ensuredir(self.path,verb=verb)
  
