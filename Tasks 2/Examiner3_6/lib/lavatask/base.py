"""Class library that provide base functionality for computer tasks

:Classes:
    Configuration - Encapsulates access to a configuration file for the runtime environment.
    Task - The primary object representing a computer based test.
    TaskClock - An encapsulation of timing for the task
    TaskClockFactory - An extendable factory method for task timing clocks.
    TestingTaskClock - A task timing mechanism that allows task timing to be "sped up" or "slowed down"
    TestingTaskClockFactory - A factory method for testing task clocks.
    Block - Highest level of organizing unit within a task,typically displays stimuli and/or records responses.
    ResponseBlock - A Block that waits for user keyboard input.
    ResponseMonitor - Encapsulates the response monitoring for a task - uses Keyboard as default.
    MouseResonseMonitor - Encapsulates response monitoring using the mouse.
    RangeResponseMonitor - Extends mouse/touch response monitoring with named screen ranges.
    ResponseRange - Encapsulates screen range info for RangeResponseMonitor
    CedrusResponseMonitor - Encapsulates response monitoring using a Cedrus Response Pad.
    TrialResponseBlock - A ResponseBlock that iterates over a set of response trials.
    SlideshowBlock - A ResponseBlock that emulates a slideshow.
    SlideshowSlide - A base class for "slides" used by the SlideshowBlock.
    InstructionBlock - A ResponseBlock that displays textual instructions.
    TaskResponses - Collection of responses during a task with functionality for writing to output files.
    TrialResponse - A utility class for recording trial responses during a task.
    Resource - Generic class functionality for locating and loading resources.
    UnicodeResource - A utility class to wrap loading unicode text resources.
    SessionConfig - A class encapsulating task session configuration.

:Author:
    Joe Hesse, jhesse@memory.ucsf.edu

"""

# Part of the LavaTask Library
# Copyright (C) 2011, Regents of the University of California
# All Rights Reserved
#
# Distributed under the terms of the BSD 2-Clause License
# (http://www.opensource.org/licenses/BSD-2-Clause)

# for some reason importing visual first solves the error of avbin.dll failing to load on windows
#from /Applications/PsychoPy3.app/Contents/Resources/lib/python3.6/psychopy/ import visual
from psychopy import visual

import os, types
from psychopy.hardware import cedrus
from psychopy import core, data, event, gui, monitors, logging
from time import strftime
from numpy import *
from csv import DictWriter
import codecs
import configparser
import lavatask.environment
#import environment


class Configuration(object):
    """Encapsulates access to a configuration file for the runtime environment.

    """
    #constants for predefined configuration file sections and options
    S_PATHS = 'paths'
    O_LAVATASK_HOME = 'home'
    O_DATA_PATH = 'data'
    O_LOG_PATH = 'log'
    O_RESOURCE_PATH='resource'
    S_DISPLAY = 'display'
    O_SCREEN = 'screen'
    O_ORIENTATION = 'orientation'
    O_WIDTHPX = 'widthpx'
    O_HEIGHTPX = 'heightpx'
    O_WIDTHCM = 'widthcm'
    S_SITE = 'site'
    O_SITEID = 'id'
    S_MACHINE = 'machine'
    O_MACHINEID = 'id'
    S_TASK = 'task'
    O_AGECOHORT = 'agecohort'
    O_LANGUAGE = 'language'
    O_FORM = 'form'
    S_FONT = 'font'
    O_NAME = 'name'
    O_SIZECM = 'sizecm'
    O_CHARSPERLINE='charsperline'
    O_CHINESE_NAME = 'chinese_name'
    O_CHINESE_SIZECM = 'chinese_sizecm'
    O_CHINESE_CHARSPERLINE='chinese_charsperline'

    def __init__(self,configFiles):
        self.configuration = {}
        self.loadConfigFiles(configFiles)

    def loadConfigFiles(self,configFiles):
        """Read in the configuration from all the specified configFiles."""

        try:
        #read in all configuration data
            config = configParser.ConfigParser()
            config.read(configFiles)
            for section in config.sections():
                for option in config.options(section):
                    self.set(section,option,config.get(section,option))
        except:
        #do nothing in particular
            return


    def get(self,section,option,default=None):
        """Returns the configured value for a section-option combination or default if not found."""
        if(section not in self.configuration.keys()  or option not in self.configuration[section].keys()):
           return default
        else:
           return self.configuration[section][option]

    def set(self,section,option,value):
        """Sets the value for a section-option combination"""
        if(section not in self.configuration.keys()):
            self.configuration.update({section:{},})
        self.configuration[section].update({option:value,})

    def getLavaTaskHome(self):
        """Returns configured LavaTask home directory or current working directory if not found."""
        return self.get(Configuration.S_PATHS,Configuration.O_LAVATASK_HOME,os.getcwd())

    def getDataPath(self):
        """Returns configured data output path or default path if not defined."""
        return self.get(Configuration.S_PATHS,Configuration.O_DATA_PATH,os.path.join(self.getLavaTaskHome(),Configuration.O_DATA_PATH))

    def getLogPath(self):
        """Returns configured log output path or default path if not defined."""
        return self.get(Configuration.S_PATHS,Configuration.O_LOG_PATH,os.path.join(self.getLavaTaskHome(),Configuration.O_LOG_PATH))

    def getResourcePath(self):
        """Returns configured resource (e.g. stimuli) path or default path if not defined."""
        return self.get(Configuration.S_PATHS,Configuration.O_RESOURCE_PATH,os.path.join(self.getLavaTaskHome(),Configuration.O_RESOURCE_PATH))

    def getDisplayScreen(self):
        """Returns configured screen number to use for task display (0 = default screen)."""
        return self.get(Configuration.S_DISPLAY,Configuration.O_SCREEN,0)

    def getDisplayOrientation(self):
        """Returns configured orientation to use for task display in degrees."""
        return self.get(Configuration.S_DISPLAY,Configuration.O_ORIENTATION,0.0)

    def getDisplayWidthCm(self):
        """Returns width of screen in cm, used to scale stimuli to consistent size ( 30 = typical 15" laptop width)."""
        return self.get(Configuration.S_DISPLAY,Configuration.O_WIDTHCM,30)

    def getSiteId(self):
        """Returns configured site id."""
        return self.get(Configuration.S_SITE,Configuration.O_SITEID,'Site_ID')

    def getMachineId(self):
        """Returns configured machine id."""
        return self.get(Configuration.S_MACHINE,Configuration.O_MACHINEID,'Machine_ID')

    def getTaskAgeCohort(self):
        """Returns configured age cohort for the task"""
        return self.get(Configuration.S_TASK,Configuration.O_AGECOHORT,'Adult')

    def getTaskLanguage(self):
        """Returns configured language for the task"""
        return self.get(Configuration.S_TASK,Configuration.O_LANGUAGE,'English')

    def getTaskForm(self):
        """Returns configured form for the task"""
        return self.get(Configuration.S_TASK,Configuration.O_FORM,'A')

    def getFontName(self,OS):
        """Returns configured name for the font"""
        return self.get(Configuration.S_FONT+'_'+OS,Configuration.O_NAME,'Courier')

    def getFontSize(self,OS):
        """Returns configured size for the font"""
        return self.get(Configuration.S_FONT+'_'+OS,Configuration.O_SIZECM,.60)

    def getFontCharsPerLine(self,OS):
        """Returns configured chars per line for the font (for centering text)"""
        return self.get(Configuration.S_FONT+'_'+OS,Configuration.O_CHARSPERLINE,65)

    def getChineseFontName(self,OS):
        """Returns configured name for the font"""
        return self.get(Configuration.S_FONT+'_'+OS,Configuration.O_CHINESE_NAME,'MingLiU')

    def getChineseFontSize(self,OS):
        """Returns configured size for the font"""
        return self.get(Configuration.S_FONT+'_'+OS,Configuration.O_CHINESE_SIZECM,1.00)

    def getChineseFontCharsPerLine(self,OS):
        """Returns configured chars per line for the font (for centering text)"""
        return self.get(Configuration.S_FONT+'_'+OS,Configuration.O_CHINESE_CHARSPERLINE,30)

    def setLavaTaskHome(self,value):
        """Sets configured LavaTask home directory. """
        return self.set(Configuration.S_PATHS,Configuration.O_LAVATASK_HOME,value)

    def setDataPath(self,value):
        """Sets configured data output path."""
        return self.set(Configuration.S_PATHS,Configuration.O_DATA_PATH,value)

    def setLogPath(self,value):
        """Sets configured log output path."""
        return self.set(Configuration.S_PATHS,Configuration.O_LOG_PATH,value)

    def setResourcePath(self,value):
        """Sets configured resource (e.g. stimuli) path."""
        return self.set(Configuration.S_PATHS,Configuration.O_RESOURCE_PATH,value)

    def setDisplayScreen(self,value):
        """Sets configured screen number to use for task display (0 = default screen)."""
        return self.set(Configuration.S_DISPLAY,Configuration.O_SCREEN,value)

    def setDisplayScreen(self,value):
        """Sets configured orientation to use for task display (0.0 = default)."""
        return self.set(Configuration.S_DISPLAY,Configuration.O_ORIENTATION,value)

    def setDisplayWidthCm(self,value):
        """Sets width of screen in cm, used to scale stimuli to consistent size ( 30 = typical 15" laptop width)."""
        return self.set(Configuration.S_DISPLAY,Configuration.O_WIDTHCM,value)

    def setSiteId(self,value):
        """sets configured site id."""
        return self.set(Configuration.S_SITE,Configuration.O_SITEID,value)

    def setMachineId(self,value):
        """Sets configured machine id."""
        return self.set(Configuration.S_MACHINE,Configuration.O_MACHINEID,value)

    def setTaskAgeCohort(self,value):
        """Set configured age cohort for the task"""
        return self.set(Configuration.S_TASK,Configuration.O_AGECOHORT,value)

    def setTaskLanguage(self,value):
        """Set configured language for the task"""
        return self.set(Configuration.S_TASK,Configuration.O_LANGUAGE,value)

    def setTaskForm(self,value):
        """Set configured form for the task"""
        return self.set(Configuration.S_TASK,Configuration.O_FORM,value)

    def setFontName(self,value):
        """Set configured name for the font"""
        return self.set(Configuration.S_FONT,Configuration.O_NAME,value)

    def setFontSize(self,value):
        """Sets configured size for the font"""
        return self.set(Configuration.S_FONT,Configuration.O_SIZECM,value)

    def setFontCharsPerLine(self,value):
        """Sets configured chars per line for the font (for centering text)"""
        return self.set(Configuration.S_FONT,Configuration.O_CHARSPERLINE,value)

    def setChineseFontName(self,value):
        """Set configured name for the font"""
        return self.set(Configuration.S_FONT,Configuration.O_CHINESE_NAME,value)

    def setChineseFontSize(self,value):
        """Sets configured size for the font"""
        return self.set(Configuration.S_FONT,Configuration.O_CHINESE_SIZECM,value)

    def setChineseFontCharsPerLine(self,value):
        """Sets configured chars per line for the font (for centering text)"""
        return self.set(Configuration.S_FONT,Configuration.O_CHINESE_CHARSPERLINE,value)

class TaskClockFactory(object):
    """Factory for TaskClocks"""

    def createClock(self):
        return TaskClock()

class TaskClock(object):
    """Utility class providing interface to timing functions.

        Primary function of this class is to decouple timing from the
        underlying clock implementation.
    """

    def __init__(self):
        self.clock = core.Clock()

    def getTime(self):
        return self.clock.getTime()

    def reset(self):
        self.clock.reset()

    def wait(self,secs):
        return core.wait(secs)


class TestingTaskClockFactory(TaskClockFactory):
    """factory class for Testing Task Clocks"""
    def __init__(self,adjustmentFactor):
        TaskClockFactory.__init__(self)
        self.adjustmentFactor = adjustmentFactor # the timing factor used to adjust the testing clocks

    def createClock(self):
        return TestingTaskClock(self.adjustmentFactor)


class TestingTaskClock(TaskClock):
    """Extension to task clock supporting "speed up" factor for faster execution of
        test suites with automated responses"""

    def __init__(self,adjustmentFactor):
        TaskClock.__init__(self)
        self.adjustmentFactor=adjustmentFactor

    def getTime(self):
        return TaskClock.getTime(self) * self.adjustmentFactor

    def wait(self,secs):
        return TaskClock.wait(self, secs / self.adjustmentFactor)


class Task (object):
    """The primary object representing a computer based test.


    """
    def __init__(self,configuration,environment=None,sessionConfig=None):
        self.name=''  #name of the task
        self.version=''  #version of the task
        self.versionDate='' #versionDate of the task
        self.environment=environment # runtime environment object
        if(self.environment==None):
            self.environment = lavatask.environment.Environment(configuration)
            self.environment.run()
        self.OS = self.environment.getOS()

        self.sessionConfig=sessionConfig #details of the subject, sessionnumber, etc.
        if(sessionConfig==None):
            self.subjectId=''
            self.sessionNum='1' #session number (supports longitudinal testing of same subject id)
            self.initials='' #field to support recording of initials (could be used to record the person administering the task or the subject)
            self.form = configuration.getTaskForm()
            self.ageCohort=configuration.getTaskAgeCohort()
            self.language=configuration.getTaskLanguage()
        else:
            self.subjectId=self.sessionConfig.subjectId
            self.sessionNum=self.sessionConfig.sessionNum
            self.initials=self.sessionConfig.initials
            self.form = self.sessionConfig.form
            self.ageCohort=self.sessionConfig.ageCohort
            self.language=self.sessionConfig.language

        if(self.language=='Chinese'):
            self.fontName=configuration.getChineseFontName(self.OS) # font name for instruction text
            self.fontSize=float(configuration.getChineseFontSize(self.OS)) # font size for instruction text
            self.fontCharsPerLine=int(configuration.getChineseFontCharsPerLine(self.OS)) # font chars per line for instruction text
        else:
            self.fontName=configuration.getFontName(self.OS) # font name for instruction text
            self.fontSize=float(configuration.getFontSize(self.OS)) # font size for instruction text
            self.fontCharsPerLine=int(configuration.getFontCharsPerLine(self.OS)) # font chars per line for instruction text

        self.sessionDate='' #the date (MM/DD/YYYY) the task was run
        self.sessionStartTime='' # the start time of the the task.
        self.sessionDateLong=''# the date and time the task was run--used for filenames (MM_DD_YYYY__HHh_MMm)
        self.clock=None  #overall task clock
        self.continueTask=True #flag to control whether to continue the task
        self.abortKeys=["escape"] #key(s) to check for aborting the task
        self.writeOnAbort=True #flag whether responses should be written upon aborting the task
        self.lavaTaskHome=configuration.getLavaTaskHome()
        self.dataPath=configuration.getDataPath()  # for storing data
        self.useSubjectFolders=True #Whether to store data in subject specific folders.
        self.outputCombinedSummary=True #Whether to output summary calculations into a combined file.
        self.logPath=configuration.getLogPath()  # for storing log output
        self.resourcePath=configuration.getResourcePath() #for locating stimuli, etc.

        self.logFile=None #a log file for the specific task execution
        self.window=None # the screen
        self.orientation = configuration.getDisplayOrientation()
        self.allowGUI=False # turn off GUI on windows.
        self.monitor=None # the monitor configuration
        self.monitorName="lavatask" #default monitor name
        self.blocks=[] #the blocks that make up the task (in order)
        self.nextBlock=None #used to control block execution -- Set to the name of the block that should run next.
        self.defaultResponseMonitor = ResponseMonitor(self)
        self.taskClockFactory = None #clock creator
        self.responses=TaskResponses(self) #the responses recorded during the task
        self.windowBackgrounds = {} #used because setting the window color is not a reliable way to draw the background color in psychopy

        self.recordScreenShots = False #flag to control recording of screenshots
        self.screenShotFormat = 'jpg' #default output format for screenshots
        self.hasScreenShots = False # used to track whether screenShots exist and should be saved

    def addBlock(self,block):
        """Adds block to the end of the block array."""
        self.blocks.append(block)

    def getBlockByName(self,blockName):
        """Returns first block that matches blockName or None."""
        for block in self.blocks:
            if(block.name == blockName):
                return block
        return None

    def getBlockByIndex(self,index):
        """Retrieves block by zero ordered index or None."""
        if len(self.blocks)>= index +1:
            return self.blocks[index]
        else:
            return None

    def setNextBlock(self,blockName):
        """Sets the name of the block that should execute next."""
        self.nextBlock = blockName

    def isTaskAborted(self):
        """Checks whether the user has requested task abort, and executes the abort."""
        if event.getKeys(self.abortKeys):
            return(self.abort())
        else:
            return False;

    def shouldContinue(self):
        """Checks whether the task should continue (e.g. has it been aborted)."""
        return (self.continueTask)

    def abort(self):
        """Executes any task specific onAbort code, and unless cancelled, marks the task as aborted."""
        if(self.doOnAbort()):
            self.continueTask=False
            logging.info("Task " + self.name + " aborted at " + str(self.getTime()))
            return True
        else:
            return False

    def doOnAbort(self):
        """Implement in subclasses to handle the abort event.

        return value: True=continue abort, False=cancel abort
        """
        return True


    def getTaskExecutionFileNamePart(self):
        """Returns the prefix for an output file based on the task execution data."""
        prefix = ''
        if(self.subjectId):
            prefix += self.subjectId + '_'
        if(self.sessionNum):
            prefix += self.sessionNum + '_'
        if(self.sessionDateLong):
            prefix += self.sessionDateLong
        return prefix

    def getDataOutputPath(self):
        if(self.useSubjectFolders):
            outputPath = os.path.join(self.dataPath,self.subjectId)
        else:
            outputPath = self.dataPath
        return outputPath


    def getFileName(self,directory,name,suffix):
        """Convenience function to combine filename parts."""
        return os.path.normpath(os.path.join(directory,name + '.' + suffix ))


    def getStandardOutputFileName(self,directory,suffix,prefix=None):
        """Returns the output filename using the standard conventions for the task execution

            [Name]_[Prefix]_[execution details].[Suffix]
        """
        name = self.name
        if(prefix):
            name += '_' + prefix
        name += '_' + self.getTaskExecutionFileNamePart()
        return self.getFileName(directory,name,suffix)


    def getReponseDetailFileName(self):
        """ gets the output filename for the detailed response record'"""
        return self.getStandardOutputFileName(self.getDataOutputPath(), 'csv')

    def getReponseSummaryFileName(self):
        """ gets the output filename for the summary record'"""
        return self.getStandardOutputFileName(self.getDataOutputPath(), 'csv', 'Summary')

    def getCombinedResponseSummaryFileName(self):
        """Returns the output filename for the combined summary statistics for the task

        default is to store this in the root of the data directory.

        """
        name = self.name + '_Summary_Combined_' + self.environment.getEnvironmentFileNamePart()
        return self.getFileName(self.dataPath,name,'csv')

    def setupOutputFolders(self):
        """Makes sure the output folder exists."""
        if not os.path.isdir(self.getDataOutputPath()):
            os.makedirs(os.path.normpath(self.getDataOutputPath())) #if this fails (e.g. permissions) we will get error
        if not os.path.isdir(self.logPath):
            os.makedirs(self.logPath)#if this fails (e.g. permissions) we will get error

    def openLogFile(self):
        """Creates a pyschopy log file for the task execution."""
        self.logFile = logging.LogFile(self.getStandardOutputFileName(self.logPath,"log"))
        logging.console.setLevel(logging.WARNING)#this outputs to the screen, not a file

    def createDefaultTaskMonitor(self):
        self.monitor = monitors.Monitor("lavatask")
        self.monitor.setSizePix(self.environment.getDisplayResolutionInPx())
        self.monitor.setWidth(self.environment.widthCm)

    def createDefaultTaskWindow(self):
        """Creates the basic psychopy window that will be used for stimuli display.  Override in subclasses as needed."""
        self.window = visual.Window(size=self.environment.getDisplayResolutionInPx(),fullscr=False, allowGUI=self.allowGUI, viewOri=self.orientation, units="cm", screen=self.environment.screen,monitor=self.monitor)


    def captureScreenShot(self):
        """get current window as screen shot"""
        if(self.recordScreenShots == True and self.window):
            self.window.getMovieFrame();
            self.hasScreenShots = True

    def saveScreenShots(self):
        """save the screen shots"""
        if (self.hasScreenShots == True and self.window):
            self.window.saveMovieFrames(os.path.normpath(os.path.join(self.logPath,self.name + "_" + self.sessionDateLong + '_' + self.subjectId + '_' + self.sessionNum + '.' + self.screenShotFormat)))
            #give things time to write our file buffers.
            self.wait(10)
    def drawBackgroundRGB(self,name,rgb):
        if(not name in self.windowBackgrounds.keys()):
            backgroundStim =  visual.PatchStim(win=self.window, tex='none',  color=rgb, colorSpace='rgb255', size=2,units='norm')
            self.addBackground(name,backgroundStim)
        backgroundStim = self.windowBackgrounds[name]
        if(backgroundStim != None):
            backgroundStim.draw()


    def drawBackground(self,background):
        if(not background in self.windowBackgrounds.keys()):
            backgroundStim =  visual.PatchStim(win=self.window, tex='none',  color=background, size=2,units='norm')
            self.addBackground(background,backgroundStim)

        backgroundStim = self.windowBackgrounds[background]
        if(backgroundStim != None):
            backgroundStim.draw()

    def addBackground(self,background,backgroundStim):
        self.windowBackgrounds.update({background:backgroundStim})


    def runTask(self):
        """Primary control routine.  Initializes, runs, and cleans up after the task."""
        self.initializeTask()
        self.doTask()
        self.doAfterTask()
        self.saveScreenShots()
        if(self.window):
            self.window.close()

    def initializeTask(self):
        """do all the work setting up the task prior to  doTask()"""
        self.resetClock()
        self.sessionDate = strftime("%m/%d/%Y")
        self.sessionStartTime = strftime("%H:%M")
        self.sessionDateLong = strftime("%m_%d_%Y_%Hh_%Mm")
        self.setupOutputFolders()
        self.openLogFile()
        if(self.monitor==None):
            self.createDefaultTaskMonitor()
        if(self.window==None):
            self.createDefaultTaskWindow()
        self.doBeforeTask()
        self.defaultResponseMonitor.initialize()


    def doTask(self):
        """Default task logic--iterates through blocks then writes out response and summary data"""
        for block in self.blocks:
            if(self.nextBlock == None or self.nextBlock == block.name):
                self.setNextBlock(None)
                if(not self.isTaskAborted()):self.doBeforeBlock(block)
                if(not self.isTaskAborted()):block.runBlock()
                if(not self.isTaskAborted()):self.doAfterBlock(block)
        if(self.responses):
            if(self.writeOnAbort or self.shouldContinue()):
                self.responses.writeResponses([self.getReponseDetailFileName()])
                summaryFiles = [self.getReponseSummaryFileName()]
                if(self.outputCombinedSummary):
                    summaryFiles.append(self.getCombinedResponseSummaryFileName())
                self.responses.writeSummaryStats(summaryFiles)



    def resetClock(self):
        """Resets the task clock to 0, creates clock if needed."""
        if(self.clock==None):
            if(self.taskClockFactory==None):
                self.taskClockFactory=TaskClockFactory()
            self.clock = self.taskClockFactory.createClock()
        else:
            self.clock.reset()
        self.defaultResponseMonitor.onResetClock('task')



    def wait(self,secs):
        """waits the number of seconds provided"""
        if(self.clock==None):
            self.resetClock()
        self.clock.wait(secs)

    def getTime(self):
        """Returns current time relative to task clock, creates clock if needed."""
        if(self.clock==None):
            self.resetClock()
        return self.clock.getTime()

    def refreshWindow(self):
        """Redraws primary task window.  Override in subclasses as needed."""
        if(self.window!=None):
            self.window.flip()

    def getTaskResponseFields(self):
        """Returns dictionary of task configuration and execution data for use in output files."""
        return {'task_name':self.name,'task_version':self.version,'task_versionDate':self.versionDate,'task_form':self.form,'task_ageCohort':self.ageCohort,
        'task_language':self.language,'site_id':self.environment.siteId,'subject_id':self.subjectId,'session_num':self.sessionNum,'initials':self.initials,'session_date':self.sessionDate,'session_start':self.sessionStartTime,'machine_id':self.environment.machineId}

    def getTaskResponseColumns(self):
        """Returns array of column names for task configuration and execution data for use in writing output files."""
        return ['task_name','task_version','task_versionDate','task_form','task_ageCohort','task_language','site_id','subject_id','session_num','session_date','session_start','initials','machine_id']

    def doBeforeTask(self):
        """Implement in subclasses to do anything that needs to be done before the task runs"""

    def doAfterTask(self):
        """Implement in subclasses to do anything that needs to be done after the task runs"""

    def doBeforeBlock(self,block):
        """Implement in subclasses to customize the task block execution (e.g. skip blocks based on runtime conditions)"""

    def doAfterBlock(self,block):
        """Implement in subclasses to customize the task block execution (e.g. skip blocks based on runtime conditions)"""



class Block(object):
    """Highest level of organizing unit within a task,typically displays stimuli and/or records responses.


    """

    def __init__(self,task,name):
        self.task=task#the parent task
        self.name=name #the block name
        self.continueBlock=True #flag whether to continue block execution
        self.blockClock=None #clock for the block (if needed)
        self.afterBlockDelay=None #amount of time to delay before running the block
        self.beforeBlockDelay=None #amount of time to delay after running the block


    def drawBackground(self,background):
        """Convenience function."""
        self.task.drawBackground(background)

    def drawBackgroundRGB(self,name,rgb):
        """Convenience function."""
        self.task.drawBackgroundRGB(name,rgb)

    def addBackground(self,background,backgroundStim):
        """Convenience function."""
        self.task.addBackground(background,backgroundStim)


    def runBlock(self):
        """Primary control routine for the block."""
        if(self.shouldContinue()): self.doBeforeBlockDelay()
        if(self.shouldContinue()): self.doBeforeBlock()
        if(self.shouldContinue()): self.doBlock()
        if(self.task.shouldContinue()): self.doAfterBlock()
        if(self.task.shouldContinue()): self.doAfterBlockDelay()

    def captureScreenShot(self):
        """record a screenshot of the window"""
        if(self.task):
            self.task.captureScreenShot()

    def doAfterBlockDelay(self):
        """Delay if the afterBlockDelay property is set."""
        if(self.afterBlockDelay!=None):
           self.wait(self.afterBlockDelay)

    def doBeforeBlockDelay(self):
        """Delay if the beforeBlockDisplay property is set."""
        if(self.beforeBlockDelay!=None):
           self.wait(self.beforeBlockDelay)

    def shouldContinue(self):
        """Checks whether the block should continue and if the task has been aborted."""
        return (self.continueBlock and self.task.shouldContinue())

    def setContinue(self,shouldContinue):
        """Sets the continueBlock property to the shouldContinue parameter."""
        self.continueBlock=shouldContinue

    def doBlock(self):
        """Implement in subclasses to do the work of the block."""

    def doBeforeBlock(self):
        """Implement in subclasses to take action before the block runs."""

    def doAfterBlock(self):
        """Implement in subclasses to take action after the block runs."""

    def resetClock(self):
        """Resets the block clock to 0, creates clock if needed."""
        if(self.blockClock==None):
            if(self.task.taskClockFactory==None):
                self.task.taskClockFactory=TaskClockFactory()
            self.blockClock=self.task.taskClockFactory.createClock()
        else:
            self.blockClock.reset()
            self.responseMonitor().onResetClock('block')

    def wait(self,secs):
        """waits for the number of seconds"""
        if(self.blockClock==None):
            self.resetClock()
        self.blockClock.wait(secs)


    def getTime(self):
        """Returns current time relative to block clock, creates clock if needed."""
        if(self.blockClock==None):
            self.resetClock()
        return self.blockClock.getTime()

    def getBlockResponseFields(self):
        """Returns dictionary of block configuration and execution data for use in output files."""
        return {'block_name':self.name}

    def getBlockResponseColumns(self):
        """Returns array of column names for block configuration and execution data for use in writing output files."""
        return ['block_name']


class ResponseBlock(Block):
    """A Block that waits for user input"""
    def __init__(self,task,name,keys=None):
        Block.__init__(self,task,name)
        self.responseKeys=keys #the response keys to capture format is ['key','key'], e.g. ['a','b','left']
        self.lastResponse=None #variable to hold the last response keys
        self.lastResponseTime=None #variable to hold the time of the last response
        self.lastResponseDevice=None #variable to hold the description of the last responses device (e.g.  mouse,  keyboard).
        self.responseEnabled=True #flag to enable/disable response checking (e.g. can wait before accepting reponses)
        self.blockTimeout = None #if the response period is time limited, set this to the time (relative to the block clock) that the block will timeout
        self.blockResponseMonitor = None #variable to hold a responseMonitor object specific to the block.

    def checkResponse(self):
        """Checks for user input that matches the configured response keys.

        Implementation is delegated to a ResponseMonitor.
        """
        return self.responseMonitor().checkResponse(self)

    def responseMonitor(self):
        """get the response monitor for the block"""
        if(self.blockResponseMonitor == None):
            return self.task.defaultResponseMonitor
        else:
            return self.blockResponseMonitor

    def enableResponse(self):
        """Enables response checking."""
        self.responseEnabled=True

    def disableResponse(self):
        """Disables response checking"""
        self.responseEnabled=False

    def clearResponseBuffer(self):
        """clears any responses queued in the response buffer"""
        return self.responseMonitor().clearResponseBuffer()

    def checkTimeout(self):
        """Checks whether the block has timed out if the blockTimeout property is set and the blockClock is running.

        Returns true if the block has timed out.
        """
        if(self.blockClock!=None and self.blockTimeout != None and self.blockTimeout <= self.getTime()):
            return True
        else:
            return False

    def doTimeout(self):
        """Implement in subclasses to take action when a block timeout happens."""

    def doBlock(self):
        """Primary response block execution routine.

        Loops checking for a response, and checking for block timeout.  When response is detected
        the block is discontinued and the doAfterResponse() method is called.  Otherwise, on each
        interation of the loop calls the doBeforeResponse() method.  These two methods should be
        implemented as needed in subclasses to do the specific work of the block.
        """

        while(self.shouldContinue()):
            if(self.checkTimeout()):
                self.setContinue(False)
                self.doTimeout()
            elif(self.checkResponse()):
                self.setContinue(False)
                self.doAfterResponse()
            elif(not self.task.isTaskAborted()):
                #event.clearEvents()
                self.doBeforeResponse()

    def doBeforeResponse(self):
        """Implement in subclasses to take action before the user provides a response (e.g display stimuli)."""

    def doAfterResponse(self):
        """Implement in subclasses to take action after the user provides a response (e.g. check response for correctness)."""


class ResponseMonitor(object):
    """Encapsulates the response monitoring for a task.

    Using this class as a "plugin" response monitor allows for easier unit testing of
    the tasks.   For a unit test create a subclass of ResponseMonitor to provide
    automated responses as the task runs.   In the test case, simply replace the
    standard response monitor with the testing response monitor.

    """
    def __init__(self,task):
        self.task = task


    def onResetClock(self,clockId):
        """perform actions on resetClock events.

        This enables response monitors with internal timers (e.g. response boxes) to
        encapusualte the timing mechanism and return response time relative to the external
        clocks.

        """

    def initialize(self):
        """Perform any initialization needed for the response monitor.

        Called before task begins.
        """
        return

    def clearResponseBuffer(self):
        """clear the response buffer"""
        event.clearEvents()


    def checkResponse(self,block):
        """Checks for user input that matches the configured response keys for the block.

        Returns true if a matching response was input.
        """
        if(block.responseEnabled==False):
            event.clearEvents()
            return False

        if(block.responseKeys==None):
            block.lastResponse=event.getKeys()
        else:
            block.lastResponse=event.getKeys(block.responseKeys)

        if(block.lastResponse==None or len(block.lastResponse)==0):
            return False
        else:
            block.lastResponse = block.lastResponse[0]
            block.lastResponseTime = block.getTime()
            block.lastResponseDevice= 'keyboard'
            return True


class MouseResponseMonitor(ResponseMonitor):
    """Implemented response monitoring for mouse keypresses

    """
    def __init__(self,task,showMouse=False,leftValue="left",middleValue="middle",rightValue="right"):
        ResponseMonitor.__init__(self,task)
        self.leftValue = leftValue
        self.middleValuue = middleValue
        self.rightValue = rightValue
        self.showMouse = showMouse
        self.mouse = None
        self.mouseState = MouseState() #used to track time of mouse button presses last time check response was called.

    def initialize(self):
        self.mouse = event.Mouse(self.showMouse,None,self.task.window)
        self._resetClickTracking()

    def checkKeyboardResponse(self,block):
        return ResponseMonitor.checkResponse(self,block)

    def _resetClickTracking(self):
        """handle resetting all the mechanisms used to track mouse clicks"""
        if(self.mouse!=None):
            self.mouse.clickReset()
            self.mouseState.clearState()
            #print "in _resetClickTracking " + str(self.task.getTime())

    def getLastMouseClicks(self):
        """gets the most recent mouse click times prior to resetting"""
        if(self.mouse):
            buttons, times = self.mouse.getPressed(True)
            return MouseState(times,buttons)
        else:
            return False

    def getNewMouseClicks(self):
        """abstracts the underlying mouse monitoring, so you only get "new" mouse clicks reported.
           getPressed Methods()
        """
        if(self.mouse):
           buttons, times = self.mouse.getPressed(True)
           if(self.mouseState.isStateChanged(times, buttons)):
               #print "buttons="+str(buttons)+ " times=" + str(times)
               #print self.mouseState.asString()
               self.mouseState.setState(times, buttons)
               return self.mouseState
        return False


    def onResetClock(self,clockId):
        self._resetClickTracking()

    def clearResponseBuffer(self):
        """clear the response buffer"""
        event.clearEvents('mouse')
        self._resetClickTracking()


    def checkResponse(self,block):
        """
        """
        if(block.responseEnabled==False):
            self.clearResponseBuffer()
            return False
        response = False

        mouseState = self.getNewMouseClicks()
        if(mouseState):
            if(mouseState.left and not mouseState.middle and not mouseState.right):
                block.lastResponse = self.leftValue
                block.lastResponseTime = block.getTime()
                block.lastResponseDevice = 'mouse'
                response = True
            elif(mouseState.middle and not mouseState.left and not mouseState.right):
                block.lastResponse = self.middleValue
                block.lastResponseTime = block.getTime()
                block.lastResponseDevice = 'mouse'
                response = True
            elif(mouseState.right and not mouseState.left and not mouseState.middle):
                block.lastResponse = self.rightValue
                block.lastResponseTime = block.getTime()
                block.lastResponseDevice = 'mouse'
                response = True

        return response


class MouseState(object):
    """This is a class to wrap the state of the mouse at a given time.  Used to track mouse clicks.

        Kind of a kludge, but it makes the rest of the code cleaner to maintain.

    """
    def __init__(self,times=[0.0,0.0,0.0],buttons=[0,0,0]):
        self.left = False  # whether left button was clicked
        self.middle = False #whether middle button was clicked
        self.right = False # whether right botton was clicked
        self.left_time = 0.0
        self.middle_time = 0.0
        self.right_time = 0.0

        self.setState(times, buttons)

    def clearState(self):
        """ resets the state"""
        self.setState([0.0,0.0,0.0], [0,0,0])

    def setState(self,times,buttons):
        """Set the state of the mouse based on the buttons and times array from mouse.getPressed(True)"""

        self.left = False
        self.middle = False
        self.right = False
        self.left_time = times[0]
        self.middle_time = times[1]
        self.right_time = times[2]

        if(self.left_time != 0.0 or buttons[0]!=0):
            self.left = True
        else:
            self.left = False

        if(self.middle_time != 0.0 or buttons[1]!=0):
            self.middle = True
        else:
            self.middle

        if(self.right_time != 0.0 or buttons[2]!=0):
            self.right = True
        else:
            self.right = False



    def isStateChanged(self,times=[0.0,0.0,0.0],buttons=[0,0,0]):
        """ is the state stored in the object different that that represented by the times / buttons passed in"""
        s = MouseState(times,buttons)
        if(s.left != self.left or s.middle!=self.middle or s.right!=self.right or
           s.left_time != self.left_time or s.middle_time != self.middle_time or s.right_time!=self.right_time):
            return True
        else:
            return False

    def hasClick(self):
        return (self.left or self.middle or self.right)

    def asString(self):
        print("Left:"+str(self.left)+"["+str(self.left_time)+"];"+"Middle:"+str(self.middle)+"["+str(self.middle_time)+"];"+"Right:"+str(self.right)+"["+str(self.right_time)+"];") #added brackets at the end

class RangeResponseMonitor(MouseResponseMonitor):
    """Class that implements ranges on the screen that may be selected as a response.

        Extends MouseResponseMonitor and is intended for use when keyboard is not
        available or desired.   Will check keyboard for key presses if requested.

    """
    def __init__(self,task,showMouse=False,left=True,keyboard=False,right=False,middle=False):
        MouseResponseMonitor.__init__(self,task,showMouse)
        self.monitorLeft = left #whether to monitor "left" mouse clicks
        self.monitorRight = right #whether to monitor "right" mouse clicks
        self.monitorMiddle = middle #whether to monitor "middle" mouse clicks
        self.monitorKeyboard = keyboard # whether to monitor the keyboard.
        self.enabledRanges = {} #dictionary for ranges that are enabled
        self.disabledRanges = {} #dictionary for ranges that are disabled

    def addRange(self,name,pos,size,enabled=True,buttons=['left']):
        """Add a named range to the monitor"""

        range = ResponseRange(name,pos,size,buttons)

        if(enabled):
            self.enabledRanges[name]=range
            if(name in self.disabledRanges.keys()):
                self.disabledRanges.pop(name)
        else:
            self.disabledRanges[name]=range
            if(name in self.enabledRanges.key()):
                self.disabledRanges.pop(name)

    def removeRange(self,name):
        """remove a named range from the monitor"""
        if(name in self.enabledRanges.keys()):
            self.enabledRanges.pop(name)
        if(name in self.disabledRanges.keys()):
            self.disabledRanges.pop(name)

    def addRangeFromStim(self,name,stim,enabled=True,buttons=['left']):
        """Use the pos and size of the stim."""
        self.addRange(name,stim.pos, stim.size, enabled, buttons)

    def enableRange(self,name):
        """enable response monitoring for a named range"""
        if(name in self.enabledRanges.keys()):
            return
        if(name in self.disabledRanges.keys()):
            self.enabledRanges[name] = self.disabledRanges.pop(name)

    def disableRange(self,name):
        """disabled response monitoring for a named range"""
        if(name in self.disabledRanges.keys()):
            return
        if(name in self.enabledRanges.keys()):
            self.disabledRanges[name] = self.enabledRanges.pop(name)

    def enableAll(self):
        """enable all ranges"""
        self.enableRanges(self.disabledRanges.keys())


    def disableAll(self):
        """disable all ranges"""
        self.disableRanges(self.enabledRanges.keys())

    def removeAll(self):
            self.enabledRanges.clear()
            self.disabledRanges.clear()

    def enableRanges(self,rangeNames):
        """enable the ranges provided"""
        for name in rangeNames:
            self.enableRange(name)

    def disableRanges(self,rangeNames):
        """disable the ranges provided"""
        for name in rangeNames:
            self.disableRange(name)

    def removeRanges(self,rangeNames):
        """remove ranges for the names provided"""
        for name in rangeNames:
            self.removeRange(name)


    def getResponseFromPos(self,button,pos,all=True):
        """Checks for a positional match between pos and all enabled ranges for the specified button.

            If all=True (the default), all ranges matched will be returned in an array
            e.g. [range1name,range2name,range3name].  If just one range is matched, then
            the return will just be the name of that range.

        """
        responses = []
        for range in self.enabledRanges.values():
            if (range.monitorsButton(button) and range.isPosInRange(pos)):
                responses.append(range.name)
        if(len(responses)==0):
            return False
        elif(len(responses)==1):
            return responses[0]
        else:
            return responses


    def checkResponse(self,block):
        """Check for a response.

            Checks the position of the mouse / touch and then
            looks to see if left,right, or middle "buttons"
            are pressed returning the first response in that
            order.

        """
        if(block.responseEnabled==False):
            self.clearResponseBuffer()
            return False

        response = False
        mouseState = self.getNewMouseClicks()
        if(mouseState):

            if(mouseState.hasClick()):
                print (mouseState.asString()) #added brackets at end
                pos = self.mouse.getPos()
                if(self.monitorLeft and mouseState.left):
                    response = self.getResponseFromPos('left',pos)
                    if(response != False):
                        block.lastResponse = response
                        block.lastResponseTime = block.getTime()
                        block.lastResponseDevice = 'range'

                elif(self.monitorRight and mouseState.right):
                    response = self.getResponseFromPos('right',pos)
                    if(response != False):
                        block.lastResponse = response
                        block.lastResponseTime = block.getTime()
                        block.lastResponseDevice = 'range'

                elif(self.monitorMiddle and mouseState.middle):
                    response = self.getResponseFromPos('middle',pos)
                    if(response != False):
                        block.lastResponse = response
                        block.lastResponseTime = block.getTime()
                        block.lastResponseDevice = 'range'


        if(response):
            return True
        return False

    def checkKeyboardResponse(self,block):
        """Use standard keyboard checking functionality if requested"""
        if(self.monitorKeyboard == True):
           return ResponseMonitor.checkResponse(self,block)
        else:
            return False

class ResponseRange(object):
    """A wrapper around the properties we need to manage for ranges used with the RangeResponseMonitor.
    """
    def __init__(self,name,pos=None,size=None,buttons=None):
        self.pos = None #center of the range in window units[x,y]
        self.size = None #size of the name in window units [x,y]
        self.buttons = buttons #which buttons to monitor for this range
        self.name = name #name for the range
        self.top = None
        self.bottom = None
        self.right = None
        self.left = None
        self.setPos(pos)
        self.setSize(size)


    def _calcCoords(self):
        """Determine the top left and bottom right coordinates in window units"""
        if(self.pos != None and self.size != None):
            self.top = self.pos[1] + round(self.size[1] / 2.00,2)
            self.bottom = self.pos[1] - round(self.size[1] / 2.00,2)
            self.left = self.pos[0] - round(self.size[0] / 2.00,2)
            self.right = self.pos[0] + round(self.size[0] / 2.00,2)
           # print self.name + ": top="+str(self.top)+ ",bottom="+str(self.bottom)+",left="+str(self.left)+",right="+str(self.right)

    def isPosInRange(self,pos):
        """Method to check whether the position given is within the range"""

        #First make sure coordinates are calculated
        if(self.top == None):
            self._calcCoords()
        if(self.top == None):
            return False

        if(pos[0]>=self.left and pos[0]<=self.right
           and pos[1] >= self.bottom and pos[1] <= self.top):
           print ("isPosInRange == True (pos=" + str(pos) + ", range=" + self.name + ")") #added brackets at end
           return True
        return False

    def monitorsButton(self,button):
        """method to check whether the particular button is monitored for this range."""
        if(self.buttons != None):
            return (button in self.buttons)
        return False

    def setPos(self,pos):
        """method to set the position, recalcs internal coords"""
        self.pos = pos
        self._calcCoords()

    def setSize(self,size):
        """method to set the size, recalcs internal coords"""
        self.size = size
        self._calcCoords()


class CedrusResponseMonitor(ResponseMonitor):
    """Implemented response monitoring for cedrus RB response box

    """
    def __init__(self,task,responseDevice,port,buttonMap = {1:'left',2:'right'}):
        ResponseMonitor.__init__(self,task,responseDevice)
        self.buttonMap = buttonMap
        print (self.buttonMap)
        self.watchedButtons = buttonMap.keys()
        print (self.watchedButtons)
        self.port = port
        self.cedrus = cedrus.RB730 (self.port)
        print (self.cedrus.getInfo())
        print (self.cedrus.measureRoundTrip())

    def initialize(self):
        return


    def clearResponseBuffer(self):
        """clear the response buffer"""
        self.cedrus.clearBuffer()


    def checkKeyboardResponse(self,block):
        return ResponseMonitor.checkResponse(self,block)


    def onResetClock(self,clockId):
        if(self.cedrus):
            if(clockId == 'task'):
                self.cedrus.resetBaseTimer()
                self.cedrus.resetTrialTimer()
            elif(clockId == 'block'):
                self.cedrus.resetTrialTimer()

    def checkResponse(self,block):
        """
        """
        if(block.responseEnabled==False):
            self.cedrus.clearBuffer()
            return False

        keyEvents = self.cedrus.getKeyEvents(self.watchedButtons,True)
        keyTime = None
        for evt in keyEvents:
            #just take earliest key event - if the key following the first key has the same timestamp then discard as multiple
            if(keyTime==None):
                block.lastResponse = self.buttonMap[evt.key]
                print ("evt.rt:" + str(evt.rt))
                block.lastResponseTime = evt.rt / 1000.0000
                keyTime = evt.rt
                block.lastResponseDevice = 'cedruspad'
            elif(keyTime ==evt.rt):
                block.lastResponse = 'multiple'
                block.lastResponseTime = evt.rt / 1000.0000
                block.lastResponseDevice = 'cedruspad'

        if(block.lastResponse==None or len(block.lastResponse)==0):
            return False
        else:
            return True

class TrialResponseBlock(ResponseBlock):
    """A ResponseBlock that iterates over a set of response trials.

    """
    def __init__(self,task,name,keys=None,trialData=None):
        ResponseBlock.__init__(self,task,name,keys)
        self.trialData = trialData  #the trial configuration data
        self.trialHandler=None # the trial handler (see psychopy.data.TrialHandler)

        self.continueTrial=True #flag whether to continue the trial
        self.trialTimeout=None #if the trial is time limited, set this to the time (relative to the trial clock) that the trial will timeout
        self.afterTrialDelay=None #amount of time to delay after running the trial
        self.beforeTrialDelay=None #amount of time to delay before running the trial

        self.currentTrial=None # the current trial
        self.currentTrialNum=0 # the current trial number within the block

    def doAfterTrialDelay(self):
        """Delay if the afterTrialDelay property is set."""
        if(self.afterTrialDelay!=None):
           self.wait(self.afterTrialDelay)

    def doBeforeTrialDelay(self):
        """Delay if the beforeTrialDelay property is set."""
        if(self.beforeTrialDelay!=None):
           self.wait(self.beforeTrialDelay)


    def shouldContinueTrial(self):
        """Checks whether the trial should continue and if the block or task has been aborted."""
        return (self.continueTrial and self.continueBlock and self.task.shouldContinue())

    def setContinueTrial(self,shouldContinue):
        """Sets the continueTrial property to the shouldContinue parameter."""
        self.continueTrial=shouldContinue

    def doBeforeBlock(self):
        """Extends base block functionality to call trial specific event methods."""
        if(self.shouldContinue()): self.doBeforeTrialBlock()
        if(self.shouldContinue()): self.doBeforeTrialDelay()
        if(self.shouldContinue()): self.doBeforeTrial()

    def doBeforeResponse(self):
        """Extends base block functionality to handle trial iterations.

        If current trial times out, then end the trial and setup the next, otherwise do
        trial specific "before response" event .
        """
        if(self.checkTrialTimeout()):
            self.doTrialTimeout()
            self.doAfterTrial()
            self.doAfterTrialDelay()
            self.doBeforeTrialDelay()
            self.doBeforeTrial()
        elif(self.shouldContinue()):
            self.doBeforeTrialResponse()

    def doAfterResponse(self):
        """Extends base block functionity to enable iterating to the next trial after a response."""
        self.setContinue(True) #the default response check in the superclass will end the block, so turn that off
        self.setContinueTrial(False)
        if(self.shouldContinue()):self.doAfterTrialResponse()
        if(self.shouldContinueTrial()==False):
            if(self.shouldContinue()):self.doAfterTrial()
            if(self.shouldContinue()): self.doAfterTrialDelay()
            if(self.shouldContinue()): self.doBeforeTrialDelay()
            if(self.shouldContinue()):self.doBeforeTrial()

    def doBeforeTrialBlock(self):
        """Implement in subclasses to take action before the trials run (e.g. initialize stimuli, load trial data)"""

    def doBeforeTrial(self):
        """Implement in subclasses to take action before each trial runs"""

    def checkTrialTimeout(self):
        """Checks whether the trial has timed out if the trialTimeout property is set and the trialClock is running.

        Returns true if the trial has timed out.
        """
        if(self.blockClock!=None and self.trialTimeout != None and self.trialTimeout <= self.getTime()):
            return True
        else:
            return False

    def doTrialTimeout(self):
        """Implement in subclasses to take action when a trial timeout happens (e.g. create 'no reponse' record in output."""

    def doBeforeTrialResponse(self):
        """Implement in subclasses to take action before a response is provided (e.g. draw stimuli)"""

    def doAfterTrialResponse(self):
        """Implement in subclasses to take action after a trial response is given (e.g. check correctness and record response)"""

    def doAfterTrial(self):
        """Implement in subclasses to take action after each trial is completed"""

    def getTrialsFromTrialHandler(self,handler):
        """Utility method to get trials from TrialHandler as an array of trialdata"""
        trials = []
        try:
            # get next trial data
            while(1):
                trials.append(handler.next())
        except StopIteration:  #no more trials
            return trials



class SlideshowBlock(ResponseBlock):
    """A ResponseBlock that displays a series of slides.

    Standard controls for slideshow
        space = go forward
        left arrow = go back
        right arrow=go forwards

    """
    def __init__(self,task,name,keys=["space","left","right"]):
        ResponseBlock.__init__(self,task,name,keys)
        self.slides=[] # array of stimuli to display (in order of appearance)
        self.slideAdvanceTimeout=None # auto advance slides if set (in seconds)
        self.currentSlideIndex=-1 #array index of the current slide
        self.currentSlide=None
        self.bufferSize=1 #number of slides +/- the current slide to load and keep in memory.
        self.currentBufferIndex=-1 #used to track slide changes relative to the buffer

    def doBeforeBlock(self):
        """Initialize clock if slide advancing is turned on."""
        if(self.slideAdvanceTimeout!=None):
            self.resetClock()
        self.nextSlide()
        self.bufferSlides()
        self.enableResponse()


    def doTimeout(self):
        """Advance the slide"""
        self.setContinue(True)
        self.nextSlide()

    def slideTimeout(self):
        """Check whether the slide timeout has been reached."""
        if(self.slideAdvanceTimeout!=None):
            if(self.getTime()>=self.slideAdvanceTimeout):
                return True
        return False

    def nextSlide(self):
        if(self.currentSlide != None):
            self.currentSlide.stop();

        self.currentSlideIndex += 1
        if(self.currentSlideIndex < len(self.slides)):
            self.currentSlide = self.slides[self.currentSlideIndex];
            if(self.currentSlide!=None):
                self.setContinue(True)
                self.resetClock()
                return

        self.setContinue(False)

    def priorSlide(self):
        if(self.currentSlide != None):
            self.currentSlide.stop();

        if(self.currentSlideIndex >=1):
            self.currentSlideIndex -= 1
            self.currentSlide = self.slides[self.currentSlideIndex];
            if(self.currentSlide!=None):
                self.resetClock()
        self.setContinue(True)  # do not end when the user tries to go back past the first slide.

    def doBeforeResponse(self):
        """play current slide."""
        self.currentSlide.start();
        self.bufferSlides()
        if(self.slideTimeout()):
            self.doTimeout()

    def bufferSlides(self):

        if(self.currentBufferIndex==self.currentSlideIndex):
            return
        else:
            self.currentBufferIndex=self.currentSlideIndex

        for i in range(len(self.slides)):
            slide = self.slides[i]
            if(slide != None and (i < (self.currentSlideIndex - self.bufferSize) or i > (self.currentSlideIndex + self.bufferSize))):
                slide.unload()
            else:
                slide.load()


    def doAfterResponse(self):
        """Move slide forward or back based on response provided"""
        self.clearResponseBuffer() #limits accidental advances
        if(self.lastResponse!=None):
            if(self.lastResponse=="left"):
                self.priorSlide()
            elif(self.lastResponse == "right" or self.lastResponse == "space"):
                self.nextSlide()

class SlideshowSlide(object):
    """A class that encapsulates slide functionality

    """
    def __init__(self,slideshow):
        """Initialize"""
        self.slideshow = slideshow
        self.loaded = False
        self.started = False
        self.done = False

    def load(self):
        """Do anything needed to prepare for playing the slide (e.g. create stimuli)."""
        if(self.loaded==False):
            self.doLoad()
            self.loaded = True

    def doLoad(self):
        """Do anything needed to prepare for playing the slide (e.g. create stimuli)."""

    def unload(self):
        if(self.loaded):
            self.doUnload()
            self.loaded = False;

    def doUnload(self):
        """Do anything needed to cleanup after the slide plays."""

    def captureScreenShot(self):
        """capture a screenshot of the window"""
        if(self.slideshow):
            self.slideshow.captureScreenShot()

    def start(self):
        if(self.done == False):
            if(self.doStart()):
                self.done = True
                self.captureScreenShot()

    def doStart(self):
        """start/play the slide. return true when done """

    def stop(self):
        self.doStop()
        self.done = False # this resets the slide so it can be played again if revisited.

    def doStop(self):
        """stop the slide"""

class InstructionBlock(ResponseBlock):
    """A ResponseBlock that displays textual instructions.

    """
    def __init__(self,task,name,keys=None,foreground="Black",background="White"):
        ResponseBlock.__init__(self,task,name,keys)
        self.text='' # text for the instruction block
        self.pos=[0,0]
        self.instructions=None; #stimlus property
        self.blockTimeout=300.0 #set default timeout for instructions to 5 minutes
        self.drawStage = 0 #enables more effecient drawning of stimuli (draw once)
        self.stims = [] # additional stims to draw.
        self.background=background
        self.foreground=foreground
        self.clearForegroundOnResponse = True # whether to "clear" the screen after the response.
        self.delayBeforeEnableResponse = 1.0 # minimum time to display instructions.
    def doBeforeBlock(self):
        """Initializes stimulus and clock."""
        if(self.instructions==None):
            self.instructions = self.createDefaultInstructionStimuli()
        self.resetClock()
        self.clearResponseBuffer()
        self.disableResponse()

    def doTimeout(self):
        """Abort the task when an instruction block times out."""
        self.task.abort()

    def doBeforeResponse(self):
        """Displays instructions."""
        if(self.drawStage == 0):
            self.drawBackground(self.background)
            for stim in self.stims:
                stim.draw()
            self.instructions.draw()
            self.task.refreshWindow()
            self.captureScreenShot()
            self.drawStage = 1
        if(self.drawStage == 1 and self.getTime() > self.delayBeforeEnableResponse):
            self.enableResponse()

    def doAfterResponse(self):
        """draw blank background"""
        if(self.clearForegroundOnResponse == True):
            self.drawBackground(self.background)
            self.task.refreshWindow()

    def createDefaultInstructionStimuli(self):
        """Creates a default Instruction Stimuli using the text property."""
        return visual.TextStim(win=self.task.window, ori=0,text=self.text,pos=self.pos,\
            alignHoriz = 'center',alignVert='center',font=self.task.fontName,height=self.task.fontSize,color=self.foreground,wrapWidth=50)

    def addStim(self,stim):
        self.stims.append(stim)



class TaskResponses(object):
    """Collection of responses recorded during a task with functionality for writing to output files.

    """
    def __init__(self,task):
        self.count = 0 #number of response records
        self.task = task # the parent task
        self.data = [] #response data (an array of dictionary objects)
        self.responseColumns=None #the columns (in order) of the response data.  Used to write out header row in output files
        self.hasResponses=False #whether any responses have been added.
    def addResponse(self,response):
        """Append the response (a dictionary) to the end of the data collection."""
        if(self.responseColumns==None):
            self.responseColumns=response.getResponseColumns()
        self.data.append(response.getResponseFields())
        self.count += 1
        self.hasResponses=True



    def writeResponses(self,filenames):
        """write all responses out to the filenames supplied to the method."""
        if(not self.hasResponses):
            return False

        for filename in filenames:
            responseWriter =  DictWriter(open(filename, 'w'),self.responseColumns ,extrasaction='ignore')
            responseWriter.writerow(dict(zip(self.responseColumns,self.responseColumns)))
            responseWriter.writerows(self.data)
            logging.info ('saved data to '+filename)

        return True
    def writeSummaryStats(self,filenames):
        """Write summary statistics out to the filenames supplied to the method.

        Generation of summary stats is deferred to subclassses that should implement the
        getSummaryStatsColumns and getSummaryStatsFields() methods.
        """

        if(not self.hasResponses):
            return False
        columns = self.getSummaryStatsColumns()
        dataFields = self.getSummaryStatsFields()
        responseWriter = None
        for filename in filenames:
            if(not os.path.isfile(filename)):  #summary file does not exist.  Create and write headers
                responseWriter =  DictWriter(open(filename, 'w'),columns ,extrasaction='ignore')
                responseWriter.writerow(dict(zip(columns,columns)))
            else: #just open for appending if it exists
                responseWriter =  DictWriter(open(filename, 'w'),columns ,extrasaction='ignore')
            responseWriter.writerow(dataFields)

        return True

    def getSummaryStatsColumns(self):
        """Implement in subclasses to return stat column names for the task

        Note: make sure to call TaskResponses.getSummaryStatsColumns() from the
        subclass to get the base columns array. Append the new columns to that array and return.

        """
        return self.task.getTaskResponseColumns()

    def getSummaryStatsFields(self):
        """Implement in subclasses to return summary stat data for the task

        Note: make sure to call TaskResponses.getSummaryStatsFields() from the
        subclass to get the base fields dictionary.  Update the dictionary with new values and return.

        """
        return self.task.getTaskResponseFields()

    def calcCorrect(self,values,noCalcValue=0):
        """Calculate the number of correct responses. """
        return len(values)

    def calcMean(self,values,noCalcValue=-5):
        """Calculate the mean of the values array passed to the method, returnng noCalcValue if Mean cannot be calculated."""
        if(len(values)==0):
            return noCalcValue
        return round(mean(values),4)

    def calcMedian(self,values,noCalcValue=-5,excludeOutliers=True):
        """Calculate the median of the values array passed to the method, optionally excluding outlier values, returning noCalcValue if Median cannot be calculated."""
        if(len(values)==0):
           return noCalcValue

        # exclude any values more than 3 stdev from the mean.
        if(excludeOutliers):
            meanValue = self.calcMean(values,noCalcValue)
            if(meanValue == noCalcValue):
                return noCalcValue
            stDevValue = self.calcStDev(values, noCalcValue)
            if(stDevValue == noCalcValue):
                return noCalcValue
            floor = meanValue - (stDevValue * 3.0000)
            ceiling = meanValue + (stDevValue * 3.0000)
            valuesNoOutliers = []
            for value in values:
                if(value >= floor and value <= ceiling):
                    valuesNoOutliers.append(value)
            return round(median(valuesNoOutliers),4)
        else:
            return round(median(values),4)




    def calcStDev(self,values,noCalcValue=-5):
        """Calculate the standard deviation of the values array passed to the method, returning noCalcValue if StDev cannot be calculated."""
        if(len(values)==0):
           return noCalcValue
        return round(std(values),4)


class TrialResponse(object):
    """A utility class for recording trial reponses during a task.

    """
    def __init__(self):
        self.responseDevice='keyboard' #the response device used (e.g. keyboard, mouse,cedruspad)
        self.block=None # the block of the response
        self.trialNum=None # the trial number within the block
        self.trialData=None #the trial configuration data
        self.key=None # the trial key response
        self.corr=None#was the subj correct this trial?
        self.rt=None#response time
        self.taskTime=None# total task time elapsed

    def getResponseFields(self):
        """Compiles fields from task, block, and response into a single data dictionary.

        Subclasses can implement the getTrialConfigurationFields() to record the trial specific
        configuration data.
        """
        fields = self.block.task.getTaskResponseFields()
        fields.update(self.block.getBlockResponseFields())
        fields.update({'response_device':self.responseDevice,'block_trial':self.trialNum,'resp_value':self.key,'resp_corr':self.corr,'resp_rt':self.rt,'task_time':self.taskTime})
        fields.update(self.getTrialConfigurationFields())
        return fields

    def getResponseColumns(self):
        """Compiles column names for the response data from task, block, and response into a single array.

        Subclasses can implement the getTrialConfigurationColumns() to include the trial specific
        configuration column names.
        """
        columns = self.block.task.getTaskResponseColumns()
        columns.append('response_device')
        for column in self.block.getBlockResponseColumns():
            columns.append(column)
        for column in self.getTrialConfigurationColumns():
            columns.append(column)
        for column in ['resp_value','resp_corr', 'resp_rt','task_time']:
            columns.append(column)
        return columns

    def getTrialConfigurationFields(self):
        """Implement in subclasses to report the specific trial configuration fields in the response data"""

    def getTrialConfigurationColumns(self):
        """Implement in subclasses to report the column names of the specific trial configuration fields """



class Resource(object):
    """Generic class functionality for locating and loading resources.

        The class attempts to locate a resource using a subfolder structure that
        supports different resources depending on the ageCohort and form of the task.
        It looks for a resource of the given name in progressively less specific folder
        locations until it finds the resource.
    """
    def __init__(self,name=None,task=None):
        self.name=name #name of the file to use for the resource
        self.searchPaths=None #paths to search for the resource
        self.task=task #reference to a task object
        self.data=None # the data loaded from the resource files
        self.loaded=False #whether the data has been loaded from the resource
        self.foundLocation=None #the location where the resource has been found

        if(task!=None):
            self.setupStandardTaskSearchPaths()


    def setupStandardTaskSearchPaths(self):
        if(self.task != None):
            self.addFolderToSearchPaths(self.task.resourcePath)
            if(self.task.ageCohort!=None):
                self.addFolderToSearchPaths(self.task.ageCohort.lower())
            if(self.task.form!=None):
                self.addFolderToSearchPaths(self.task.form.lower())
            if(self.task.language!=None):
                self.addFolderToSearchPaths(self.task.language.lower())


    def addFolderToSearchPaths(self,folder):
        """Add folders to the search paths.  By default, take the new folder and look for it in each level of the current search path structure"""
        if(self.searchPaths==None):
            self.searchPaths=[]
            self.searchPaths.append(folder)
        else:
            newPaths = []
            for path in self.searchPaths:
                newPaths.insert(0,path)
                newPaths.insert(0,os.path.normpath(os.path.join(path,folder)))
            self.searchPaths=newPaths


    def load(self):
        """Load the resource data, default implementation is to simply read the file"""
        if(not self.loaded):
            self.findResourceLocation()
            self.data = self._readResource(self.getResourceLocation())
            self.loaded = True

    def _readResource(self,file):
        """utility method to read the resource.   may be overridden in subclasses"""
        file = open(file,"r")
        return file.read()

    def getResourceLocation(self):
        """return the full path to the resource based on task configuration"""
        self.findResourceLocation()
        if(self.foundLocation != None):
            return os.path.normpath(os.path.join(self.foundLocation,self.name))
            #return ('/Users/shubhaviarya/Desktop/Courses/UMN/dr\\ lim/NIH_Examiner/Tasks/Examiner3_6/resource/examiner/flanker/adult/english/practice.txt')
        else:
            #should not get to this point, but if so, simply return the name of
            #the resource, hopefully it is in the same folder as the current working oath
            #return self.name
            #goes here
            #return (/Users/shubhaviarya/Desktop/Courses/UMN/dr\\ lim/NIH_Examiner/Tasks/Examiner3_6/resource/examiner/flanker/adult/english/practice.txt)
            return (self.name) #self.foundLocation is None, self.searchPaths is a list

    def findResourceLocation(self): #problem is in this function -- foundLocation=None .
        #if(not self.foundLocation):
        if(self.foundLocation == None):
            #if(self.searchPaths):
            if(self.searchPaths != None):
                for x in self.searchPaths:
                    if(os.path.isdir(x)):
                        if(os.path.isfile(os.path.normpath(os.path.join(x,self.name)))):
                            self.foundLocation = x
                            return

    def getData(self):
        """return the resource data, loading the resource if needed"""
        if(not self.loaded):
            self.load()
            return self.data

class UnicodeResource(Resource):
    """A utility class to wrap loading unicode text resources.

    """
    def __init__(self,name=None,task=None):
        Resource.__init__(self,name,task)

    def _readResource(self,file):
        """Override base method to load unicode text"""
        file = codecs.open(self.getResourceLocation(), encoding='utf-8')
        return file.read()

    def getText(self):
        self.load()

        # quick way to support RTL languages
        # need to work line by line otherwise [::-1] will reverse the line order as well
        if(self.task.language=='Hebrew'):
            work = self.data.split(u'\n')
            rtlResult = []
            for line in work:
                rtlResult.append(line[::-1])
            return u'\n'.join(rtlResult)

        return self.data

    def getCenteredText(self,width=None):
        self.load()

        # chinese space character: 3000 (hex value); 12288 (decimal value); &#12288; (web value)
        # normal space character: 32 (decimal value)
        if(self.task.language=='Chinese'):
            space_character = chr(12288)
        else:
            space_character = chr(32)

        if(width==None):
            width = self.task.fontCharsPerLine

        formatString = u'{0:' + space_character + '^' + unicode(width) + '}'

        work = self.data.split(u'\n')
        centeredResult = []
        for line in work:
            trimmedLine = self._trimText(line)
            if(len(trimmedLine)>0):
                centeredLine = formatString.format(trimmedLine)
            else:
                centeredLine = trimmedLine

            # a quick way to support RTL languages
            if(self.task.language=='Hebrew'):
                centeredLine = centeredLine[::-1]

            centeredResult.append(centeredLine)
        return u'\n'.join(centeredResult)

    def _trimText(self,text):
        #string the BOM from the string if it exists then strip spaces / tabs / etc from both sides.
        return text.lstrip( unicode( codecs.BOM_UTF8, "utf8" )).strip()

class SessionConfig(object):
    """The class provides a standard dialog box to collect basic session configuration data."""

    def __init__(self,title="Configure Testing Session",subjectId="",sessionNum="",initials="",form="a",language="English",ageCohort="Adult"):
        self.title = title
        self.subjectId = subjectId
        self.sessionNum = sessionNum
        self.initials=initials
        self.form=form
        self.language=language
        self.ageCohort=ageCohort

    def getSessionConfig(self):

        configured = False
        while(configured==False):

            configured=True

            dlg = gui.Dlg(title=self.title, pos=(300,300), size=(300,300))
            dlg.addText('Session Info', color='Blue')
            dlg.addField('Subject ID:', self.subjectId, color='Blue')
            dlg.addField('Session Number:',self.sessionNum,color='Blue')
            dlg.addField('Tester Initials:', self.initials,color='Blue')
            dlg.addText('Battery Configuration', color='Blue')
            dlg.addField('Form:', self.form,color='Blue')
            dlg.addText('Options: a, b, c', color='Black')
            dlg.addField('Language:',self.language, color='Blue')
            dlg.addText('Options: English (e); Spanish (s); Chinese (c); Hebrew (h)', color='Black')
            dlg.addField('Age Group:', self.ageCohort,color='Blue')
            dlg.addText('Options: Adult (a); Child (c)', color='Black')
            dlg.show()

            if dlg.OK==False:
                return False
            else:
                self.subjectId=dlg.data[0]
                self.sessionNum=dlg.data[1]
                self.initials=dlg.data[2]
                self.form=dlg.data[3]
                self.language=dlg.data[4]
                self.ageCohort=dlg.data[5]


            if(len(self.subjectId)<1 or len(self.sessionNum)<1 or len(self.initials) < 1):
                requiredError = gui.Dlg(title=self.title)
                requiredError.addText('Subject ID, Session Number, Tester Initials and Form are required.')
                requiredError.show()
                configured=False
                if(requiredError.OK==False):
                    return False

            if(self.form in ['a','b','c','A','B','C']):
                #make sure form is in lowercase
               self.form = self.form.lower()
            else:
                self.form=""
                formError = gui.Dlg(title=self.title)
                formError.addText('The form provided is invalid.  Please enter "a","b",or "c"')
                formError.show()
                configured=False
                if(formError.OK==False):
                    return False

            if(self.language and self.language.lower() in ['e','english']):
               self.language = 'English'
            elif(self.language and self.language.lower() in ['s','spanish']):
                self.language = 'Spanish'
            elif(self.language and self.language.lower() in ['c','chinese']):
                self.language = 'Chinese'
            elif(self.language and self.language.lower() in ['h','hebrew']):
                self.language = 'Hebrew'
            else:
                self.language=""
                formError = gui.Dlg(title=self.title)
                formError.addText('The language provided is invalid.  Please enter e/English or s/Spanish or c/Chinese or h/Hebrew')
                formError.show()
                configured=False
                if(formError.OK==False):
                    return False

            if(self.ageCohort and self.ageCohort.lower() in ['a','adult']):
                self.ageCohort = "Adult"
            elif(self.ageCohort and self.ageCohort.lower() in ['c','child']):
                self.ageCohort = "Child"
            else:
                self.ageCohort=""
                formError = gui.Dlg(title=self.title)
                formError.addText('The age cohort provided is invalid.  Please enter a/Adult or c/Child"')
                formError.show()
                configured=False
                if(formError.OK==False):
                    return False

        return True

#CHANGES
#1. line 1636 : 'wb' to 'w'
#2. 1656: 'wb' to 'w'