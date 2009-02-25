'''
AUTHOR: Oliver Palmer
CONTACT: oliverpalmer@opalmer.com
INITIAL: Feb 6 2009
PURPOSE: Module used to configure a command line render based on operating system
and architecture.   This module first looks at the operating system, then the arhitecture.
After discovering this information it will then try and discover the currently installed software.

    This file is part of PyFarm.

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

from os import listdir, system
from os.path import isfile, islink, isdir, normpath
from Util import GetOs
from PyQt4.QtCore import QRegExp


def AddExtraPath(inputPath):
    '''
    If we find extra paths to add, insert them into the
    search list.
    '''
    if len(inputPath)>=1:
        for addPath in inputPath:
            yield addPath
    else:
        pass

class SoftwareInstalled(object):
    '''
    Preconfigure the software

    INITIAL VARS:
        self.os -- the os of the system (linux, mac, windows)
        self.arch -- the architecture of the processor (x86, x64)

    NOTES:
        -Each program config function contains a prefixList, this is the path
        to search for the installed software
    '''
    def __init__(self):
        os_arch = GetOs()
        self.os = os_arch[0]
        self.arch = os_arch[1]

    def _findProgram(self, expession, expCapStart, prefixes, renderSearchPath, commonName, fileGrep, widgetIndex):
        '''
        Given a regular expression and other information,
        search for and return all results.

        INPUT:
            expession -- regular expression to use in search
            expCapStart -- Position to return cap from
            prefixes -- paths to searh for programs
            renderSearchPath -- final path to renderer, used in search bu adding the prefix+searchresult
            commonName -- common program name to add to output
            fileGrep, -- grep used to search for scene/script files
            widgetIndex -- widget index value for gui
        '''
        exp = QRegExp(expession) # declare the regular expression

        # linux/mac loop
        if self.os == 'linux' or self.os == 'mac':
            for prefix in prefixes:
                if isdir(prefix):
                    for result in listdir(prefix):
                        if not exp.indexIn(result): # use a regular expression
                            # if the forward slash exists, remove it
                            if renderSearchPath[0] == '/':
                                renderer = renderSearchPath[1:]

                            if isfile('%s/%s/%s' % (prefix, result, renderer)):
                                yield [str(exp.cap(0)[expCapStart:]), '%s/%s/%s::%s::%s::%s' \
                                                      % (prefix, result, renderer, commonName, fileGrep, widgetIndex)]

        # see above if statement for documentation
        # windows loop
        elif self.os == 'windows':
            for prefix in prefixes:
                if isdir(prefix):
                    for result in listdir(prefix):
                        if not exp.indexIn(result):
                            if renderSearchPath[0:1] == '\\':
                                renderer = renderSearchPath[1:]

                            if isfile('%s\\%s\\%s' % (prefix, result, renderer)):
                                yield [str(exp.cap(0)[expCapStart:]), '%s\\%s\\%s::%s::%s::%s' \
                                                      % (prefix, result, renderer, commonName, fileGrep, widgetIndex)]

    def maya(self, extraPath=[]):
        '''
        Return all of the installed versions of maya as a dictionary

        INPUT:
            extraPath -- Add extra path(s) to search for
        '''
        OUTPUT = {}
        prefixList = []
        commonName = 'maya'
        fileGrep = 'Maya Scene File (*.mb *.ma)'
        widgetIndex = '0'
        expression = r"""[m|M]aya(200[89]|8.[05]|8[05]|7(.0|0))"""


        # if we find user declared paths to use, add them
        for newPath in AddExtraPath(extraPath):
            prefixList.append(newPath)

        if self.os == 'linux':
            # paths to search for maya
            prefixList.append('/usr/autodesk')

            for result in self._findProgram(expression, 4, prefixList, '/bin/Render', commonName, fileGrep, widgetIndex):
                OUTPUT['Maya '+ result[0]] = result[1]

        elif self.os == 'mac':
            prefixList.append('/Applications/Autodesk/')

        elif self.os == 'windows':
            ###########################
            # system call note below: NOTE THE DOUBLE QUOTES!
            #system('"%s\\%s\\%s"' % (prefix, result, renderPath))
            ###########################
            prefixList.append('C:\\Program Files\\Autodesk')

            for result in self._findProgram(expression, 4, prefixList, '\\bin\\Render.exe', commonName, fileGrep, widgetIndex):
                OUTPUT['Maya '+ result[0]] = result[1]

        return OUTPUT


    def houdini(self, extraPath=[]):
        '''
        Return all of the houdini versions installed

        INPUT:
            extraPath -- Add extra path(s) to search for

        RENDERING NOTES:
            usage: hscript <random_seed>_<project_name>.<frame_num>.cmd
        '''
        OUTPUT = {}
        prefixList = []
        commonName = 'houdini'
        fileGrep = 'Houdini File (*.hip)'
        widgetIndex = '1'
        expression = r"""hfs9.[15].[0-9]+"""
        win_expression = r"""Houdini 9.[15].[0-9]+"""

        # if we find extra paths to use, add them
        for newPath in AddExtraPath(extraPath):
            prefixList.append(newPath)

        if self.os == 'linux':
            prefixList.append('/opt')
            prefixList.append('/usr')

            for result in self._findProgram(expression, 3, prefixList, '/bin/hbatch', commonName, fileGrep, widgetIndex):
                OUTPUT['Houdini '+ result[0]] = result[1]

        elif self.os == 'mac':
            pass

        elif self.os == 'windows':
            prefixList.append('C:\\Program Files\\Side Effects Software')

            for result in self._findProgram(win_expression, 8, prefixList, '\\bin\\hbatch.exe', commonName, fileGrep, widgetIndex):
                OUTPUT['Houdini '+ result[0]] = result[1]

        return OUTPUT

    def shake(self, extraPath=[]):
        '''
        Return the installation of shake, if it is installed

        INPUT:
            extraPath -- Add extra path(s) to search for

        SHAKE FLAG NOTES:
            v/vv -- Verbose(-vv just gives you a percentage as the frames render) .
            cpus -- number of cpus to use
            sequential -- will process each file out node in turn.
            t -- fram range (ex. 1-10)
        '''
        OUTPUT = {}
        commonName = 'shake'
        fileGrep = 'Shake Script (*.shk)'
        widgetIndex = '2'
        prefixList = ['/usr/apple/shake-v4.00.0607', '/opt/shake', \
                           '/usr/local/shake']

        # if we find extra paths to use, add them
        for newPath in AddExtraPath(extraPath):
            prefixList.append(newPath)

        if self.os == 'linux':
            for prefix in prefixList:
                if isdir(prefix):
                    for result in listdir(prefix):
                        if isfile('%s/%s/shake' % (prefix, result)):
                            OUTPUT["Shake"] = '%s/%s/shake::%s::%s::%s' % (prefix, result, commonName, fileGrep, widgetIndex)

        if self.os == 'mac':
            prefixList = ['/Applications/Shake/shake.app/Contents/MacOS/shake']

        return OUTPUT

class ConfigureCommand(object):
    '''
    Given an input dictionary and a program (ex. self.maya)
    yield the output commands
    '''
    def __init__(self, softwareDict):
      self.software = softwareDict

    def maya(self, ver, sFrame, eFrame, bFrame, rayRender):
      '''
      Yield the sequence of frames for maya

      VARS:
         ver -- Version of maya to pull from self.software
         sFrame -- Start frame of sequence
         eFrame -- End Frame of sequence
         bFrame -- By frame or sequence step
         rayRender -- If using mental ray, set to true
      '''
      version = self.sofware[ver]

    def houdini(self, ver, sFrame, eFrame, bFrame):
      '''
      Yield the sequence of frames for houdini

      VARS:
        ver -- Version of houdini to pull from self.software
        sFrame -- Start frame of sequence
        eFrame -- End Frame of sequence
        bFrame -- By frame or sequence step
      '''
      version = self.sofware[ver]

    def shake(self, version, sFrame, eFrame, bFrame):
      '''
      Yield the sequence of frames for shake

      VARS:
        ver -- Version of shake to pull from self.software
        sFrame -- Start frame of sequence
        eFrame -- End Frame of sequence
        bFrame -- By frame or sequence step
      '''
      version = self.sofware[ver]


class RenderLayerBreakdown(object):
    '''
    Breakdown an input file into individual layers.
    Yield each layer back to the ui.
    '''
    def __init__(self, inputFile):
        self.file = inputFile

    def houdini(self):
        '''Output the houdini mantra nodes'''
        hip = open(self.file)
        exp = QRegExp(r"""[0-9]+out/[0-9a-zA-Z]+[.]parm""")

        for line in hip.readline():
            if not exp.indexIn(line):
                yield line



# small set of tests

# get ready to find the currently installed software
#LOCAL_SOFTWARE = {}
#software = SoftwareInstalled()

# find the software and add it to the dictionary
#LOCAL_SOFTWARE.update(software.maya())
#LOCAL_SOFTWARE.update(software.houdini())
#LOCAL_SOFTWARE.update(software.shake())

#for (software,path) in LOCAL_SOFTWARE.items():
#    print path.split('::')[1]
#    print 'Found %s at %s' % (software,path)
#
#print LOCAL_SOFTWARE