'''
HOMEPAGE: www.pyfarm.net
INITIAL: March 28 2010
PURPOSE: Module to provide compression support for binary files

This file is part of PyFarm.
Copyright (C) 2008-2010 Oliver Palmer

PyFarm is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyFarm is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyFarm.  If not, see <http://www.gnu.org/licenses/>.
'''

import zlib
from lib.Logger import Logger

__MODULE__ = "lib.Compress"

###
# NOTES
###
# Vary compression level based on size of file