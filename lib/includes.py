'''
HOMEPAGE: www.pyfarm.net
INITIAL: Dec5 2010
PURPOSE: Minor functions to be used by the entire package when lib is imported

    This file is part of PyFarm.
    Copyright (C) 2008-2010 Oliver Palmer

    PyFarm is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PyFarm is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with PyFarm.  If not, see <http://www.gnu.org/licenses/>.
'''
import os
import sys
import imp

CWD    = os.path.dirname(os.path.abspath(__file__))
PYFARM = os.path.abspath(os.path.join(CWD, ".."))
MODULE = os.path.basename(__file__)
if PYFARM not in sys.path: sys.path.append(PYFARM)

def importFile(filename,  verbose=False):
    (path, name) = os.path.split(filename)
    (name, ext) = os.path.splitext(name)
    try:
        (file, filename, data) = imp.find_module(name, [path])

    except ImportError, e:
        raise ImportError(e)
    return imp.load_module(name, file, filename, data)