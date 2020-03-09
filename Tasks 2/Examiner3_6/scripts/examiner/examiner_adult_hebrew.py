#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script for running the Examiner battery
    
  Loads the configuration file, running the environment check, 
  gathering input from tester with Default Values, and running the Tasks   
      
    
:Author:
- Joe Hesse  

"""
# Part of the Examiner Computer Based Task Library
# Copyright (C) 2011, Regents of the University of California
# All Rights Reserved
#
# Distributed under the terms of the BSD 2-Clause License 
# (http://www.opensource.org/licenses/BSD-2-Clause)

#add lavatask library folder to system path for python
import sys

# Half the time on Windows machines you get the following error:
# "ERROR avbin.dll failed to load. Try importing psychopy.visual as the first library 
# (before anything that uses scipy) and make sure that avbin is installed."
# This error only applies to videos which we don't use so doesn't affect us, but good idea
# to at least hide the error so that users don't get freaked out (which they have).
if sys.platform=='win32':
    import ctypes
    avbin_lib=ctypes.cdll.LoadLibrary('avbin')
    import psychopy.visual
    #assert psychopy.visual.haveAvbin

sys.path.append("../../lib")

from psychopy import core, gui
import lavatask.base
import examiner.flanker
import examiner.setshifting
import examiner.cpt
import examiner.dotcounting
import examiner.nback
import examiner.saccades
import lavatask.environment

#load configuration file
config = lavatask.base.Configuration(['../../lavatask.cfg','examiner.cfg'])

#check test environment, recording findings in data folder
environment = lavatask.environment.Environment(config)
environment.run()

sessionConfig = lavatask.base.SessionConfig("Configure Examiner Battery Session",language='Hebrew')
if(not sessionConfig.getSessionConfig()):
    core.quit()

myDlg = gui.Dlg(title="Administer Flanker Task")
myDlg.addText('Click OK to administer the Flanker Task.')
myDlg.addText('Click CANCEL to skip the Flanker Task.')
myDlg.show()#show dialog and wait for OK or Cancel
if myDlg.OK==True:
    flanker = examiner.flanker.FlankerTask(config,environment,sessionConfig)
    flanker.runTask()

myDlg = gui.Dlg(title="Administer Set Shifting Task")
myDlg.addText('Click OK to administer the Set Shifting Task.')
myDlg.addText('Click CANCEL to skip the Set Shifting Task.')
myDlg.show()#show dialog and wait for OK or Cancel
if myDlg.OK==True:
    setshifting = examiner.setshifting.SetShiftingTask(config,environment,sessionConfig)
    setshifting.runTask()

myDlg = gui.Dlg(title="Administer Dot Counting Task")
myDlg.addText('Click OK to administer the Dot Counting Task.')
myDlg.addText('Click CANCEL to skip the Dot Counting Task.')
myDlg.show()#show dialog and wait for OK or Cancel
if myDlg.OK==True:
    dotcounting = examiner.dotcounting.DotCountingTask(config,environment,sessionConfig)
    dotcounting.runTask()


myDlg = gui.Dlg(title="Administer Continuous Performance Task")
myDlg.addText('Click OK to administer the Continuous Performance Task.')
myDlg.addText('Click CANCEL to skip the Continuous Performance Task.')
myDlg.show()#show dialog and wait for OK or Cancel
if myDlg.OK==True:
    cpt = examiner.cpt.CPTTask(config,environment,sessionConfig)
    cpt.runTask()

myDlg = gui.Dlg(title="Administer NBack Task")
myDlg.addText('Click OK to administer the NBack Task.')
myDlg.addText('Click CANCEL to skip the NBack Task.')
myDlg.show()#show dialog and wait for OK or Cancel
if myDlg.OK==True:
    nback = examiner.nback.NBackTask(config,environment,sessionConfig)
    nback.runTask()
    

myDlg = gui.Dlg(title="Administer Saccades Task")
myDlg.addText('Click OK to administer the Saccades Task.')
myDlg.addText('Click CANCEL to skip the Saccades Task.')
myDlg.show()#show dialog and wait for OK or Cancel
if myDlg.OK==True:
    saccades = examiner.saccades.SaccadesTask(config,environment,sessionConfig)
    saccades.runTask()
    

myDlg = gui.Dlg(title="Examiner Battery Complete")
myDlg.addText('The Examiner Battery is complete.')
myDlg.show()#show dialog and wait for OK or Cancel

core.quit()
sys.exit()
