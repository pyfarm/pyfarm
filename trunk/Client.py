#!/usr/bin/env python
'''
HOMEPAGE: www.pyfarm.net
INITIAL: May 26 2010
PURPOSE: To handle and run all client connections on a remote machine

    This file is part of PyFarm.
    Copyright (C) 2008-2011 Oliver Palmer

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

from PyQt4 import QtCore

CWD       = os.path.dirname(os.path.abspath(__file__))
PYFARM    = CWD
MODULE    = os.path.basename(__file__)
CFG_ROOT  = os.path.join(PYFARM, "cfg")
CFG_GEN   = os.path.join(CFG_ROOT, "general.ini")
CONTEXT   = MODULE.split(".")[0]

from lib.net.tcp.Queue import QueueClient

from lib.net import tcp, udp
from lib import Logger, Settings, Session

log = Logger.Logger(MODULE)

class Main(QtCore.QObject):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.masterHostname = ''
        self.masterAddress  = ''
        self.config         = Settings.ReadConfig.general(CFG_GEN)
        self.pidFile        = Session.State(context=CONTEXT)

    def handlePid(self):
        '''Handle actions relating to the process id file'''
        if self.pidFile.running() or self.pidFile.exists():
            msg = "%s You cannot run more than one client at once.%s" % (os.linesep, os.linesep)
            msg += "Would you like to shutdown the other client process? ([y]/n) "
            #response = raw_input(msg)
            response = "y"
            log.warning("Forced overwrite")

            if response.strip().lower() == "y":
                self.pidFile.write(force=True)
                self.listenForBroadcast()

            else:
                log.critical("You can only run one client at a time")
                sys.exit(1)

        else:
            self.pidFile.write()
            self.listenForBroadcast()

    def stop(self):
        '''Stop any currently running clients'''
        log.info("Attempting to stop client process")
        if self.pidFile.exists():
            self.pidFile.kill()
            self.pidFile.remove()

        log.info("Exiting")
        sys.exit(0)

    def listenForBroadcast(self):
        '''
        Step 1:
        Listen for an incoming broadcast from the master
        '''
        portNum        = self.config['servers']['broadcast']
        self.broadcast = udp.Broadcast.BroadcastReceiever(portNum, parent=self)
        self.connect(self.broadcast, QtCore.SIGNAL("masterFound"), self.setMasterAddress)
        self.broadcast.run()

    def setMasterAddress(self, response):
        '''
        Step 2:
        Set self.master to the incoming ip
        '''
        newName = False
        newAddr = False

        # check for new hostname
        if response[0] != self.masterHostname:
            self.masterHostname  = response[0]
            newName              = True

        # check for new address
        if response[1] != self.masterAddress:
            self.masterAddress = response[1]
            newName            = True

        # if new hostname OR address, update log and
        #  refresh services
        portNum = self.config['servers']['queue']
        queue   = tcp.Queue.QueueClient(self.masterAddress, port=portNum)
        if newName or newAddr:
            log.info("Received master address")
            queue.addClient()

        else:
            log.info("Already connected to master: %s" % response[0])
            queue.addClient(new=False)


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option(
                        "--stop", dest="stop",
                        default=False, action="store_true",
                        help="Stop any currently running clients"
                    )

    (options, args) = parser.parse_args()
    app  = QtCore.QCoreApplication(sys.argv)
    main = Main(app)

    if options.stop:
        main.stop()

    else:
        main.handlePid()

    sys.exit(app.exec_())