#!/usr/bin/env python
# -*- python -*-
#BEGIN_LEGAL
#
#Copyright (c) 2024 Intel Corporation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  
#END_LEGAL
"""Base functionality: messages, verbosity, python version checking"""

import os
import sys
import traceback
import locale

_MBUILD_ENCODING = locale.getpreferredencoding()
def unicode_encoding() -> str:
    return _MBUILD_ENCODING

PY3 = sys.version_info > (3,)
def is_python3():
    return PY3

_mbuild_verbose_level = 1
def verbose(level=0) -> bool:
  """Return True if the configured message level supplied is >= the
  level arguement
  @param level: int
  @param level: the verbosity level at which this function should return True
  
  @rtype: bool
  @return: True iff the level argument is >= current verbosity level
  """
  global _mbuild_verbose_level
  if _mbuild_verbose_level >= level:
    return True
  return False
def set_verbosity(v):
  """Set the global verbosity level. 0=quiet, 99=very very noisy"""
  global _mbuild_verbose_level
  _mbuild_verbose_level = v

def get_verbosity():
  """Return the global verbosity level. 0=quiet, 99=very very noisy"""
  global _mbuild_verbose_level
  return _mbuild_verbose_level

def bracket(s,m='') -> str:
  """add a bracket around s and append m.
  @rtype: string
  @return: a bracketed string s and a suffixed message m
  """
  return u'[{}] {}'.format(s,m)

def error_msg(s,t):
  """Emit '[s] t' to stderr with a newline"""
  print(bracket(s,t))

def msg(s, pad=''):
  """Emit s to stdout with a newline"""
  print(pad, end='')
  print(s)
  
def msgn(s, pad=''):
  """Emit s to stdout without a newline"""
  print(pad, end='')
  print(s, end='')

def msgb(s,t='',pad=''):
  """a bracketed  string s  sent to stdout, followed by a string t"""
  msg(bracket(s,t), pad=pad)

def vmsg(v,s,pad=''):
  """If verbosity v is sufficient, emit s to stdout with a newline"""
  # someone could pass unicode as pad...
  if verbose(v):
    msg(s,pad=pad)

def vmsgb(v,s,t='',pad=''):
  """If verbosity v is sufficient, emit a bracketed string s sent to
  stdout, followed by a string t"""
  vmsg(v,bracket(s,t),pad=pad)

def cond_die(v, cmd, msg):
  """Conditionally die, if v is not zero. Print the msg and the cmd.
  @type v: int
  @param v: we die if v is not 0

  @type cmd: string
  @param cmd: a command to print

  @type msg: string
  @param msg: a message to print before the command
  """
  if v != 0:
    s = msg + "\n  [CMD] " + cmd
    die(s)

def die(m,s=''):
  """Emit an error message m (and optionally s) and exit with a return
     value 1"""
  msgb("MBUILD ERROR", "%s %s\n\n" % (m,s) )
  etype, value, tb = sys.exc_info()
  if tb is None:
    stack = traceback.extract_stack()[:-1]
    traceback.print_list(stack, file=sys.stdout)
  else:
    traceback.print_exception(etype, value, tb, file=sys.stdout)
  sys.exit(1)

def warn(m):
  """Emit an warning message"""
  msgb("MBUILD WARNING", m)

def get_python_version():
  """Return the python version as an integer
  @rtype: int
  @return: major * 100000 + minor + 1000 + fixlevel
  """
  tuple = sys.version_info
  major = int(tuple[0])
  minor = int(tuple[1])
  fix  = int(tuple[2])
  vnum = major *100000 + minor * 1000 + fix
  return vnum

def get_python_version_tuple():
  """Return the python version as a tuple (major,minor,fixlevel)
  @rtype: tuple
  @return: (major,minor,fixlevel)
  """
  
  tuple = sys.version_info
  major = int(tuple[0])
  minor = int(tuple[1])
  fix  = int(tuple[2])
  return (major,minor,fix)

def check_python_version(maj,minor,fix=0):
  """Return true if the current python version at least the one
  specified by the arguments.
  @rtype: bool
  @return: True/False
  """
  t = get_python_version_tuple()
  if t[0] > maj:
    return True
  if t[0] == maj and t[1] > minor:
    return True
  if t[0] == maj and t[1] == minor and t[2] >= fix:
    return True
  return False
  


try:
  if check_python_version(3,9) == False:
    die("MBUILD error: Need Python version 3.9 or later.")
except:
  die("MBUILD error: Need Python version 3.9 or later.")

import platform
_on_mac = False
_on_native_windows = False
_on_windows = False # cygwin or native windows
_on_cygwin = False
_on_linux  = False
_on_freebsd = False
_on_netbsd = False
_operating_system_name = platform.system()
if _operating_system_name.find('CYGWIN') != -1:
   _on_cygwin = True
   _on_windows = True
elif  _operating_system_name == 'Microsoft' or  _operating_system_name == 'Windows':
   _on_native_windows = True
   _on_windows = True
elif _operating_system_name == 'Linux':
   _on_linux = True
elif _operating_system_name == 'FreeBSD':
   _on_freebsd = True
elif _operating_system_name == 'NetBSD':
   _on_netbsd = True
elif _operating_system_name == 'Darwin':
   _on_mac = True
else:
   die("Could not detect operating system type: " + _operating_system_name)

def on_native_windows():
  """
  @rtype: bool
  @return: True iff on native windows win32/win64
  """
  global _on_native_windows
  return _on_native_windows

def on_windows(): 
  """
  @rtype: bool
  @return: True iff on  windows cygwin/win32/win64
  """
  global _on_windows
  return _on_windows

def on_mac(): 
  """
  @rtype: bool
  @return: True iff on mac
  """
  global _on_mac
  return _on_mac

######  


def bytes2unicode(bs):
    """Convert a bytes object to unicode"""
    return bs.decode(unicode_encoding())

def ensure_string(x):
    # strings in python2 turn up as bytes
    # strings in python3 show up as strings and are unicode
    if isinstance(x,bytes):
        return bytes2unicode(x)
    if isinstance(x,list):
        o = []
        for y in x:
            if isinstance(y,bytes):
                o.append( bytes2unicode(y) )
            else:
                o.append( y )
        return o
    return x

def uappend(lst,s):
    """Make sure s is unicode before adding it to the list lst"""
    lst.append(ensure_string(s))

def is_stringish(x):
   if isinstance(x,bytes) or isinstance(x,str):
      return True
   return False
