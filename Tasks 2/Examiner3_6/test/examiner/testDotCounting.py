#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Class library that provides unit testing classes for the Dot Counting computer based task

:Classes:
    TestDotCounting - class to test the dot counting task. 
    TestDotCountingResponseMonitor - custom response provider for Dot Counting testing
    
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
import examiner.dotcounting


class TestDotCountingResponseMonitor(lavatask.base.ResponseMonitor):
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
        if(self.responseMethod == "Spacebar"):
            return self.check_Spacebar(block)
        elif(self.responseMethod == "Arrows"):
            return self.check_Arrows(block)
        return False
    
    
    def check_Spacebar(self,block):
        if(self.lastResponseTime == None):
            self.lastResponseTime = block.getTime()
        
        if(self.lastResponseTime + 2.0 > block.getTime()):
            return False;
        else:
            block.lastResponse = 'space'
            block.lastResponseTime = block.getTime()
            self.lastResponseTime = None
            self.responseCount = self.responseCount + 1
            return True
            
    def check_Arrows(self,block):
        if(self.lastResponseTime == None):
            self.lastResponseTime = block.getTime()
        
        if(self.lastResponseTime + 2.0 > block.getTime()):
            return False;
        else:
            if(self.responseCount > 40 and self.responseCount < 70):
                block.lastResponse = 'left'
            else:
                block.lastResponse = 'right'

            block.lastResponseTime = block.getTime()
            self.lastResponseTime = None
            self.responseCount = self.responseCount + 1
            return True
            
class TestDotCounting(unittest.TestCase):
    """Test cases for the Dot Counting task 
    """
    
    def setUp(self):
        """create a sped up timer for tasks"""
        testConfig = lavatask.base.Configuration(['../../lavatask.cfg','Test.cfg'])
        self.task = examiner.dotcounting.DotCountingTask(testConfig)
        self.task.taskClockFactory = lavatask.base.TestingTaskClockFactory(10.000)
        
    def test_Arrows(self):
        """Test CPT using arrows to advance forward and backward through the screens with a 2 second delay"""
        self.task.sessionNum = "Arrows"
        self.task.subjectId = "TestDotCounting"
        self.task.defaultResponseMonitor = TestDotCountingResponseMonitor(self.task,"Arrows")
        self.task.runTask()
        self.assertEqual(self.task.defaultResponseMonitor.responseCount,104)
        
    def test_Spacebar(self):
        """Test CPT using spacebar to advance through all screens with a 2 second delay"""
        self.task.sessionNum = "Spacebar"
        self.task.subjectId = "TestDotCounting"
        self.task.defaultResponseMonitor = TestDotCountingResponseMonitor(self.task,"Spacebar")
        self.task.runTask()
        self.assertEqual(self.task.defaultResponseMonitor.responseCount,46)
    

class TestDotCountingVariations(unittest.TestCase):
    """Test variations for the Dot Counting task 
    """
    
    def setUp(self):
        """create a sped up timer for tasks"""
        testConfig = lavatask.base.Configuration(['../../lavatask.cfg','Test.cfg'])
        self.task = examiner.dotcounting.DotCountingTask(testConfig)
        self.task.taskClockFactory = lavatask.base.TestingTaskClockFactory(50.000)
        self.task.recordScreenShots = True
        
    def test_EnglishA(self):
        """Test Dot Counting English FormA"""
        self.task.sessionNum = "EnglishA"
        self.task.subjectId = "TestDotCounting"
        self.task.defaultResponseMonitor = TestDotCountingResponseMonitor(self.task,"Spacebar")
        self.task.language = 'English'
        self.task.form = 'a'
        self.task.runTask()
        self.assertEqual(self.task.defaultResponseMonitor.responseCount,46)


    def test_EnglishB(self):
        """Test Dot Counting English Form B"""
        self.task.sessionNum = "EnglishB"
        self.task.subjectId = "TestDotCounting"
        self.task.defaultResponseMonitor = TestDotCountingResponseMonitor(self.task,"Spacebar")
        self.task.language = 'English'
        self.task.form = 'b'
        self.task.runTask()
        self.assertEqual(self.task.defaultResponseMonitor.responseCount,46)

    def test_EnglishC(self):
        """Test Dot Counting English Form C"""
        self.task.sessionNum = "EnglishC"
        self.task.subjectId = "TestDotCounting"
        self.task.defaultResponseMonitor = TestDotCountingResponseMonitor(self.task,"Spacebar")
        self.task.language = 'English'
        self.task.form = 'c'
        self.task.runTask()
        self.assertEqual(self.task.defaultResponseMonitor.responseCount,46)

    def test_SpanishA(self):
        """Test Dot Counting Spanish Form A"""
        self.task.sessionNum = "SpanishA"
        self.task.subjectId = "TestDotCounting"
        self.task.defaultResponseMonitor = TestDotCountingResponseMonitor(self.task,"Spacebar")
        self.task.language = 'Spanish'
        self.task.form = 'a'
        self.task.runTask()
        self.assertEqual(self.task.defaultResponseMonitor.responseCount,46)

    def test_HebrewA(self):
        """Test Dot Counting Hebrew Form A"""
        self.task.sessionNum = "HebrewA"
        self.task.subjectId = "TestDotCounting"
        self.task.defaultResponseMonitor = TestDotCountingResponseMonitor(self.task,"Spacebar")
        self.task.language = 'Hebrew'
        self.task.form = 'a'
        self.task.runTask()
        self.assertEqual(self.task.defaultResponseMonitor.responseCount,46)

def runCalcTests():
    #No calcs
    return True

def runFlowTests():
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDotCounting)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
def runVariationsTests():
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDotCountingVariations)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
   runCalcTests()
   runFlowTests()
   runVariationsTests()
    
