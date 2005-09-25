#
# cfilter.py -- Client filter functions
#
#    Copyright (C) 1999-2002  Peter Liljenberg <petli@ctrl-c.liu.se>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""plwm.filter contains various classes and functions which can be
used to create client filters.  These client filters can be used in
various places, e.g. for selecting whether a client window should have
a frame, which clients to cycle among for selection, etc.

A filter is called with one argument, a client object.  The return
value is true or false, depending on how the filter evaluated for the
client.

Simple filter functions:

  true		always true
  false		always false
  is_client     true if the object is a wmanager.Client instance
  
  iconified     true if the client is iconified
  mapped        true if the client is mapped

Functions matching the client resource name (i.e. res_name or res_class):

  name(string)     true if the name exactly matches string
  re_name(regexp)  true if the name matches the regexp string
  glob_name(glob)  true if the name matches the glob string

Functions matching the client title:

  title(string)     true if the title exactly matches string
  re_title(regexp)  true if the title matches the regexp string
  glob_title(glob)  true if the title matches the glob string

Compound filters:

  And(filter, filter...)  true if all the filters are true
  Or(filter, filter...)   true if any of the filters are true
  Not(filter)             true if the filter is false

"""

import re
import fnmatch

# We must use class objects everywhere.  This is caused by the method
# semantics used in Python: anytime we get the value of an attribute
# in a class, and that value is a function, it is converted into a
# method object.  Since it is likely that filters will be assigned to
# class attributes, e.g. Client.start_iconified, we can't allow any
# filter to be ordinary functions.  So instead we use Python objects
# with a __call__ method to circumvent this problem.

# To limit the performance penalty we sets self.__call__ to
# self.__call__.  This subtle little assignment will fetch the unbound
# __call__ method from the class dict, bind it to the instance and
# assign it to the instance dict.  This reduces each filter invokation
# to a normal function call.  Additionally, this avoids having to
# traverse the class tree to find the method.

# The drawback is that we create a circular reference, which
# introduces a memory leak for Python 1.5.2 users.  Therefore, we only
# use this technique for the static filters which shouldn't get
# garbage collected anyway.  When 1.5.2 support is dropped, we can let
# the dynamic objects do this too.


class StaticClientFilter:
    def __init__(self):
	self.__call__ = self.__call__
	
class _True(StaticClientFilter):
    def __call__(self, c):
	return 1
true = _True()
all = true

class _False(StaticClientFilter):
    def __call__(self, c):
	return 0
false = _False()
none = false

class And:
    def __init__(self, *args):
	self.filters = args

    def __call__(self, c):
	for f in self.filters:
	    if not f(c):
		return 0
	return 1

class Or:
    def __init__(self, *args):
	self.filters = args

    def __call__(self, c):
	for f in self.filters:
	    if f(c):
		return 1
	return 0

class Not:
    def __init__(self, filter):
	self.filter = filter

    def __call__(self, c):
	return not self.filter(c)


class _IsClient(StaticClientFilter):

    # We can't import wmanager when cfilter is loaded,
    # since wmanager imports cfilter.  If we try,
    # nothing will have been evaluated so there is no
    # attributes here.  So to avoid this circular dependency,
    # import wmanager when we first call this filter and fetch
    # the client class.  Then reset the __call__ method to the real
    # __call__ method.  
    
    def __call__(self, c):
	import wmanager
	self.client_class = wmanager.Client
	self.__call__ = self.real___call__
	return self.real___call__(c)

    def real___call__(self, c):
	return isinstance(c, self.client_class)
    
is_client = _IsClient()

class _Iconified(StaticClientFilter):
    def __call__(self, c):
	return not c.is_mapped()
iconified = _Iconified()

class _Mapped(StaticClientFilter):
    def __call__(self, c):
	return c.is_mapped()
mapped = _Mapped()


class _NameBase:
    def __init__(self, pattern):
	self.pattern = pattern

    def check(self, str):
	if str is None:
	    return self.pattern is None
	else:
	    return self.check_pattern(str)

class _StringName(_NameBase):
    def check_pattern(self, str):
	return self.pattern == str

class _ReName(_NameBase):
    def __init__(self, pattern):
	_NameBase.__init__(self, re.compile(pattern))

    def check_pattern(self, str):
	return self.pattern.search(str) is not None

class _GlobName(_NameBase):
    def check_pattern(self, str):
	return fnmatch.fnmatchcase(str, self.pattern)

class _Title:
    def __call__(self, c):
	return self.check(c.get_title())

class _Resource:
    def __call__(self, c):
	return self.check(c.res_name) or self.check(c.res_class)

class name(_StringName, _Resource): pass
class re_name(_ReName, _Resource): pass
class glob_name(_GlobName, _Resource): pass

class title(_StringName, _Title): pass
class re_title(_ReName, _Title): pass
class glob_title(_GlobName, _Title): pass
