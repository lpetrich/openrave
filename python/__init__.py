# -*- coding: utf-8 -*-
# 
# OpenRAVE Python bindings are licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License. 
#
# example code from: http://code.activestate.com/recipes/576508-version-specific-import/
if '_original__import__' not in locals():
    _original__import__ = __import__

def loadstable(ver):
    return _loadversion(ver, prefix="_openravepy_")

def loadlatest():
    return _loadversion('', prefix="_latest_")

def _loadversion(ver, prefix):
    targetname = prefix + ver.replace('.', '_')
    mainpackage = _original__import__("openravepy", globals(), locals(), [targetname])
    global openravepy_currentversion
    openravepy_currentversion = getattr(mainpackage, targetname)
    # Let users change versions after choosing this one
    openravepy_currentversion.loadstable = loadstable
    openravepy_currentversion.loadlatest = loadlatest
    return openravepy_currentversion

def myimport(name, theglobals=None, thelocals=None, fromlist=None, level=-1):
    if name.split('.')[0] != "openravepy":
        return _original__import__(name, theglobals, thelocals, fromlist, level)

    if not openravepy_currentversion:
        raise Exception("After importing openravepy, you must load a specific version by typing something like 'openravepy = openravepy.loadstable(\"0.1\")' .")

    def withversion(name):
        """
        Turn "openravepy[.anything]" into "<versionname>[.anything]" , where <versionname> is something like 'openravepy._openravepy_0_1'
        """
        parts = name.split('.')
        parts[0] = openravepy_currentversion.__name__ # eg 'openravepy._openravepy_0_1'
        return '.'.join(parts)

    # "import openravepy[.whatever.whatever]"
    if not fromlist:
        # use <versionname> instead of "openravepy", but otherwise execute the  import as expected
        _original__import__(withversion(name), theglobals, thelocals, fromlist, level)
        # but return <openravepy_currentversion> as the top-level package instead of returning openravepy as expected
        return openravepy_currentversion

    # "from openravepy[.whatever.whatever] import thing": instead,
    # "from <versionname>[.whatever.whatever] import thing", and 
    # return thing as expected
    return _original__import__(withversion(name), theglobals, thelocals, fromlist, level)

__builtins__['__import__'] = myimport

try:
    if __openravepy_noautoload__:
        openravepy_currentversion = None
    else:
        openravepy_currentversion = loadlatest()
except NameError:
    openravepy_currentversion = loadlatest()

if openravepy_currentversion is not None:
    from _latest_ import *
    from _latest_ import __version__
    from _latest_ import __author__
    from _latest_ import __copyright__
