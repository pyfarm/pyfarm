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
minor network library to return information related to
domain name services
'''

import socket

from pyfarm import datatypes

def ip(hostname=None):
    '''returns the hostname of the current machine'''
    if hostname is None:
        hostname = socket.gethostname()

    try:
        addr = socket.gethostbyname(hostname)
        return addr

    except socket.gaierror, error:
        # in some circumstances os x will not be
        # able to query it's own hostname in dns because
        # the local dns cache is expecting <hostname>.local
        # to be looked up
        if datatypes.OS == datatypes.OperatingSystem.MAC:
            hostname = "%s.local" % hostname
            return socket.gethostbyname(hostname)

        # similar situation for windows when attempting to
        # perform lookups and the local dns cache takes
        # precedence over asking the dns server
        elif datatypes.OS == datatypes.OperatingSystem.WINDOWS:
            hostname = "%s." % hostname
            return socket.gethostbyname(hostname)

        raise
# end ip