# No shebang line, this module is meant to be imported
#
# This file is part of PyFarm.
# Copyright (C) 2008-2013 Oliver Palmer
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

"""
main preferences module which contains a base class for use outside of
:mod:`pyfarm.preferences`
"""

from lib.python.pyfarm.preferences.base.loader import Loader
from lib.python.pyfarm.preferences.base.enums import NOTSET


class Preferences(object):
    """
    The main preferences object which may be subclassed by other
    preference objects for extension purposes.

    :param string prefix:
        the directory prefix to use when searching for
        preferences

    :param string filename:
        the filename to use for queries.  As an example these
        will have the same results:

            >>> p1 = Preferences()
            >>> p2 = Preferences(filename='database')
            >>> assert p1.get('database.setup') == p2.get('setup')
    """
    _data = {}

    def __init__(self, prefix=None, filename=None):
        self.prefix = '' if prefix is None else prefix
        self.filename = filename
    # end __init__

    @classmethod
    def _get(
            cls, key, failobj=NOTSET, force=False, return_loader=False,
            filename=None
    ):
        """
        See :meth:`get` for this classmethod's documentation.  This
        classmethod is called internally by :meth:`get` and returns class
        level data
        """
        # before we do anything check to see if the requested key
        # is something that maps to a callable function
        split = key.split(".")
        if filename is None:
            filename = split[0]
            key_uri = ".".join(split[1:])
        else:
            key_uri = ".".join(split)

        # load the underlying data if necessary, retrieve it from
        # cace otherwise
        if filename not in cls._data:
            data = cls._data[filename] = Loader(filename, force=force)
        else:
            data = cls._data[filename]

        # simply return the data if the filename
        # we found was the same as the key key
        if filename != key:
            try:
                data = data[key_uri]

            except KeyError:
                if failobj is not NOTSET:
                    return failobj
                raise
        else:
            return data if return_loader else data.data.copy()

        return data
    # end _get

    def get(self, key, failobj=NOTSET, force=False, return_loader=False):
        """
        Base classmetod which is used for the sole purpose of data
        retrieval from the yaml file(s).

        :param failobj:
           the object to return in the even of failure, if this value is
           not provided the original exception will be raised

        :param boolean force:
           if True then force reload the underlying file(s)

        :param boolean return_loader:
           if True and the key requested happened to be a preference file
           name then return the loader instead of a copy of the loader data

        :exception KeyError:
           This behaves slightly differently from :meth:`dict.get` in that
           unless failobj is set it will reraise the original exception
        """
        return self._get(
            key, failobj=failobj, force=force, return_loader=return_loader,
            filename=self.filename
        )
    # end get
# end Preferences