'''
HOMEPAGE: www.pyfarm.net
INITIAL: Dec 26 2010
PURPOSE: To handle the setup and maintenance of the network table

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

CWD      = os.path.dirname(os.path.abspath(__file__))
PYFARM   = os.path.abspath(os.path.join(CWD, "..",  ".."))
MODULE   = os.path.basename(__file__)
LOGLEVEL = 2
if PYFARM not in sys.path: sys.path.append(PYFARM)

from PyQt4.Qt import Qt
from PyQt4 import QtSql, QtCore

from lib import Logger

# setup logging
log = Logger.Logger(MODULE, LOGLEVEL)

class Manager(object):
    '''
    SqlTable manager for QTableView objects.

    VARIABLES:
        ui        (QTableView) -- Table to add sql model to
        tableName (str)        -- Name of database to run query on
        path      (str)        -- Location of sql file (or special memory string)
        columns   (list)       -- Columns to retrieve from table
        sort      (str)        -- Column to sort table by
    '''
    def __init__(self, ui, tableName, path, columns, sort=None):
        self.ui        = ui
        self.tableName = tableName
        self.path      = path
        self.columns   = columns
        self.sqlModel  = QtSql.QSqlTableModel()
        self.sqlTable  = QtSql.QSqlDatabase.addDatabase("QSQLITE")

        query = "SELECT %s FROM %s" % (','.join(columns), self.tableName)

        # create global column variables
        i = 0
        for column in columns:
            vars()[column] = i
            i += 1

        # final setup
        self.sqlTable.setDatabaseName(path)
        self.sqlModel.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.sqlModel.setTable(self.tableName)

        if self.sqlTable.open():
            self.sqlQuery = QtSql.QSqlQuery(query)
            self.select   = self.sqlModel.setQuery(self.sqlQuery)

            # set header data
            direction  = QtCore.Qt.Horizontal
            for column in columns:
                label  = QtCore.QVariant(column.lower().capitalize())
                colNum = vars()[column]
                self.sqlModel.setHeaderData(colNum, direction, label)

            # set sorting, if a sort column was given
            if sort:
                self.sqlModel.setSort(vars()[sort], QtCore.Qt.AscendingOrder)

            # set interface's model
            self.ui.setModel(self.sqlModel)

        else:
            log.error("Failed to open database!!")

    def refresh(self):
        log.debug("Refreshing host table")
        self.sqlModel.select()