#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script example for running the Saccades Task
    
  Provides example of loading configuration file and running the SaccadesTask   
       
    
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
sys.path.append("../../../lib")

from psychopy import core, gui
import lavatask.base
import examiner.saccades

#load configuration file
config = lavatask.base.Configuration(['../../../lavatask.cfg','examiner.cfg'])


#check test environment, recording findings in data folder
environment = lavatask.environment.Environment(config)
environment.run()

sessionConfig = lavatask.base.SessionConfig("Configure Saccades Session")
if(not sessionConfig.getSessionConfig()):
    core.quit()

#Setup default task execution data
task = examiner.saccades.SaccadesTask(config,environment,sessionConfig)

task.runTask()
core.quit() 
sys.exit()
