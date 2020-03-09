"""Class library that provides runtime environment monitoring functionality for computer tasks

:Classes:
        Environment - wrapper around Pyschopy environment checking functionality

:
:Author:
    Joe Hesse, jhesse@memory.ucsf.edu

"""

# Part of the LavaTask Library
# Copyright (C) 2011, Regents of the University of California
# All Rights Reserved
#
# Distributed under the terms of the BSD 2-Clause License
# (http://www.opensource.org/licenses/BSD-2-Clause)

import os
from psychopy import info, logging
from time import strftime
from csv import DictWriter
import pyglet
pyglet.options['debug_gl'] = False#must be done before importing pyglet.gl or pyglet.window
import pyglet.gl, pyglet.window

class Environment (object):
    """The primary object representing the computer based testing environment.



    """
    def __init__(self,configuration):
        self.pyschopyVersion=''  #version of psychopy
        self.machineName='' #the host name of the machine
        self.systemPlatform='' #the type and version of the Operating System
        self.pythonVersion='' #version of python
        self.windowRefreshMedian='' #median of the window refresh time in ms
        self.windowRefreshMean='' #mean of the window refresh time in ms
        self.windowRefreshStdev='' #stdev of the window refresh time in ms
        self.envVersion='1.1.0.0' #version of this environment class
        self.siteId=configuration.getSiteId() #site id - specific to the deployment
        self.machineId=configuration.getMachineId() #machine unique id - configured manually
        self.dataPath=configuration.getDataPath()  # for storing data
        self.screen=int(configuration.getDisplayScreen()) #screen to use
        self.widthCm=float(configuration.getDisplayWidthCm()) #height of the display in centimeters
        self.widthPx = 0 #default to zero, so if we cannot determine screen size it is obvious
        self.heightPx = 0 #default to zero, so if we cannot determine screen size it is obvious

    def run(self):
        self.getRunTimeInfo()
        self.getDisplayResolutionInPx()
        self.writeEnvironmentData()


    def getOS(self):
        if(self.systemPlatform.lower().startswith('linux')):
           return 'linux'
        elif(self.systemPlatform.lower().startswith('windows')):
            return 'windows'
        elif(self.systemPlatform.lower().startswith('darwin')):
            return 'osx'
        else:
            return 'undetermined'

    def getRunTimeInfo(self):
         cwd = os.getcwd()  #to handle bug in PsychoPy V1.71 where the cwd gets set to the psychopy lib folder.
         rtInfo = info.RunTimeInfo()
         os.chdir(cwd)
         self.psychopyVersion = rtInfo['psychopyVersion']
         self.pythonVersion = rtInfo['pythonVersion']
         self.machineName = rtInfo['systemHostName']
         self.systemPlatform = rtInfo['systemPlatform']
         self.windowRefreshStdev = rtInfo['windowRefreshTimeSD_ms']
         self.windowRefreshMedian = rtInfo['windowRefreshTimeMedian_ms']
         self.windowRefreshMean = rtInfo['windowRefreshTimeAvg_ms']
         self.envDate = strftime("%m/%d/%Y")
         self.envTime = strftime("%H:%M")

    def getEnvironmentFileNamePart(self):
        """Return the filename part that encodes the site and machine configuration."""
        part = ''
        if(self.siteId):
            part += self.siteId
        if(self.machineId):
            part += '_' + self.machineId
        return part

    def writeEnvironmentData(self):
         filename = os.path.normpath(os.path.join(self.dataPath,'Environment_' + self.getEnvironmentFileNamePart() + '.csv'))
         columns = ['site_id','machine_id','env_date','env_time','system_platform','machine_name','python_version',\
                    'psychopy_version','env_version','window_refresh_stdev','window_refresh_median','window_refresh_mean',\
                    'width_px','height_px','width_cm','screen']
         environ_data = {'site_id':self.siteId,'machine_id':self.machineId,'env_date':self.envDate,'env_time':self.envTime,'system_platform':self.systemPlatform,\
                         'machine_name':self.machineName,'python_version':self.pythonVersion,'psychopy_version':self.psychopyVersion,'env_version':self.envVersion,\
                         'window_refresh_stdev':self.windowRefreshStdev,'window_refresh_median':self.windowRefreshMedian,'window_refresh_mean':self.windowRefreshMean,\
                         'width_px':self.widthPx,'height_px':self.heightPx,'width_cm':self.widthCm,'screen':self.screen}

         if not os.path.isdir(self.dataPath):
             os.makedirs(self.dataPath)#if this fails (e.g. permissions) we will get error
         responseWriter = None
         if(not os.path.isfile(filename)):  #summary stat file does not exist.  Create and write headers
            responseWriter =  DictWriter(open(filename, 'w'),columns ,extrasaction='ignore')
            #responseWriter.writerow(dict(zip(columns,columns)))
            responseWriter.writeheader()
         else: #just open for appending if it exists
            responseWriter =  DictWriter(open(filename, 'a'),columns ,extrasaction='ignore')
         responseWriter.writerow(environ_data)

    def getDisplayResolutionInPx(self):
        if(self.widthPx==0):  #we haven't determined resolution yet
            allScrs = pyglet.window.get_platform().get_default_display().get_screens()
            if len(allScrs)>self.screen:
                thisScreen = allScrs[self.screen]
                self.widthPx = thisScreen.width
                self.heightPx = thisScreen.height

        return [self.widthPx,self.heightPx]
