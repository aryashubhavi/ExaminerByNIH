#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Class library that provides unit testing classes for the Saccades computer based task

:Classes:
    TestSaccades - class to test the Saccades task. 
    TestSaccadesResponseMonitor - custom response provider for Saccades testing
    
:Author:
    Joe Hesse, jhesse@memory.ucsf.edu
    
"""

# Part of the Examiner Computer Based Task Library
# Copyright (C) 2011, Regents of the University of California
# All Rights Reserved
#
# Distributed under the terms of the BSD 2-Clause License 
# (http://www.opensource.org/licenses/BSD-2-Clause)

#add examiner library folder to system path for python
import sys
sys.path.append("../../lib/")


import os
import unittest
import lavatask.base
import examiner.saccades


class TestSaccadesResponseMonitor(lavatask.base.ResponseMonitor):
    """Extends the base response monitor to provide automatic responses for test cases.
    
    
    """
    def __init__(self,task,responseMethod):
        lavatask.base.ResponseMonitor.__init__(self,task)
        self.responseMethod = responseMethod #the current response method to use 
        self.responseCount = 0
        self.lastResponseTime = None
    def initialize(self):
        return;
    
    def checkResponse(self,block):
        """ Call method for the specific test response pattern
        """
        return self.check(block)
        
    
    def check(self,block):
        if(block.responseEnabled==False):return False
        
        if(block.name.endswith("Instr")):
            if(block.getTime() > 1):
                block.lastResponse = "space"
                block.lastResponseTime
                return True
        return False 
            
  
        
            
class TestSaccadesVariations(unittest.TestCase):
    """Test variations for the Saccades task 
    """
    
    def setUp(self):
        """create a sped up timer for tasks"""
        testConfig = lavatask.base.Configuration(['../../lavatask.cfg','Test.cfg'])
        self.task = examiner.saccades.SaccadesTask(testConfig)
        self.task.taskClockFactory = lavatask.base.TestingTaskClockFactory(50.000)
        self.task.recordScreenShots = True
        
    def test_EnglishFormA(self):
        """Test English Saccades"""
        self.task.sessionNum = "English"
        self.task.subjectId = "TestSaccades"
        self.task.defaultResponseMonitor = TestSaccadesResponseMonitor(self.task,"Test")
        self.task.runTask()
        #what can we assert?
    
    def test_EnglishFormB(self):
        """Test English Saccades"""
        self.task.sessionNum = "English"
        self.task.subjectId = "TestSaccades"
        self.task.defaultResponseMonitor = TestSaccadesResponseMonitor(self.task,"Test")
        self.task.form = "B"
        self.task.runTask()
        #what can we assert?
    
    def test_EnglishFormC(self):
        """Test English Saccades"""
        self.task.sessionNum = "English"
        self.task.subjectId = "TestSaccades"
        self.task.defaultResponseMonitor = TestSaccadesResponseMonitor(self.task,"Test")
        self.task.form = "C"
        self.task.runTask()
        #what can we assert?
    
    def test_Spanish(self):
        """Test Spanish Saccades"""
        self.task.sessionNum = "Spanish"
        self.task.subjectId = "TestSaccades"
        self.task.defaultResponseMonitor = TestSaccadesResponseMonitor(self.task,"Test")
        self.task.language = "Spanish"
        self.task.runTask()
    
    def test_Hebrew(self):
        """Test Hebrew Saccades"""
        self.task.sessionNum = "Hebrew"
        self.task.subjectId = "TestSaccades"
        self.task.defaultResponseMonitor = TestSaccadesResponseMonitor(self.task,"Test")
        self.task.language = "Hebrew"
        self.task.runTask()
        
              
def runCalcTests():
    #no calcs
    return True
    
def runFlowTests():
    #no flow logic or output
    return True

def runVariationsTests():
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSaccadesVariations)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
   runCalcTests()
   runFlowTests()
   runVariationsTests()
    