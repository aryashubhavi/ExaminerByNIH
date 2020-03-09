#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script example for running the Environment Checking Task
    
  Provides example of loading configuration file, running the environment check  
      
:Author:
    Joe Hesse, jhesse@memory.ucsf.edu

"""

# Part of the LavaTask Library
# Copyright (C) 2011, Regents of the University of California
# All Rights Reserved
#
# Distributed under the terms of the BSD 2-Clause License 
# (http://www.opensource.org/licenses/BSD-2-Clause)


#add lavatask library folder to system path for python
import sys
sys.path.append("../../lib")

from psychopy import core, gui
import lavatask.base
import lavatask.environment

#load configuration file
config = lavatask.base.Configuration(['../../lavatask.cfg','lavatask.cfg'])

#check test environment, recording findings in data folder
environment = lavatask.environment.Environment(config)
environment.run()

core.quit()
