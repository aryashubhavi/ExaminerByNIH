#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Class library that provides unit testing classes for the Set Shifting computer based task

:Classes:
    TestSetShiftingCalc - test cases for the summary calculations for the SetShifting Task
    TestSetShiftingFlowAndOutput - test cases for the practice trials flow. 
    TestSetShiftingResponseMonitor - custom response provider for set shifting testing
    
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
import examiner.setshifting


class TestSetShiftingResponseMonitor(lavatask.base.ResponseMonitor):
    """Extends the base response monitor to provide automatic responses for test cases.
    
    
    """
    def __init__(self,task,responseMethod):
        lavatask.base.ResponseMonitor.__init__(self,task)
        self.responseMethod = responseMethod #the current response method to use 
        
        
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
        elif(self.responseMethod == "FrequentNoResponse"):
            return self.check_FrequentNoResponse(block)
        return False
    
    def check_AllCorrect(self,block):
        if(block.responseEnabled==False):return False
        
        if(block.name in ["firstPracticeBlock","secondPracticeBlock","thirdPracticeBlock","throwawayBlock","testingBlock"]):
            if(block.getTime() >= block.targetDisplayTime + .5):
                block.lastResponse = block.currentTrial.corr_resp
                block.lastResponseTime = block.getTime()
                return True
        else:
            if(block.getTime() > .5):
                block.lastResponse = "space"
                block.lastResponseTime = block.getTime()
                return True
        
    def check_FailAllPractice(self,block):
        if(block.responseEnabled==False):return False
        
        if(block.name in ["firstPracticeBlock","secondPracticeBlock","thirdPracticeBlock","throwawayBlock","testingBlock"]):
            if(block.getTime() >= block.targetDisplayTime + .5):
                if(block.currentTrial.corr_resp == "left"):
                    block.lastResponse = "right"
                else:
                    block.lastResponse = "left"
                block.lastResponseTime = block.getTime()
                return True
        else:
            if(block.getTime() > .5):
                block.lastResponse = "space"
                block.lastResponseTime = block.getTime()
                return True
    
    def check_FailFirstPractice(self,block):
        if(block.responseEnabled==False):return False
        
        if(block.name in ["firstPracticeBlock"]):
            if(block.getTime() >= block.targetDisplayTime + .5):
                block.lastResponse = "left"
                block.lastResponseTime = block.getTime()
                return True
        elif(block.name in ["secondPracticeBlock","thirdPracticeBlock","throwawayBlock","testingBlock"]):
            if(block.getTime() >= block.targetDisplayTime + .5):
                block.lastResponse = block.currentTrial.corr_resp
                block.lastResponseTime = block.getTime()
                return True
        else:
            if(block.getTime() > .5):
                block.lastResponse = "space"
                block.lastResponseTime = block.getTime()
                return True
    
    def check_FailSecondPractice(self,block):
        if(block.responseEnabled==False):return False
        
        if(block.name in ["firstPracticeBlock","secondPracticeBlock"]):
            if(block.getTime() >= block.targetDisplayTime + .5):
                block.lastResponse = "left"
                block.lastResponseTime = block.getTime()
                return True
        elif(block.name in ["thirdPracticeBlock","throwawayBlock","testingBlock"]):
            if(block.getTime() >= block.targetDisplayTime + .5):
                block.lastResponse = block.currentTrial.corr_resp
                block.lastResponseTime = block.getTime()
                return True
        else:
            if(block.getTime() > .5):
                block.lastResponse = "space"
                block.lastResponseTime = block.getTime()
                return True
    
    def check_FrequentNoResponse(self,block):
        if(block.responseEnabled==False):return False
        
        if(block.name in ["firstPracticeBlock"]):
            if(block.getTime() >= block.targetDisplayTime + .5):
                block.lastResponse = block.currentTrial.corr_resp
                block.lastResponseTime = block.getTime()
                return True
        elif(block.name in ["secondPracticeBlock","thirdPracticeBlock","throwawayBlock","testingBlock"]):
            if(block.getTime() >= block.targetDisplayTime + .5):
                if(block.currentTrialNum % 10 == 0):
                    return False #simulate no response
                else:
                    block.lastResponse = block.currentTrial.corr_resp
                    block.lastResponseTime = block.getTime()
                    return True
        else:
            if(block.getTime() > .5):
                block.lastResponse = "space"
                block.lastResponseTime = block.getTime()
                return True
    


class TestSetShiftingFlowAndOutput(unittest.TestCase):
    """Test cases for the Set Shifting task application flow and output files,
    
    """
    def setUp(self):
        """create a sped up timer for tasks"""
        testConfig = lavatask.base.Configuration(['../../lavatask.cfg','Test.cfg'])
        self.task = examiner.setshifting.SetShiftingTask(testConfig)
        self.task.taskClockFactory = lavatask.base.TestingTaskClockFactory(50.000)

    
    def test_AllCorrectEnglishAdult(self):
        """Test Set Shifting flow when all responses correct"""
        self.task.sessionNum = "AllCorrect"
        self.task.subjectId = "TestSetShifting"
        self.task.defaultResponseMonitor = TestSetShiftingResponseMonitor(self.task,"AllCorrect")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,122)
    
    def test_FailFirstPracticeEnglishAdult(self):
        """Test Set Shifting fail the first practice"""
        self.task.sessionNum = "FailFirstPractice"
        self.task.subjectId = "TestSetShifting"
        self.task.defaultResponseMonitor = TestSetShiftingResponseMonitor(self.task,"FailFirstPractice")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,138)
        
    def test_FailSecondPracticeEnglishAdult(self):
        """Test Set Shifting flow, fail the first and second practice."""
        self.task.sessionNum = "FailSecondPractice"
        self.task.subjectId = "TestSetShifting"
        self.task.defaultResponseMonitor = TestSetShiftingResponseMonitor(self.task,"FailSecondPractice")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,154)
    
    def test_FailAllPracticeEnglishAdult(self):
        """Test Set Shifting flow, fail all practice."""
        self.task.sessionNum = "FailAllPractice"
        self.task.subjectId = "TestSetShifting"
        self.task.defaultResponseMonitor = TestSetShiftingResponseMonitor(self.task,"FailAllPractice")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,48)
        
    def test_FrequentNoResponseEnglishAdult(self):
        """Test Set Shifting flow, frequent no response."""
        self.task.sessionNum = "FrequentNoResponse"
        self.task.subjectId = "TestSetShifting"
        self.task.defaultResponseMonitor = TestSetShiftingResponseMonitor(self.task,"FrequentNoResponse")
        self.task.runTask()
        summary = self.task.responses.getSummaryStatsFields()
        self.assertEqual(summary['shape_corr'],18)
        self.assertEqual(summary['color_corr'],18)
        self.assertEqual(summary['shift_corr'],58)
        self.assertEqual(self.task.responses.count,122)
    

class TestSetShiftingCalc(unittest.TestCase):
    """Test cases for the summary calculations for the SetShifting Task.
    
    """
    def setUp(self):
        """create a standard set shifting task for unit tests."""
        testConfig = lavatask.base.Configuration(['../../lavatask.cfg','Test.cfg'])
        self.task = examiner.setshifting.SetShiftingTask(testConfig) 
        self.task.sessionNum = "Calculations"
        self.task.subjectId = "TestSetShifting"
        self.task.initializeTask()
        
    
    def test_calculation01(self):
        """Test calculations: test summary stats when no responses present."""
        responses = self.task.responses
        summary = responses.getSummaryStatsFields()
        self.assertEqual(round(summary['shift_score'],3),-5)
        self.assertEqual(summary['shift_error_diff'],-5)
        self.assertEqual(summary['total_trials'],0)
        self.assertEqual(summary['color_corr'],0)
        self.assertEqual(summary['color_errors'],0)
        self.assertEqual(summary['color_median'],-5)
        self.assertEqual(summary['color_mean'],-5)
        self.assertEqual(summary['color_stdev'],-5)
        self.assertEqual(summary['shape_corr'],0)
        self.assertEqual(summary['shape_errors'],0)
        self.assertEqual(summary['shape_median'],-5)
        self.assertEqual(summary['shape_mean'],-5)
        self.assertEqual(summary['shape_stdev'],-5)
        self.assertEqual(summary['shift_corr'],0)
        self.assertEqual(summary['shift_errors'],0)
        self.assertEqual(summary['shift_median'],-5)
        self.assertEqual(summary['shift_mean'],-5)
        self.assertEqual(summary['shift_stdev'],-5)
        self.assertEqual(summary['shifted_corr'],0)
        self.assertEqual(summary['shifted_errors'],0)
        self.assertEqual(summary['shifted_median'],-5)
        self.assertEqual(summary['shifted_mean'],-5)
        self.assertEqual(summary['shifted_stdev'],-5)
        self.assertEqual(summary['nonshifted_corr'],0)
        self.assertEqual(summary['nonshifted_errors'],0)
        self.assertEqual(summary['nonshifted_median'],-5)
        self.assertEqual(summary['nonshifted_mean'],-5)
        self.assertEqual(summary['nonshifted_stdev'],-5)
        
    def test_calculation02(self):
        """Test calculations: test summary stats when all responses are correct and given at 1.2345 seconds."""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(True,10,10,16)
        lastCue = None
        shiftedCount = 0
        for trialData in testingBlock.trialHandler:
            response = examiner.setshifting.SetShiftingResponse()
            response.block=testingBlock
            response.trialData = trialData
            response.key=trialData.corr_resp
            response.rt=1.2345
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corr_resp):
                response.corr=1
            else:
                response.corr=0
            
            if( trialData.condition=='shift'):
                if(lastCue==None or lastCue==trialData.cue):
                    response.shift=0
                else:
                    response.shift=1
                    shiftedCount+=1
                lastCue = trialData.cue
            else:
                response.shift = 0
            
            responses.addResponse(response)
            
        summary = responses.getSummaryStatsFields()
        self.assertEqual(round(summary['shift_score'],3),7.104)
        self.assertEqual(summary['shift_error_diff'],0)
        self.assertEqual(summary['total_trials'],104)
        self.assertEqual(summary['color_corr'],20)
        self.assertEqual(summary['color_errors'],0)
        self.assertEqual(summary['color_median'],1.2345)
        self.assertEqual(summary['color_mean'],1.2345)
        self.assertEqual(summary['color_stdev'],0)
        self.assertEqual(summary['shape_corr'],20)
        self.assertEqual(summary['shape_errors'],0)
        self.assertEqual(summary['shape_median'],1.2345)
        self.assertEqual(summary['shape_mean'],1.2345)
        self.assertEqual(summary['shape_stdev'],0)
        self.assertEqual(summary['shift_corr'],64)
        self.assertEqual(summary['shift_errors'],0)
        self.assertEqual(summary['shift_median'],1.2345)
        self.assertEqual(summary['shift_mean'],1.2345)
        self.assertEqual(summary['shift_stdev'],0)
        self.assertEqual(summary['shifted_corr'],shiftedCount)
        self.assertEqual(summary['shifted_errors'],0)
        self.assertEqual(summary['shifted_median'],1.2345)
        self.assertEqual(summary['shifted_mean'],1.2345)
        self.assertEqual(summary['shifted_stdev'],0)
        self.assertEqual(summary['nonshifted_corr'],64-shiftedCount)
        self.assertEqual(summary['nonshifted_errors'],0)
        self.assertEqual(summary['nonshifted_median'],1.2345)
        self.assertEqual(summary['nonshifted_mean'],1.2345)
        self.assertEqual(summary['nonshifted_stdev'],0)
        
    def test_calculation03(self):
        """Test calculations: test summary stats when all responses are incorrect and given at 1.2345 seconds."""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(True,10,10,16)
        lastCue = None
        shiftedCount = 0
        for trialData in testingBlock.trialHandler:
            response = examiner.setshifting.SetShiftingResponse()
            response.block=testingBlock
            response.trialData = trialData
            response.rt=1.2345
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.trialData.corr_resp=='left'):
                response.key='right'
            else:
                response.key='left'
            response.corr=0
            
            if( trialData.condition=='shift'):
                if(lastCue==None or lastCue==trialData.cue):
                    response.shift=0
                else:
                    response.shift=1
                    shiftedCount+=1
                lastCue = trialData.cue
            else:
                response.shift = 0
            
            responses.addResponse(response)
            
        summary = responses.getSummaryStatsFields()
        
        self.assertEqual(round(summary['shift_score'],3),-5)
        self.assertEqual(summary['shift_error_diff'],24)
        self.assertEqual(summary['total_trials'],104)
        self.assertEqual(summary['color_corr'],0)
        self.assertEqual(summary['color_errors'],20)
        self.assertEqual(summary['color_median'],-5)
        self.assertEqual(summary['color_mean'],-5)
        self.assertEqual(summary['color_stdev'],-5)
        self.assertEqual(summary['shape_corr'],0)
        self.assertEqual(summary['shape_errors'],20)
        self.assertEqual(summary['shape_median'],-5)
        self.assertEqual(summary['shape_mean'],-5)
        self.assertEqual(summary['shape_stdev'],-5)
        self.assertEqual(summary['shift_corr'],0)
        self.assertEqual(summary['shift_errors'],64)
        self.assertEqual(summary['shift_median'],-5)
        self.assertEqual(summary['shift_mean'],-5)
        self.assertEqual(summary['shift_stdev'],-5)
        self.assertEqual(summary['shifted_corr'],0)
        self.assertEqual(summary['shifted_errors'],shiftedCount)
        self.assertEqual(summary['shifted_median'],-5)
        self.assertEqual(summary['shifted_mean'],-5)
        self.assertEqual(summary['shifted_stdev'],-5)
        self.assertEqual(summary['nonshifted_corr'],0)
        self.assertEqual(summary['nonshifted_errors'],64-shiftedCount)
        self.assertEqual(summary['nonshifted_median'],-5)
        self.assertEqual(summary['nonshifted_mean'],-5)
        self.assertEqual(summary['nonshifted_stdev'],-5)
       
       
    def test_calculation04(self):
        """Test calculations: test summary stats when all responses are correct and left are at 1.1111 seconds and right are at 3.3333"""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(True,10,10,16)
        lastCue = None
        shiftedCount = 0
        for trialData in testingBlock.trialHandler:
            response = examiner.setshifting.SetShiftingResponse()
            response.block=testingBlock
            response.trialData = trialData
            response.key=response.trialData.corr_resp
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.trialData.corr_resp=='left'):
                response.rt=1.1111
            else:
                response.rt=3.3333
            response.corr=1
            
            if( trialData.condition=='shift'):
                if(lastCue==None or lastCue==trialData.cue):
                    response.shift=0
                else:
                    response.shift=1
                    shiftedCount+=1
                lastCue = trialData.cue
            else:
                response.shift = 0
            
            responses.addResponse(response)
            
        summary = responses.getSummaryStatsFields()
        
        self.assertEqual(round(summary['shift_score'],3),5.594)
        self.assertEqual(summary['shift_error_diff'],0)
        self.assertEqual(summary['total_trials'],104)
        self.assertEqual(summary['color_corr'],20)
        self.assertEqual(summary['color_errors'],0)
        self.assertEqual(summary['color_median'],2.2222)
        self.assertEqual(summary['color_mean'],2.2222)
        self.assertEqual(summary['color_stdev'],1.1111)
        self.assertEqual(summary['shape_corr'],20)
        self.assertEqual(summary['shape_errors'],0)
        self.assertEqual(summary['shape_median'],2.2222)
        self.assertEqual(summary['shape_mean'],2.2222)
        self.assertEqual(summary['shape_stdev'],1.1111)
        self.assertEqual(summary['shift_corr'],64)
        self.assertEqual(summary['shift_errors'],0)
        self.assertEqual(summary['shift_median'],2.2222)
        self.assertEqual(summary['shift_mean'],2.2222)
        self.assertEqual(summary['shift_stdev'],1.1111)
        self.assertEqual(summary['shifted_corr'],shiftedCount)
        self.assertEqual(summary['shifted_errors'],0)
        self.assertEqual(summary['nonshifted_corr'],64-shiftedCount)
        self.assertEqual(summary['nonshifted_errors'],0)
         
    def test_calculation05(self):
        """Test calculations: test summary stats when all responses are correct and shifted are at 1.1111 seconds and nonshifted are at 3.3333"""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(True,10,10,16)
        lastCue = None
        shiftedCount = 0
        for trialData in testingBlock.trialHandler:
            response = examiner.setshifting.SetShiftingResponse()
            response.block=testingBlock
            response.trialData = trialData
            response.key=response.trialData.corr_resp
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            response.corr=1
            
            if( trialData.condition=='shift'):
                if(lastCue==None or lastCue==trialData.cue):
                    response.shift=0
                    response.rt=3.3333
                else:
                    response.shift=1
                    response.rt=1.1111
                    shiftedCount+=1
                lastCue = trialData.cue
            else:
                response.shift = 0
                response.rt = 3.3333
                    
            responses.addResponse(response)
            
        summary = responses.getSummaryStatsFields()
        
        #self.assertEqual(round(summary['shift_score'],3),)  can't determine from test harness.
        self.assertEqual(summary['shift_error_diff'],0)
        self.assertEqual(summary['total_trials'],104)
        self.assertEqual(summary['color_corr'],20)
        self.assertEqual(summary['color_errors'],0)
        self.assertEqual(summary['color_median'],3.3333)
        self.assertEqual(summary['color_mean'],3.3333)
        self.assertEqual(summary['color_stdev'],0)
        self.assertEqual(summary['shape_corr'],20)
        self.assertEqual(summary['shape_errors'],0)
        self.assertEqual(summary['shape_median'],3.3333)
        self.assertEqual(summary['shape_mean'],3.3333)
        self.assertEqual(summary['shape_stdev'],0)
        self.assertEqual(summary['shift_corr'],64)
        self.assertEqual(summary['shift_errors'],0)
        self.assertEqual(summary['shifted_corr'],shiftedCount)
        self.assertEqual(summary['shifted_errors'],0)
        self.assertEqual(summary['shifted_median'],1.1111)
        self.assertEqual(summary['shifted_mean'],1.1111)
        self.assertEqual(summary['shifted_stdev'],0)
        self.assertEqual(summary['nonshifted_corr'],64-shiftedCount)
        self.assertEqual(summary['nonshifted_errors'],0)
        self.assertEqual(summary['nonshifted_median'],3.3333)
        self.assertEqual(summary['nonshifted_mean'],3.3333)
        self.assertEqual(summary['nonshifted_stdev'],0)

    def test_calculation06(self):
        """Test calculations: test summary stats when all responses are left at 2.0000 seconds"""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(True,10,10,16)
        lastCue = None
        shiftedCount = 0
        shiftedLeftCount = 0
        for trialData in testingBlock.trialHandler:
            response = examiner.setshifting.SetShiftingResponse()
            response.block=testingBlock
            response.trialData = trialData
            response.key="left"
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            response.corr=1
            response.rt=2.0000
            
            if(response.trialData.corr_resp == 'left'):
                response.corr=1
            else:
                response.corr=0
                
            if( trialData.condition=='shift'):
                if(lastCue==None or lastCue==trialData.cue):
                    response.shift=0
                else:
                    response.shift=1
                    shiftedCount+=1
                    if(response.trialData.corr_resp=='left'):
                        shiftedLeftCount+=1
                lastCue = trialData.cue
            else:
                response.shift = 0
                    
            responses.addResponse(response)
            
        summary = responses.getSummaryStatsFields()
        
        self.assertEqual(round(summary['shift_score'],3),3.365)
        self.assertEqual(summary['shift_error_diff'],12)
        self.assertEqual(summary['total_trials'],104)
        self.assertEqual(summary['color_corr'],10)
        self.assertEqual(summary['color_errors'],10)
        self.assertEqual(summary['color_median'],2.0000)
        self.assertEqual(summary['color_mean'],2.0000)
        self.assertEqual(summary['color_stdev'],0)
        self.assertEqual(summary['shape_corr'],10)
        self.assertEqual(summary['shape_errors'],10)
        self.assertEqual(summary['shape_median'],2.0000)
        self.assertEqual(summary['shape_mean'],2.0000)
        self.assertEqual(summary['shape_stdev'],0)
        self.assertEqual(summary['shift_corr'],32)
        self.assertEqual(summary['shift_errors'],32)
        self.assertEqual(summary['shift_median'],2.0000)
        self.assertEqual(summary['shift_mean'],2.0000)
        self.assertEqual(summary['shift_stdev'],0)
        self.assertEqual(summary['shifted_corr'],shiftedLeftCount)
        self.assertEqual(summary['shifted_errors'],shiftedCount - shiftedLeftCount)
        self.assertEqual(summary['shifted_median'],2.0000)
        self.assertEqual(summary['shifted_mean'],2.0000)
        self.assertEqual(summary['shifted_stdev'],0)
        self.assertEqual(summary['nonshifted_corr'],32 - shiftedLeftCount)
        self.assertEqual(summary['nonshifted_errors'],32 - (shiftedCount - shiftedLeftCount))
        self.assertEqual(summary['nonshifted_median'],2.0000)
        self.assertEqual(summary['nonshifted_mean'],2.0000)
        self.assertEqual(summary['nonshifted_stdev'],0)

    def test_calculation07(self):
        """Test calculations: test summary stats when all responses are left at 3.0000 seconds"""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(True,10,10,16)
        lastCue = None
        shiftedCount = 0
        shiftedLeftCount = 0
        for trialData in testingBlock.trialHandler:
            response = examiner.setshifting.SetShiftingResponse()
            response.block=testingBlock
            response.trialData = trialData
            response.key="left"
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            response.corr=1
            response.rt=3.0000
            
            if(response.trialData.corr_resp == 'left'):
                response.corr=1
            else:
                response.corr=0
                
            if( trialData.condition=='shift'):
                if(lastCue==None or lastCue==trialData.cue):
                    response.shift=0
                else:
                    response.shift=1
                    shiftedCount+=1
                    if(response.trialData.corr_resp=='left'):
                        shiftedLeftCount+=1
                lastCue = trialData.cue
            else:
                response.shift = 0
                    
            responses.addResponse(response)
            
        summary = responses.getSummaryStatsFields()
        self.assertEqual(round(summary['shift_score'],3),2.5)
        self.assertEqual(summary['shift_error_diff'],12)
        self.assertEqual(summary['total_trials'],104)
        self.assertEqual(summary['color_corr'],10)
        self.assertEqual(summary['color_errors'],10)
        self.assertEqual(summary['color_median'],3.0000)
        self.assertEqual(summary['color_mean'],3.0000)
        self.assertEqual(summary['color_stdev'],0)
        self.assertEqual(summary['shape_corr'],10)
        self.assertEqual(summary['shape_errors'],10)
        self.assertEqual(summary['shape_median'],3.0000)
        self.assertEqual(summary['shape_mean'],3.0000)
        self.assertEqual(summary['shape_stdev'],0)
        self.assertEqual(summary['shift_corr'],32)
        self.assertEqual(summary['shift_errors'],32)
        self.assertEqual(summary['shift_median'],3.0000)
        self.assertEqual(summary['shift_mean'],3.0000)
        self.assertEqual(summary['shift_stdev'],0)
        self.assertEqual(summary['shifted_corr'],shiftedLeftCount)
        self.assertEqual(summary['shifted_errors'],shiftedCount - shiftedLeftCount)
        self.assertEqual(summary['shifted_median'],3.0000)
        self.assertEqual(summary['shifted_mean'],3.0000)
        self.assertEqual(summary['shifted_stdev'],0)
        self.assertEqual(summary['nonshifted_corr'],32 - shiftedLeftCount)
        self.assertEqual(summary['nonshifted_errors'],32 - (shiftedCount - shiftedLeftCount))
        self.assertEqual(summary['nonshifted_median'],3.0000)
        self.assertEqual(summary['nonshifted_mean'],3.0000)
        self.assertEqual(summary['nonshifted_stdev'],0)



    def test_calculation08(self):
        """Test calculations: test summary stats when all responses are left at .3000 seconds"""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(True,10,10,16)
        lastCue = None
        shiftedCount = 0
        shiftedLeftCount = 0
        for trialData in testingBlock.trialHandler:
            response = examiner.setshifting.SetShiftingResponse()
            response.block=testingBlock
            response.trialData = trialData
            response.key="left"
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            response.corr=1
            response.rt=0.300
            
            if(response.trialData.corr_resp == 'left'):
                response.corr=1
            else:
                response.corr=0
                
            if( trialData.condition=='shift'):
                if(lastCue==None or lastCue==trialData.cue):
                    response.shift=0
                else:
                    response.shift=1
                    shiftedCount+=1
                    if(response.trialData.corr_resp=='left'):
                        shiftedLeftCount+=1
                lastCue = trialData.cue
            else:
                response.shift = 0
                    
            responses.addResponse(response)
            
        summary = responses.getSummaryStatsFields()
        self.assertEqual(round(summary['shift_score'],3),7.5)
        self.assertEqual(summary['shift_error_diff'],12)
        self.assertEqual(summary['total_trials'],104)
        self.assertEqual(summary['color_corr'],10)
        self.assertEqual(summary['color_errors'],10)
        self.assertEqual(summary['color_median'],.3000)
        self.assertEqual(summary['color_mean'],.3000)
        self.assertEqual(summary['color_stdev'],0)
        self.assertEqual(summary['shape_corr'],10)
        self.assertEqual(summary['shape_errors'],10)
        self.assertEqual(summary['shape_median'],.3000)
        self.assertEqual(summary['shape_mean'],.3000)
        self.assertEqual(summary['shape_stdev'],0)
        self.assertEqual(summary['shift_corr'],32)
        self.assertEqual(summary['shift_errors'],32)
        self.assertEqual(summary['shift_median'],.3000)
        self.assertEqual(summary['shift_mean'],.3000)
        self.assertEqual(summary['shift_stdev'],0)
        self.assertEqual(summary['shifted_corr'],shiftedLeftCount)
        self.assertEqual(summary['shifted_errors'],shiftedCount - shiftedLeftCount)
        self.assertEqual(summary['shifted_median'],.3000)
        self.assertEqual(summary['shifted_mean'],.3000)
        self.assertEqual(summary['shifted_stdev'],0)
        self.assertEqual(summary['nonshifted_corr'],32 - shiftedLeftCount)
        self.assertEqual(summary['nonshifted_errors'],32 - (shiftedCount - shiftedLeftCount))
        self.assertEqual(summary['nonshifted_median'],.3000)
        self.assertEqual(summary['nonshifted_mean'],.3000)
        self.assertEqual(summary['nonshifted_stdev'],0)



class TestSetShiftingVariations(unittest.TestCase):
    """Test cases for the Set Shifting task application flow and output files,
    
    """
    def setUp(self):
        """create a sped up timer for tasks"""
        testConfig = lavatask.base.Configuration(['../../lavatask.cfg','Test.cfg'])
        self.task = examiner.setshifting.SetShiftingTask(testConfig)
        self.task.taskClockFactory = lavatask.base.TestingTaskClockFactory(50.000)
        self.task.recordScreenShots = True
          
    def test_EnglishAdult(self):
        """Test English Adult Set Shifting, fail the first and second practice."""
        self.task.sessionNum = "EnglishAdult"
        self.task.subjectId = "TestSetShifting"
        self.task.defaultResponseMonitor = TestSetShiftingResponseMonitor(self.task,"FailSecondPractice")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,154)

    def test_SpanishAdult(self):
        """Test Spanish Adult Set Shifting, fail the first and second practice."""
        self.task.sessionNum = "SpanishAdult"
        self.task.subjectId = "TestSetShifting"
        self.task.defaultResponseMonitor = TestSetShiftingResponseMonitor(self.task,"FailSecondPractice")
        self.task.language = 'Spanish'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,154)

    def test_HebrewAdult(self):
        """Test Hebrew Adult Set Shifting, fail the first and second practice."""
        self.task.sessionNum = "HebrewAdult"
        self.task.subjectId = "TestSetShifting"
        self.task.defaultResponseMonitor = TestSetShiftingResponseMonitor(self.task,"FailSecondPractice")
        self.task.language = 'Hebrew'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,154)

    def test_EnglishChild(self):
        """Test English Child Set Shifting, fail the first and second practice."""
        self.task.sessionNum = "EnglishChild"
        self.task.subjectId = "TestSetShifting"
        self.task.defaultResponseMonitor = TestSetShiftingResponseMonitor(self.task,"FailSecondPractice")
        self.task.ageCohort = 'Child'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,154)

    def test_SpanishChild(self):
        """Test Spanish Child Set Shifting, fail the first and second practice."""
        self.task.sessionNum = "SpanishChild"
        self.task.subjectId = "TestSetShifting"
        self.task.defaultResponseMonitor = TestSetShiftingResponseMonitor(self.task,"FailSecondPractice")
        self.task.language = 'Spanish'
        self.task.ageCohort = 'Child'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,154)

    def test_HebrewChild(self):
        """Test Hebrew Child Set Shifting, fail the first and second practice."""
        self.task.sessionNum = "HebrewChild"
        self.task.subjectId = "TestSetShifting"
        self.task.defaultResponseMonitor = TestSetShiftingResponseMonitor(self.task,"FailSecondPractice")
        self.task.language = 'Hebrew'
        self.task.ageCohort = 'Child'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,154)

def runCalcTests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSetShiftingCalc)
    unittest.TextTestRunner(verbosity=2).run(suite)

def runFlowTests():
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSetShiftingFlowAndOutput)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
def runVariationsTests():
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSetShiftingVariations)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
   runCalcTests()
   runFlowTests()
   runVariationsTests()
    