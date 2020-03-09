#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Class library that provides unit testing classes for the CPT computer based task

:Classes:
    TestCPTCalc - test cases for the summary calculations for the CPT Task
    TestCPTFlowAndOutput - test cases for the practice trials flow. 
    TestCPTResponseMonitor - custom response provider for CPT testing

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
import examiner.cpt


class TestCPTResponseMonitor(lavatask.base.ResponseMonitor):
    """Extends the base response monitor to provide automatic responses for test cases.
    
    
    """
    def __init__(self,task,responseMethod):
        lavatask.base.ResponseMonitor.__init__(self,task)
        self.responseMethod = responseMethod #the current response method to use 
        self.lastTrialHandled = 0 #used to track when response has already been provided
        self.currentBlock = "None"
        self.firstTargetError = False
        self.firstNontargetError = False 
        self.secondTargetError = False
        self.secondNontargetError = False
        
    def initialize(self):
        return;
    def checkResponse(self,block):
        """ Call method for the specific test response pattern
        """
        if(self.responseMethod == "AllCorrect"):
            return self.check_AllCorrect(block)
        elif(self.responseMethod == "FailFirstPractice"):
            return self.check_FailFirstPractice(block)
        elif(self.responseMethod == "FailSecondPractice"):
            return self.check_FailSecondPractice(block)
        elif(self.responseMethod == "FailAllPractice"):
            return self.check_FailAllPractice(block)
        elif(self.responseMethod == "FourErrorsPerSet"):
            return self.check_FourErrorsPerSet(block)
        return False
    
    def markTrialHandled(self,block):
        self.lastTrialHandled = block.currentTrialNum
    
    def isTrialHandled(self,block):
        return (self.lastTrialHandled == block.currentTrialNum)
    
    
    def check_AllCorrect(self,block):
        if(block.responseEnabled==False):return False
        
        if(block.name in ["firstPracticeBlock","secondPracticeBlock","thirdPracticeBlock","testingBlock"]):
            if(block.getTime() >= .5 and not self.isTrialHandled(block)):
                self.markTrialHandled(block)
                if(block.currentTrial.stimulus=='target'):
                    block.lastResponse = 'left'
                    block.lastResponseTime = block.getTime()
                    return True
        else: #handle instructions
            if(block.getTime() > .5):
                block.lastResponse = "space"
                block.lastResponseTime = block.getTime()
                return True
        
    def check_FailAllPractice(self,block):
        if(block.responseEnabled==False):return False
        
        if(block.name in ["firstPracticeBlock","secondPracticeBlock","thirdPracticeBlock","testingBlock"]):
            if(block.getTime() >= .5 and not self.isTrialHandled(block)):
                self.markTrialHandled(block)
                if(block.currentTrial.stimulus!='target'):
                    block.lastResponse = 'left'
                    block.lastResponseTime = block.getTime()
                    return True
        else: #handle instructions
            if(block.getTime() > .5):
                block.lastResponse = "space"
                block.lastResponseTime = block.getTime()
                return True
    
    def check_FailFirstPractice(self,block):
        if(block.responseEnabled==False):return False
        
        if(block.name in ["firstPracticeBlock"]):
          if(block.getTime() >= .5 and not self.isTrialHandled(block)):
                self.markTrialHandled(block)
                if(block.currentTrial.stimulus!='target'):
                    block.lastResponse = 'left'
                    block.lastResponseTime = block.getTime()
                    return True
        elif(block.name in ["secondPracticeBlock","thirdPracticeBlock","testingBlock"]):
            if(block.getTime() >= .5 and not self.isTrialHandled(block)):
                self.markTrialHandled(block)
                if(block.currentTrial.stimulus=='target'):
                    block.lastResponse = 'left'
                    block.lastResponseTime = block.getTime()
                    return True
        else: #handle instructions
            if(block.getTime() > .5):
                block.lastResponse = "space"
                block.lastResponseTime = block.getTime()
                return True
    
    def check_FailSecondPractice(self,block):
        if(block.responseEnabled==False):return False
        
        
        if(block.name in ["firstPracticeBlock","secondPracticeBlock"]):
          if(block.getTime() >= .5 and not self.isTrialHandled(block)):
                self.markTrialHandled(block)
                if(block.currentTrial.stimulus!='target'):
                    block.lastResponse = 'left'
                    block.lastResponseTime = block.getTime()
                    return True
        elif(block.name in ["thirdPracticeBlock","testingBlock"]):
            if(block.getTime() >= .5 and not self.isTrialHandled(block)):
                self.markTrialHandled(block)
                if(block.currentTrial.stimulus=='target'):
                    block.lastResponse = 'left'
                    block.lastResponseTime = block.getTime()
                    return True
        else: #handle instructions
            if(block.getTime() > .5):
                block.lastResponse = "space"
                block.lastResponseTime = block.getTime()
                return True
    
    
    def check_FourErrorsPerSet(self,block):
        '''Fail four times in each block.
        
            First Target, fail by omission
            First NonTarget, fail by intrusion
            Second Target, fail by multiple response
            Second NonTarget, fail by multiple response
            
        '''
        if(self.currentBlock != block.name):
            self.currentBlock = block.name
            self.firstTargetError = False
            self.firstNontargetError = False 
            self.secondTargetError = False
            self.secondNontargetError = False
        
        if(block.responseEnabled==False):return False
        
        if(block.name in ["firstPracticeBlock","secondPracticeBlock","thirdPracticeBlock","testingBlock"]):
            
            if(block.getTime() >= .5 and not self.isTrialHandled(block)):
            
                if(block.currentTrial.stimulus=='target'):
                    if(not self.firstTargetError):
                        self.markTrialHandled(block)
                        self.firstTargetError = True
                    elif(not self.secondTargetError):
                        block.lastResponse = 'left'
                        block.lastResponseTime = block.getTime()
                        self.secondTargetError = 1
                        return True
                    elif(self.secondTargetError == 1):
                        if(block.getTime()>=1):
                            block.lastResponse = 'left'
                            block.lastResponseTime = block.getTime()
                            self.secondTargetError = 2
                            self.markTrialHandled(block)
                            return True
                    else:
                        self.markTrialHandled(block)
                        block.lastResponse = 'left'
                        block.lastResponseTime = block.getTime()
                        return True
                else: #nontargets
                    if(not self.firstNontargetError):
                        self.markTrialHandled(block)
                        block.lastResponse = 'left'
                        block.lastResponseTime = block.getTime()
                        self.firstNontargetError = True
                        return True
                    elif(not self.secondNontargetError):
                        block.lastResponse = 'left'
                        block.lastResponseTime = block.getTime()
                        self.secondNontargetError = 1
                        return True
                    elif(self.secondNontargetError == 1):
                        if(block.getTime()>=1):
                            block.lastResponse = 'left'
                            block.lastResponseTime = block.getTime()
                            self.secondNontargetError = 2
                            self.markTrialHandled(block)
                            return True
                    else:
                        self.markTrialHandled(block)
                        
        else: #handle instructions
            if(block.getTime() > .5):
                block.lastResponse = "space"
                block.lastResponseTime = block.getTime()
                return True


class TestCPTFlowAndOutput(unittest.TestCase):
    """Test cases for the CPT task application flow and output files,
    
    """
    
    def setUp(self):
        """create a sped up timer for tasks"""
        testConfig = lavatask.base.Configuration(['../../lavatask.cfg','Test.cfg'])
        self.task = examiner.cpt.CPTTask(testConfig)
        #only run at 25 times speed.  Running at 50 times speed creates an unresolvable error with one of the test cases. 
        self.task.taskClockFactory = lavatask.base.TestingTaskClockFactory(25.000)
        
    
    def test_AllCorrectEnglishAdult(self):
        """Test CPT flow when all responses correct"""
        self.task.sessionNum = "AllCorrect"
        self.task.subjectId = 'CPTTest'
        self.task.defaultResponseMonitor = TestCPTResponseMonitor(self.task,"AllCorrect")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,120)
    
    def test_FailFirstPracticeEnglishAdult(self):
        """Test CPT fail the first practice"""
        self.task.sessionNum = "FailFirstPractice"
        self.task.subjectId = 'CPTTest'
        self.task.defaultResponseMonitor = TestCPTResponseMonitor(self.task,"FailFirstPractice")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,140)
        
    def test_FailSecondPracticeEnglishAdult(self):
        """Test CPT flow, fail the first and second practice."""
        self.task.sessionNum = "FailSecondPractice"
        self.task.subjectId = 'CPTTest'
        self.task.defaultResponseMonitor = TestCPTResponseMonitor(self.task,"FailSecondPractice")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,160)
    
    def test_FailAllPracticeEnglishAdult(self):
        """Test CPT flow, fail all practice."""
        self.task.sessionNum = "FailAllPractice"
        self.task.subjectId = 'CPTTest'
        self.task.defaultResponseMonitor = TestCPTResponseMonitor(self.task,"FailAllPractice")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,60)
        
    def test_FourErrorsPerSetEnglishAdult(self):
        """Test cpt flow, fail four per set."""
        self.task.sessionNum = "FourErrorsPerSet"
        self.task.subjectId = 'CPTTest'
        self.task.defaultResponseMonitor = TestCPTResponseMonitor(self.task,"FourErrorsPerSet")
        self.task.runTask()
        summary = self.task.responses.getSummaryStatsFields()
        self.assertEqual(summary['total_corr'],96)
        self.assertEqual(summary['target_corr'],78)
        self.assertEqual(summary['target_errors'],1)
        self.assertEqual(summary['nontarget_corr'],18)
        self.assertEqual(summary['nontarget_errors'],1)
        self.assertEqual(summary['performance_errors'],2)
        self.assertEqual(self.task.responses.count,120)
    
class TestCPTCalc(unittest.TestCase):
    """Test cases for the summary calculations for the CPT Task.
    
    """
    def setUp(self):
        """create a standard cpt task for unit tests."""
        testConfig = lavatask.base.Configuration(['../../lavatask.cfg','Test.cfg'])
        self.task = examiner.cpt.CPTTask(testConfig)
        self.task.sessionNum = "Calculations"
        self.task.subjectId = 'CPTTest'
        self.task.createDefaultTaskMonitor()
        self.task.createDefaultTaskWindow()
        self.task.initializeTask()
        
    
    def test_calculation01(self):
        """Test calculations: test summary stats when no responses present."""
        responses = self.task.responses
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['total_trials'],0)
        self.assertEqual(summary['total_corr'],0)
        self.assertEqual(summary['total_errors'],0)
        self.assertEqual(summary['target_corr'],0)
        self.assertEqual(summary['target_errors'],0)
        self.assertEqual(summary['target_mean'],-5)
        self.assertEqual(summary['target_median'],-5)
        self.assertEqual(summary['target_stdev'],-5)
        self.assertEqual(summary['nontarget_corr'],0)
        self.assertEqual(summary['nontarget_errors'],0)
        self.assertEqual(summary['performance_errors'],0)
      
    def test_calculation02(self):
        """Test calculations: test summary stats when all target responses are correct and given at 1.2345 seconds."""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(4)
        for trialData in testingBlock.trialHandler:
            response = examiner.cpt.CPTResponse()
            response.block=testingBlock
            response.trialData = trialData
            if(response.trialData.stimulus=='target'):
                response.key='left'
                response.rt=1.2345
                response.responses.append(1.2345)
                response.taskTime=0 #not needed for calc testing
                response.trialNum=0 #not needed for calc testing
                response.corr=1
            else:
                response.key='none'
                response.rt=0
                response.taskTime=0 #not needed for calc testing
                response.trialNum=0 #not needed for calc testing
                response.corr=1
          
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['total_trials'],100)
        self.assertEqual(summary['total_corr'],100)
        self.assertEqual(summary['total_errors'],0)
        self.assertEqual(summary['target_corr'],80)
        self.assertEqual(summary['target_errors'],0)
        self.assertEqual(summary['target_mean'],1.2345)
        self.assertEqual(summary['target_median'],1.2345)
        self.assertEqual(summary['target_stdev'],0)
        self.assertEqual(summary['nontarget_corr'],20)
        self.assertEqual(summary['nontarget_errors'],0)
        self.assertEqual(summary['performance_errors'],0)
      
    def test_calculation03(self):
        """Test calculations: test summary stats when all responses are incorrect and given at 1.2345 seconds."""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(4)
        for trialData in testingBlock.trialHandler:
            response = examiner.cpt.CPTResponse()
            response.block=testingBlock
            response.trialData = trialData
            if(response.trialData.stimulus=='nontarget'):
                response.key='left'
                response.rt=1.2345
                response.responses.append(1.2345)
                response.taskTime=0 #not needed for calc testing
                response.trialNum=0 #not needed for calc testing
                response.corr=0
            else:
                response.key='none'
                response.rt=0
                response.taskTime=0 #not needed for calc testing
                response.trialNum=0 #not needed for calc testing
                response.corr=0
          
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['total_trials'],100)
        self.assertEqual(summary['total_corr'],0)
        self.assertEqual(summary['total_errors'],100)
        self.assertEqual(summary['target_corr'],0)
        self.assertEqual(summary['target_errors'],80)
        self.assertEqual(summary['target_mean'],-5)
        self.assertEqual(summary['target_median'],-5)
        self.assertEqual(summary['target_stdev'],-5)
        self.assertEqual(summary['nontarget_corr'],0)
        self.assertEqual(summary['nontarget_errors'],20)
        self.assertEqual(summary['performance_errors'],0)
    
    def test_calculation04(self):
        """Test calculations: test summary stats when half target responses are at  1.1111 seconds and half are at 3.3333"""
        responses = self.task.responses
        self.lastRT = 1.1111
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(4)
        for trialData in testingBlock.trialHandler:
            response = examiner.cpt.CPTResponse()
            response.block=testingBlock
            response.trialData = trialData
            if(response.trialData.stimulus=='target'):
                response.key='left'
                if(self.lastRT==1.1111):
                    response.rt=3.3333
                    self.lastRT=3.3333
                    response.responses.append(3.3333)
                
                else:
                    response.rt=1.1111
                    self.lastRT=1.1111
                    response.responses.append(1.1111)
                
                response.taskTime=0 #not needed for calc testing
                response.trialNum=0 #not needed for calc testing
                response.corr=1
            else:
                response.key='none'
                response.rt=0
                response.taskTime=0 #not needed for calc testing
                response.trialNum=0 #not needed for calc testing
                response.corr=1
          
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['total_trials'],100)
        self.assertEqual(summary['total_corr'],100)
        self.assertEqual(summary['total_errors'],0)
        self.assertEqual(summary['target_corr'],80)
        self.assertEqual(summary['target_errors'],0)
        self.assertEqual(summary['target_mean'],2.2222)
        self.assertEqual(summary['target_median'],2.2222)
        self.assertEqual(summary['target_stdev'],1.1111)
        self.assertEqual(summary['nontarget_corr'],20)
        self.assertEqual(summary['nontarget_errors'],0)
        self.assertEqual(summary['performance_errors'],0)

    def test_calculation05(self):
        """Test calculations: test summary stats when all nontarget trials are answered incorrect"""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(4)
        for trialData in testingBlock.trialHandler:
            response = examiner.cpt.CPTResponse()
            response.block=testingBlock
            response.trialData = trialData
            response.key='left'
            response.rt=1.2345
            response.responses.append(1.2345)
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.trialData.stimulus=='target'):
                response.corr=1
            else:
                response.corr=0
                
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['total_trials'],100)
        self.assertEqual(summary['total_corr'],80)
        self.assertEqual(summary['total_errors'],20)
        self.assertEqual(summary['target_corr'],80)
        self.assertEqual(summary['target_errors'],0)
        self.assertEqual(summary['target_mean'],1.2345)
        self.assertEqual(summary['target_median'],1.2345)
        self.assertEqual(summary['target_stdev'],0)
        self.assertEqual(summary['nontarget_corr'],0)
        self.assertEqual(summary['nontarget_errors'],20)
        self.assertEqual(summary['performance_errors'],0)
    
    def test_calculation06(self):
        """Test calculations: test all three types of errors"""
        responses = self.task.responses
        self.lastTarget = 4
        self.lastNontarget = 4
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(4)
        for trialData in testingBlock.trialHandler:
            response = examiner.cpt.CPTResponse()
            response.block=testingBlock
            response.trialData = trialData
            if(response.trialData.stimulus=='target'):
                if(self.lastTarget==4):
                    self.lastTarget=1  #correct
                    response.key='left'
                    response.rt=3.3333
                    response.responses.append(3.3333)
                    response.corr = 1
                elif(self.lastTarget==1):
                    response.key='none'  #ommision
                    response.rt=0
                    response.corr=0
                    self.lastTarget=2
                elif(self.lastTarget==2):
                    self.lastTarget=3  #double response
                    response.key='left'
                    response.rt=3.3333
                    response.responses.append(1.1111)
                    response.responses.append(3.3333)
                    response.corr = 0
                    response.extraResponses='[1.1111,3.3333]'
                elif(self.lastTarget==3):
                    self.lastTarget=4  #correct
                    response.key='left'
                    response.rt=3.3333
                    response.responses.append(3.3333)
                    response.corr = 1
   
                   
                response.taskTime=0 #not needed for calc testing
                response.trialNum=0 #not needed for calc testing
               
            else:  #nontargets
                if(self.lastNontarget==4):
                    self.lastNontarget=1  #incorrect
                    response.key='left'
                    response.rt=3.3333
                    response.responses.append(3.3333)
                    response.corr = 0
                elif(self.lastNontarget==1):
                    response.key='none'  #correct
                    response.rt=0
                    response.corr=1
                    self.lastNontarget=2
                elif(self.lastNontarget==2):
                    self.lastNontarget=3  #double response
                    response.key='left'
                    response.rt=3.3333
                    response.responses.append(3.3333)
                    response.corr = 0
                    response.extraResponses='[1.1111,3.3333]'
                elif(self.lastNontarget==3):
                    response.key='none'  #correct
                    response.rt=0
                    response.corr=1
                    self.lastNontarget=4
                   
                response.taskTime=0 #not needed for calc testing
                response.trialNum=0 #not needed for calc testing
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['total_trials'],100)
        self.assertEqual(summary['total_corr'],50)
        self.assertEqual(summary['total_errors'],50)
        self.assertEqual(summary['target_corr'],40)
        self.assertEqual(summary['target_errors'],20)
        self.assertEqual(summary['target_mean'],3.3333)
        self.assertEqual(summary['target_median'],3.3333)
        self.assertEqual(summary['target_stdev'],0)
        self.assertEqual(summary['nontarget_corr'],10)
        self.assertEqual(summary['nontarget_errors'],5)
        self.assertEqual(summary['performance_errors'],25)

class TestCPTVariations(unittest.TestCase):
    """Test variations of the CPT task 
    
    """
    
    def setUp(self):
        """create a sped up timer for tasks"""
        testConfig = lavatask.base.Configuration(['../../lavatask.cfg','Test.cfg'])
        self.task = examiner.cpt.CPTTask(testConfig)
        #only run at 25 times speed.  Running at 50 times speed creates an unresolvable error with one of the test cases. 
        self.task.taskClockFactory = lavatask.base.TestingTaskClockFactory(25.000)
        self.task.recordScreenShots = True
            
    def test_EnglishAdultA(self):
        """Test CPT Adult English Form A, fail the first and second practice."""
        self.task.sessionNum = "EnglishAdultA"
        self.task.subjectId = 'CPTTest'
        self.task.defaultResponseMonitor = TestCPTResponseMonitor(self.task,"FailSecondPractice")
        self.task.language = 'English'
        self.task.form = 'a'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,160)
    
    def test_SpanishAdultA(self):
        """Test CPT Adult Spanish Form A, fail the first and second practice."""
        self.task.sessionNum = "SpanishAdultA"
        self.task.subjectId = 'CPTTest'
        self.task.defaultResponseMonitor = TestCPTResponseMonitor(self.task,"FailSecondPractice")
        self.task.language = 'Spanish'
        self.task.form = 'a'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,160)

    def test_HebrewAdultA(self):
        """Test CPT Adult Hebrew Form A, fail the first and second practice."""
        self.task.sessionNum = "HebrewAdultA"
        self.task.subjectId = 'CPTTest'
        self.task.defaultResponseMonitor = TestCPTResponseMonitor(self.task,"FailSecondPractice")
        self.task.language = 'Hebrew'
        self.task.form = 'a'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,160)
  
    def test_EnglishAdultB(self):
        """Test CPT Adult English Form B, fail the first and second practice."""
        self.task.sessionNum = "EnglishAdultB"
        self.task.subjectId = 'CPTTest'
        self.task.defaultResponseMonitor = TestCPTResponseMonitor(self.task,"FailSecondPractice")
        self.task.language = 'English'
        self.task.form = 'b'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,160)
    
    def test_SpanishAdultB(self):
        """Test CPT Adult Spanish Form B, fail the first and second practice."""
        self.task.sessionNum = "SpanishAdultB"
        self.task.subjectId = 'CPTTest'
        self.task.defaultResponseMonitor = TestCPTResponseMonitor(self.task,"FailSecondPractice")
        self.task.language = 'Spanish'
        self.task.form = 'b'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,160)

    def test_HebrewAdultB(self):
        """Test CPT Adult Hebrew Form B, fail the first and second practice."""
        self.task.sessionNum = "HebrewAdultB"
        self.task.subjectId = 'CPTTest'
        self.task.defaultResponseMonitor = TestCPTResponseMonitor(self.task,"FailSecondPractice")
        self.task.language = 'Hebrew'
        self.task.form = 'b'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,160)

    def test_EnglishAdultC(self):
        """Test CPT Adult English Form C, fail the first and second practice."""
        self.task.sessionNum = "EnglishAdultC"
        self.task.subjectId = 'CPTTest'
        self.task.defaultResponseMonitor = TestCPTResponseMonitor(self.task,"FailSecondPractice")
        self.task.language = 'English'
        self.task.form = 'c'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,160)
    
    def test_SpanishAdultC(self):
        """Test CPT Adult Spanish Form C, fail the first and second practice."""
        self.task.sessionNum = "SpanishAdultC"
        self.task.subjectId = 'CPTTest'
        self.task.defaultResponseMonitor = TestCPTResponseMonitor(self.task,"FailSecondPractice")
        self.task.language = 'Spanish'
        self.task.form = 'c'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,160)

    def test_HebrewAdultC(self):
        """Test CPT Adult Hebrew Form C, fail the first and second practice."""
        self.task.sessionNum = "HebrewAdultC"
        self.task.subjectId = 'CPTTest'
        self.task.defaultResponseMonitor = TestCPTResponseMonitor(self.task,"FailSecondPractice")
        self.task.language = 'Hebrew'
        self.task.form = 'c'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,160)

def runCalcTests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCPTCalc)
    unittest.TextTestRunner(verbosity=2).run(suite)

def runFlowTests():
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCPTFlowAndOutput)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
def runVariationsTests():
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCPTVariations)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
   runCalcTests()
   runFlowTests()
   runVariationsTests()
    