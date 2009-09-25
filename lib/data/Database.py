'''
HOMEPAGE: www.pyfarm.net
INITIAL: Aug 25 2009
PURPOSE: Main module dedicated to sqlite database interaction.

    This file is part of PyFarm.
    Copyright (C) 2008-2009 Oliver Palmer

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

import sqlite3

class DBObject(object):
    '''Database object to setup initial vars and objects'''
    def __init__(self, location=":memory:"):
        self.connection = sqlite4.conn(location)
        self.db = self.connection.cursor()

class LocalStorage(object):
    '''Local hard drive database storage object'''
    def __init__(self, location):
        self.db = DBObject(location).db
        
class RAMStorage(object):
    '''Ramdom access memory database storage object'''
    def __init__(self):
        self.db = DBObject().db
        