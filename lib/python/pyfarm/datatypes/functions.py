# No shebang line, this module is meant to be imported
#
# This file is part of PyFarm.
# Copyright (C) 2008-2012 Oliver Palmer
#
# PyFarm is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyFarm is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with PyFarm.  If not, see <http://www.gnu.org/licenses/>.

'''
functions for use within the datatypes module
'''

def notimplemented(name, module='psutil'):
    msg = "this version of %s does not implement %s(), " % (module, name)
    msg += "please consider upgrading"
    raise NotImplementedError(msg)
# end notimplemented

def bytes_to_megabytes(value):
    return int(value / 1024 / 1024)
# end bytes_to_megabytes