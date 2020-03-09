#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Class library that provides unit testing classes for the Flanker computer based task

:Classes:
    TestFlankerCalc - test cases for the summary calculations for the Flanker Task
    TestFlankerFlowAndOutput - test cases for the practice trials flow. 
    TestFlankerResponseMonitor - custom response provider for flanker testing
    
    
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
import examiner.flanker


class TestFlankerResponseMonitor(lavatask.base.ResponseMonitor):
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
            if(block.getTime()-block.currentTrialFixation >= .2):
                block.lastResponse = block.currentTrial.corrAns
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
            if(block.getTime()-block.currentTrialFixation >= .2):
                if(block.currentTrial.corrAns == "left"):
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
            if(block.getTime()-block.currentTrialFixation >= .2):
                block.lastResponse = "left"
                block.lastResponseTime = block.getTime()
                return True
        elif(block.name in ["secondPracticeBlock","thirdPracticeBlock","throwawayBlock","testingBlock"]):
            if(block.getTime()-block.currentTrialFixation >= .2):
                block.lastResponse = block.currentTrial.corrAns
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
            if(block.getTime()-block.currentTrialFixation >= .2):
                block.lastResponse = "left"
                block.lastResponseTime = block.getTime()
                return True
        elif(block.name in ["thirdPracticeBlock","throwawayBlock","testingBlock"]):
            if(block.getTime()-block.currentTrialFixation >= .2):
                block.lastResponse = block.currentTrial.corrAns
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
            if(block.getTime()-block.currentTrialFixation >= .2):
                block.lastResponse = block.currentTrial.corrAns
                block.lastResponseTime = block.getTime()
                return True
        elif(block.name in ["secondPracticeBlock","thirdPracticeBlock","throwawayBlock","testingBlock"]):
            if(block.getTime()-block.currentTrialFixation >= .2):
                if(block.currentTrial.corrAns == "left" and block.currentTrial.upDown == "up"):
                    return False #simulate no response
                else:
                    block.lastResponse = block.currentTrial.corrAns
                    block.lastResponseTime = block.getTime()
                    return True
        else:
            if(block.getTime() > .5):
                block.lastResponse = "space"
                block.lastResponseTime = block.getTime()
                return True
    


class TestFlankerFlowAndOutput(unittest.TestCase):
    """Test cases for the Flanker task application flow and output files,
    
    """
    
    def setUp(self):
        """create a sped up timer for tasks"""
        testConfig = lavatask.base.Configuration(['../../lavatask.cfg','Test.cfg'])
        self.task = examiner.flanker.FlankerTask(testConfig)
        self.task.taskClockFactory = lavatask.base.TestingTaskClockFactory(50.000)

    
    def test_AllCorrectEnglishAdult(self):
        """Test flanker flow when all responses correct"""
        self.task.sessionNum = "AllCorrect"
        self.task.subjectId = "TestFlanker"
        self.task.defaultResponseMonitor = TestFlankerResponseMonitor(self.task,"AllCorrect")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,58)
    
    def test_FailFirstPracticeEnglishAdult(self):
        """Test flanker fail the first practice"""
        self.task.sessionNum = "FailFirstPractice"
        self.task.subjectId = "TestFlanker"
        self.task.defaultResponseMonitor = TestFlankerResponseMonitor(self.task,"FailFirstPractice")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,66)
        
    def test_FailSecondPracticeEnglishAdult(self):
        """Test flanker flow, fail the first and second practice."""
        self.task.sessionNum = "FailSecondPractice"
        self.task.subjectId = "TestFlanker"
        self.task.defaultResponseMonitor = TestFlankerResponseMonitor(self.task,"FailSecondPractice")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,74)
    
    def test_FailAllPracticeEnglishAdult(self):
        """Test flanker flow, fail all practice."""
        self.task.sessionNum = "FailAllPractice"
        self.task.subjectId = "TestFlanker"
        self.task.defaultResponseMonitor = TestFlankerResponseMonitor(self.task,"FailAllPractice")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,24)
        
    def test_FrequentNoResponseEnglishAdult(self):
        """Test no response functionality."""
        self.task.sessionNum = "FrequentNoResponse"
        self.task.subjectId = "TestFlanker"
        self.task.defaultResponseMonitor = TestFlankerResponseMonitor(self.task,"FrequentNoResponse")
        self.task.runTask()
        summary = self.task.responses.getSummaryStatsFields()
        self.assertEqual(summary['total_corr'],36)
        self.assertEqual(summary['incongr_corr'],18)
        self.assertEqual(summary['congr_corr'],18)
        self.assertEqual(summary['right_corr'],24)
        self.assertEqual(summary['left_corr'],12)
        self.assertEqual(summary['up_corr'],12)
        self.assertEqual(summary['down_corr'],24)
        self.assertEqual(self.task.responses.count,58)
    

class TestFlankerCalc(unittest.TestCase):
    """Test cases for the summary calculations for the Flanker Task.
    
    """
    def setUp(self):
        """create a standard flanker task for unit tests."""
        testConfig = lavatask.base.Configuration(['../../lavatask.cfg','Test.cfg'])
        self.task = examiner.flanker.FlankerTask(testConfig)
        self.task.sessionNum = "Calculations"
        self.task.subjectId = "TestFlanker"
        self.task.initializeTask()
        
    
    def test_calculation01(self):
        """Test calculations: test summary stats when no responses present."""
        responses = self.task.responses
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['flanker_score'],-5)
        self.assertEqual(summary['flanker_error_diff'],-5)
        self.assertEqual(summary['total_corr'],0)
        self.assertEqual(summary['total_corr'],0)
        self.assertEqual(summary['total_median'],-5)
        self.assertEqual(summary['total_mean'],-5)
        self.assertEqual(summary['total_stdev'],-5)
        self.assertEqual(summary['incongr_corr'],0)
        self.assertEqual(summary['incongr_median'],-5)
        self.assertEqual(summary['incongr_mean'],-5)
        self.assertEqual(summary['incongr_stdev'],-5)
        self.assertEqual(summary['congr_corr'],0)
        self.assertEqual(summary['congr_median'],-5)
        self.assertEqual(summary['congr_mean'],-5)
        self.assertEqual(summary['congr_stdev'],-5)
        self.assertEqual(summary['left_corr'],0)
        self.assertEqual(summary['left_median'],-5)
        self.assertEqual(summary['left_mean'],-5)
        self.assertEqual(summary['left_stdev'],-5)
        self.assertEqual(summary['right_corr'],0)
        self.assertEqual(summary['right_median'],-5)
        self.assertEqual(summary['right_mean'],-5)
        self.assertEqual(summary['right_stdev'],-5)
        self.assertEqual(summary['up_corr'],0)
        self.assertEqual(summary['up_median'],-5)
        self.assertEqual(summary['up_mean'],-5)
        self.assertEqual(summary['up_stdev'],-5)
        self.assertEqual(summary['down_corr'],0)
        self.assertEqual(summary['down_median'],-5)
        self.assertEqual(summary['down_mean'],-5)
        self.assertEqual(summary['down_stdev'],-5)
    
    def test_calculation02(self):
        """Test calculations: test summary stats when all responses are correct and given at 1.2345 seconds."""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(6)
        for trialData in testingBlock.trialHandler:
            response = examiner.flanker.FlankerResponse()
            response.block=testingBlock
            response.trialData = trialData
            response.fixation = 0 #not needed for calc testing
            response.key=trialData.corrAns
            response.rt=1.2345
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corrAns):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['flanker_score'],7.478)
        self.assertEqual(summary['flanker_error_diff'],0)
        self.assertEqual(summary['total_corr'],48)
        self.assertEqual(summary['total_median'],1.2345)
        self.assertEqual(summary['total_mean'],1.2345)
        self.assertEqual(summary['total_stdev'],0)
        self.assertEqual(summary['incongr_corr'],24)
        self.assertEqual(summary['incongr_median'],1.2345)
        self.assertEqual(summary['incongr_mean'],1.2345)
        self.assertEqual(summary['incongr_stdev'],0)
        self.assertEqual(summary['congr_corr'],24)
        self.assertEqual(summary['congr_median'],1.2345)
        self.assertEqual(summary['congr_mean'],1.2345)
        self.assertEqual(summary['congr_stdev'],0)
        self.assertEqual(summary['left_corr'],24)
        self.assertEqual(summary['left_median'],1.2345)
        self.assertEqual(summary['left_mean'],1.2345)
        self.assertEqual(summary['left_stdev'],0)
        self.assertEqual(summary['right_corr'],24)
        self.assertEqual(summary['right_median'],1.2345)
        self.assertEqual(summary['right_mean'],1.2345)
        self.assertEqual(summary['right_stdev'],0)
        self.assertEqual(summary['up_corr'],24)
        self.assertEqual(summary['up_median'],1.2345)
        self.assertEqual(summary['up_mean'],1.2345)
        self.assertEqual(summary['up_stdev'],0)
        self.assertEqual(summary['down_corr'],24)
        self.assertEqual(summary['down_median'],1.2345)
        self.assertEqual(summary['down_mean'],1.2345)
        self.assertEqual(summary['down_stdev'],0)
    
    def test_calculation03(self):
        """Test calculations: test summary stats when all responses are incorrect and given at 1.2345 seconds."""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(6)
        for trialData in testingBlock.trialHandler:
            response = examiner.flanker.FlankerResponse()
            response.block=testingBlock
            response.trialData = trialData
            response.fixation = 0 #not needed for calc testing
            if(trialData.corrAns=="left"):
                response.key = "right"
            else:
                response.key = "left"
            response.rt=1.2345
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corrAns):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['flanker_score'],-5)
        self.assertEqual(summary['flanker_error_diff'],0)
        self.assertEqual(summary['total_corr'],0)
        self.assertEqual(summary['total_median'],-5)
        self.assertEqual(summary['total_mean'],-5)
        self.assertEqual(summary['total_stdev'],-5)
        self.assertEqual(summary['incongr_corr'],0)
        self.assertEqual(summary['incongr_median'],-5)
        self.assertEqual(summary['incongr_mean'],-5)
        self.assertEqual(summary['incongr_stdev'],-5)
        self.assertEqual(summary['congr_corr'],0)
        self.assertEqual(summary['congr_median'],-5)
        self.assertEqual(summary['congr_mean'],-5)
        self.assertEqual(summary['congr_stdev'],-5)
        self.assertEqual(summary['left_corr'],0)
        self.assertEqual(summary['left_median'],-5)
        self.assertEqual(summary['left_mean'],-5)
        self.assertEqual(summary['left_stdev'],-5)
        self.assertEqual(summary['right_corr'],0)
        self.assertEqual(summary['right_median'],-5)
        self.assertEqual(summary['right_mean'],-5)
        self.assertEqual(summary['right_stdev'],-5)
        self.assertEqual(summary['up_corr'],0)
        self.assertEqual(summary['up_median'],-5)
        self.assertEqual(summary['up_mean'],-5)
        self.assertEqual(summary['up_stdev'],-5)
        self.assertEqual(summary['down_corr'],0)
        self.assertEqual(summary['down_median'],-5)
        self.assertEqual(summary['down_mean'],-5)
        self.assertEqual(summary['down_stdev'],-5)
    
    def test_calculation04(self):
        """Test calculations: test summary stats when all responses are correct and left are at 1.1111 seconds and right are at 3.3333"""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(6)
        for trialData in testingBlock.trialHandler:
            response = examiner.flanker.FlankerResponse()
            response.block=testingBlock
            response.trialData = trialData
            response.fixation = 0 #not needed for calc testing
            response.key = trialData.corrAns
            if(trialData.corrAns=="left"):
                response.rt=1.1111
            else:
                response.rt = 3.3333
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corrAns):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['flanker_score'],5.837)
        self.assertEqual(summary['flanker_error_diff'],0)
        self.assertEqual(summary['total_corr'],48)
        self.assertEqual(summary['total_median'],2.2222)
        self.assertEqual(summary['total_mean'],2.2222)
        self.assertEqual(summary['total_stdev'],1.1111)
        self.assertEqual(summary['incongr_corr'],24)
        self.assertEqual(summary['incongr_median'],2.2222)
        self.assertEqual(summary['incongr_mean'],2.2222)
        self.assertEqual(summary['incongr_stdev'],1.1111)
        self.assertEqual(summary['congr_corr'],24)
        self.assertEqual(summary['congr_median'],2.2222)
        self.assertEqual(summary['congr_mean'],2.2222)
        self.assertEqual(summary['congr_stdev'],1.1111)
        self.assertEqual(summary['left_corr'],24)
        self.assertEqual(summary['left_median'],1.1111)
        self.assertEqual(summary['left_mean'],1.1111)
        self.assertEqual(summary['left_stdev'],0)
        self.assertEqual(summary['right_corr'],24)
        self.assertEqual(summary['right_median'],3.3333)
        self.assertEqual(summary['right_mean'],3.3333)
        self.assertEqual(summary['right_stdev'],0)
        self.assertEqual(summary['up_corr'],24)
        self.assertEqual(summary['up_median'],2.2222)
        self.assertEqual(summary['up_mean'],2.2222)
        self.assertEqual(summary['up_stdev'],1.1111)
        self.assertEqual(summary['down_corr'],24)
        self.assertEqual(summary['down_median'],2.2222)
        self.assertEqual(summary['down_mean'],2.2222)
        self.assertEqual(summary['down_stdev'],1.1111)
        
    def test_calculation05(self):
        """Test calculations: test summary stats when all responses are correct and up are at 1.1111 seconds and down are at 3.3333"""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(6)
        for trialData in testingBlock.trialHandler:
            response = examiner.flanker.FlankerResponse()
            response.block=testingBlock
            response.trialData = trialData
            response.fixation = 0 #not needed for calc testing
            response.key = trialData.corrAns
            if(trialData.upDown=="up"):
                response.rt=1.1111
            else:
                response.rt = 3.3333
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corrAns):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['flanker_score'],5.837)
        self.assertEqual(summary['flanker_error_diff'],0)
        self.assertEqual(summary['total_corr'],48)
        self.assertEqual(summary['total_median'],2.2222)
        self.assertEqual(summary['total_mean'],2.2222)
        self.assertEqual(summary['total_stdev'],1.1111)
        self.assertEqual(summary['incongr_corr'],24)
        self.assertEqual(summary['incongr_median'],2.2222)
        self.assertEqual(summary['incongr_mean'],2.2222)
        self.assertEqual(summary['incongr_stdev'],1.1111)
        self.assertEqual(summary['congr_corr'],24)
        self.assertEqual(summary['congr_median'],2.2222)
        self.assertEqual(summary['congr_mean'],2.2222)
        self.assertEqual(summary['congr_stdev'],1.1111)
        self.assertEqual(summary['left_corr'],24)
        self.assertEqual(summary['left_median'],2.2222)
        self.assertEqual(summary['left_mean'],2.2222)
        self.assertEqual(summary['left_stdev'],1.1111)
        self.assertEqual(summary['right_corr'],24)
        self.assertEqual(summary['right_median'],2.2222)
        self.assertEqual(summary['right_mean'],2.2222)
        self.assertEqual(summary['right_stdev'],1.1111)
        self.assertEqual(summary['up_corr'],24)
        self.assertEqual(summary['up_median'],1.1111)
        self.assertEqual(summary['up_mean'],1.1111)
        self.assertEqual(summary['up_stdev'],0)
        self.assertEqual(summary['down_corr'],24)
        self.assertEqual(summary['down_median'],3.3333)
        self.assertEqual(summary['down_mean'],3.3333)
        self.assertEqual(summary['down_stdev'],0)
    
    def test_calculation06(self):
        """Test calculations: test summary stats when all responses are correct and congruent are at 1.1111 seconds and incongruent are at 3.3333"""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(6)
        for trialData in testingBlock.trialHandler:
            response = examiner.flanker.FlankerResponse()
            response.block=testingBlock
            response.trialData = trialData
            response.fixation = 0 #not needed for calc testing
            response.key = trialData.corrAns
            if(trialData.congruent==1):
                response.rt=1.1111
            else:
                response.rt = 3.3333
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corrAns):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['flanker_score'],5.0)
        self.assertEqual(summary['flanker_error_diff'],0)
        self.assertEqual(summary['total_corr'],48)
        self.assertEqual(summary['total_median'],2.2222)
        self.assertEqual(summary['total_mean'],2.2222)
        self.assertEqual(summary['total_stdev'],1.1111)
        self.assertEqual(summary['incongr_corr'],24)
        self.assertEqual(summary['incongr_median'],3.3333)
        self.assertEqual(summary['incongr_mean'],3.3333)
        self.assertEqual(summary['incongr_stdev'],0)
        self.assertEqual(summary['congr_corr'],24)
        self.assertEqual(summary['congr_median'],1.1111)
        self.assertEqual(summary['congr_mean'],1.1111)
        self.assertEqual(summary['congr_stdev'],0)
        self.assertEqual(summary['left_corr'],24)
        self.assertEqual(summary['left_median'],2.2222)
        self.assertEqual(summary['left_mean'],2.2222)
        self.assertEqual(summary['left_stdev'],1.1111)
        self.assertEqual(summary['right_corr'],24)
        self.assertEqual(summary['right_median'],2.2222)
        self.assertEqual(summary['right_mean'],2.2222)
        self.assertEqual(summary['right_stdev'],1.1111)
        self.assertEqual(summary['up_corr'],24)
        self.assertEqual(summary['up_median'],2.2222)
        self.assertEqual(summary['up_mean'],2.2222)
        self.assertEqual(summary['up_stdev'],1.1111)
        self.assertEqual(summary['down_corr'],24)
        self.assertEqual(summary['down_median'],2.2222)
        self.assertEqual(summary['down_mean'],2.2222)
        self.assertEqual(summary['down_stdev'],1.1111)
        
        
    def test_calculation07(self):
        """Test calculations: test summary stats when all responses are correct and congruent are at 3.3333 seconds and incongruent are at 1.1111"""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(6)
        for trialData in testingBlock.trialHandler:
            response = examiner.flanker.FlankerResponse()
            response.block=testingBlock
            response.trialData = trialData
            response.fixation = 0 #not needed for calc testing
            response.key = trialData.corrAns
            if(trialData.congruent==0):
                response.rt=1.1111
            else:
                response.rt = 3.3333
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corrAns):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['flanker_score'],7.772)
        self.assertEqual(summary['flanker_error_diff'],0)
        self.assertEqual(summary['total_corr'],48)
        self.assertEqual(summary['total_median'],2.2222)
        self.assertEqual(summary['total_mean'],2.2222)
        self.assertEqual(summary['total_stdev'],1.1111)
        self.assertEqual(summary['incongr_corr'],24)
        self.assertEqual(summary['incongr_median'],1.1111)
        self.assertEqual(summary['incongr_mean'],1.1111)
        self.assertEqual(summary['incongr_stdev'],0)
        self.assertEqual(summary['congr_corr'],24)
        self.assertEqual(summary['congr_median'],3.3333)
        self.assertEqual(summary['congr_mean'],3.3333)
        self.assertEqual(summary['congr_stdev'],0)
        self.assertEqual(summary['left_corr'],24)
        self.assertEqual(summary['left_median'],2.2222)
        self.assertEqual(summary['left_mean'],2.2222)
        self.assertEqual(summary['left_stdev'],1.1111)
        self.assertEqual(summary['right_corr'],24)
        self.assertEqual(summary['right_median'],2.2222)
        self.assertEqual(summary['right_mean'],2.2222)
        self.assertEqual(summary['right_stdev'],1.1111)
        self.assertEqual(summary['up_corr'],24)
        self.assertEqual(summary['up_median'],2.2222)
        self.assertEqual(summary['up_mean'],2.2222)
        self.assertEqual(summary['up_stdev'],1.1111)
        self.assertEqual(summary['down_corr'],24)
        self.assertEqual(summary['down_median'],2.2222)
        self.assertEqual(summary['down_mean'],2.2222)
        self.assertEqual(summary['down_stdev'],1.1111)
        
    def test_calculation08(self):
        """Test calculations: test summary stats when all responses are correct RT = 0"""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(6)
        for trialData in testingBlock.trialHandler:
            response = examiner.flanker.FlankerResponse()
            response.block=testingBlock
            response.trialData = trialData
            response.fixation = 0 #not needed for calc testing
            response.key = trialData.corrAns
            response.rt = 0
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corrAns):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['flanker_score'],10.000)
        self.assertEqual(summary['flanker_error_diff'],0)
        self.assertEqual(summary['total_corr'],48)
        self.assertEqual(summary['total_median'],0)
        self.assertEqual(summary['total_mean'],0)
        self.assertEqual(summary['total_stdev'],0)
        self.assertEqual(summary['incongr_corr'],24)
        self.assertEqual(summary['incongr_median'],0)
        self.assertEqual(summary['incongr_mean'],0)
        self.assertEqual(summary['incongr_stdev'],0)
        self.assertEqual(summary['congr_corr'],24)
        self.assertEqual(summary['congr_median'],0)
        self.assertEqual(summary['congr_mean'],0)
        self.assertEqual(summary['congr_stdev'],0)
        self.assertEqual(summary['left_corr'],24)
        self.assertEqual(summary['left_median'],0)
        self.assertEqual(summary['left_mean'],0)
        self.assertEqual(summary['left_stdev'],0)
        self.assertEqual(summary['right_corr'],24)
        self.assertEqual(summary['right_median'],0)
        self.assertEqual(summary['right_mean'],0)
        self.assertEqual(summary['right_stdev'],0)
        self.assertEqual(summary['up_corr'],24)
        self.assertEqual(summary['up_median'],0)
        self.assertEqual(summary['up_mean'],0)
        self.assertEqual(summary['up_stdev'],0)
        self.assertEqual(summary['down_corr'],24)
        self.assertEqual(summary['down_median'],0)
        self.assertEqual(summary['down_mean'],0)
        self.assertEqual(summary['down_stdev'],0)
        
    def test_calculation09(self):
        """Test calculations: test summary stats when all responses are correct and congruent are at 0.0001 seconds and incongruent are at 3.9999"""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(6)
        for trialData in testingBlock.trialHandler:
            response = examiner.flanker.FlankerResponse()
            response.block=testingBlock
            response.trialData = trialData
            response.fixation = 0 #not needed for calc testing
            response.key = trialData.corrAns
            if(trialData.congruent==1):
                response.rt=0.0001
            else:
                response.rt = 3.9999
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corrAns):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['flanker_score'],5.000)
        self.assertEqual(summary['flanker_error_diff'],0)
        self.assertEqual(summary['total_corr'],48)
        self.assertEqual(summary['total_median'],2.000)
        self.assertEqual(summary['total_mean'],2.000)
        self.assertEqual(summary['total_stdev'],1.9999)
        self.assertEqual(summary['incongr_corr'],24)
        self.assertEqual(summary['incongr_median'],3.9999)
        self.assertEqual(summary['incongr_mean'],3.9999)
        self.assertEqual(summary['incongr_stdev'],0)
        self.assertEqual(summary['congr_corr'],24)
        self.assertEqual(summary['congr_median'],0.0001)
        self.assertEqual(summary['congr_mean'],0.0001)
        self.assertEqual(summary['congr_stdev'],0)
        self.assertEqual(summary['left_corr'],24)
        self.assertEqual(summary['left_median'],2.0000)
        self.assertEqual(summary['left_mean'],2.0000)
        self.assertEqual(summary['left_stdev'],1.9999)
        self.assertEqual(summary['right_corr'],24)
        self.assertEqual(summary['right_median'],2.0000)
        self.assertEqual(summary['right_mean'],2.0000)
        self.assertEqual(summary['right_stdev'],1.9999)
        self.assertEqual(summary['up_corr'],24)
        self.assertEqual(summary['up_median'],2.0000)
        self.assertEqual(summary['up_mean'],2.0000)
        self.assertEqual(summary['up_stdev'],1.9999)
        self.assertEqual(summary['down_corr'],24)
        self.assertEqual(summary['down_median'],2.0000)
        self.assertEqual(summary['down_mean'],2.0000)
        self.assertEqual(summary['down_stdev'],1.9999)
        


    def test_calculation10(self):
        """Test calculations: test summary stats when all responses are left  and congruent are at 1.0000 seconds and incongruent are at 3.0000"""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(6)
        for trialData in testingBlock.trialHandler:
            response = examiner.flanker.FlankerResponse()
            response.block=testingBlock
            response.trialData = trialData
            response.fixation = 0 #not needed for calc testing
            response.key = "left"
            if(trialData.congruent==1):
                response.rt=1.0000
            else:
                response.rt = 3.0000
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corrAns):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
      
        self.assertEqual(summary['flanker_score'],2.5)
        self.assertEqual(summary['flanker_error_diff'],0)
        self.assertEqual(summary['total_corr'],24)
        self.assertEqual(summary['total_median'],2.0000)
        self.assertEqual(summary['total_mean'],2.0000)
        self.assertEqual(summary['total_stdev'],1.0000)
        self.assertEqual(summary['incongr_corr'],12)
        self.assertEqual(summary['incongr_median'],3.0000)
        self.assertEqual(summary['incongr_mean'],3.0000)
        self.assertEqual(summary['incongr_stdev'],0)
        self.assertEqual(summary['congr_corr'],12)
        self.assertEqual(summary['congr_median'],1.0000)
        self.assertEqual(summary['congr_mean'],1.0000)
        self.assertEqual(summary['congr_stdev'],0)
        self.assertEqual(summary['left_corr'],24)
        self.assertEqual(summary['left_median'],2.0000)
        self.assertEqual(summary['left_mean'],2.0000)
        self.assertEqual(summary['left_stdev'],1.0000)
        self.assertEqual(summary['right_corr'],0)
        self.assertEqual(summary['right_median'],-5)
        self.assertEqual(summary['right_mean'],-5)
        self.assertEqual(summary['right_stdev'],-5)
        self.assertEqual(summary['up_corr'],12)
        self.assertEqual(summary['up_median'],2.0000)
        self.assertEqual(summary['up_mean'],2.0000)
        self.assertEqual(summary['up_stdev'],1.0000)
        self.assertEqual(summary['down_corr'],12)
        self.assertEqual(summary['down_median'],2.0000)
        self.assertEqual(summary['down_mean'],2.0000)
        self.assertEqual(summary['down_stdev'],1.0000)
        
    def test_calculation11(self):
        """Test calculations: test summary stats when all incongruent up are incorrect, all others correct and all rt = .878"""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(6)
        for trialData in testingBlock.trialHandler:
            response = examiner.flanker.FlankerResponse()
            response.block=testingBlock
            response.trialData = trialData
            response.fixation = 0 #not needed for calc testing
            if(trialData.congruent==0 and trialData.upDown=='up'):
                response.corr = 0
            else:
                response.corr = 1
            response.rt = .878
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['flanker_score'],5.929)
        self.assertEqual(summary['flanker_error_diff'],12)
        self.assertEqual(summary['total_corr'],36)
        self.assertEqual(summary['total_median'],0.878)
        self.assertEqual(summary['total_mean'],0.878)
        self.assertEqual(summary['total_stdev'],0.000)
        self.assertEqual(summary['incongr_corr'],12)
        self.assertEqual(summary['incongr_median'],0.878)
        self.assertEqual(summary['incongr_mean'],0.878)
        self.assertEqual(summary['incongr_stdev'],0)
        self.assertEqual(summary['congr_corr'],24)
        self.assertEqual(summary['congr_median'],0.878)
        self.assertEqual(summary['congr_mean'],0.878)
        self.assertEqual(summary['congr_stdev'],0)
        self.assertEqual(summary['left_corr'],18)
        self.assertEqual(summary['left_median'],0.878)
        self.assertEqual(summary['left_mean'],0.878)
        self.assertEqual(summary['left_stdev'],0)
        self.assertEqual(summary['right_corr'],18)
        self.assertEqual(summary['right_median'],0.878)
        self.assertEqual(summary['right_mean'],0.878)
        self.assertEqual(summary['right_stdev'],0)
        self.assertEqual(summary['up_corr'],12)
        self.assertEqual(summary['up_median'],0.878)
        self.assertEqual(summary['up_mean'],0.878)
        self.assertEqual(summary['up_stdev'],0)
        self.assertEqual(summary['down_corr'],24)
        self.assertEqual(summary['down_median'],0.878)
        self.assertEqual(summary['down_mean'],0.878)
        self.assertEqual(summary['down_stdev'],0)

    def test_calculation12(self):
        """Test calculations: test summary stats when all incongruent up are incorrect, all others correct and all rt = .440"""
        responses = self.task.responses
        testingBlock = self.task.getBlockByName("testingBlock")
        testingBlock.initializeTrialData(6)
        for trialData in testingBlock.trialHandler:
            response = examiner.flanker.FlankerResponse()
            response.block=testingBlock
            response.trialData = trialData
            response.fixation = 0 #not needed for calc testing
            if(trialData.congruent==0 and trialData.upDown=='up'):
                response.corr = 0
            else:
                response.corr = 1
            response.rt = .440
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()

        self.assertEqual(summary['flanker_score'],7.500)
        self.assertEqual(summary['flanker_error_diff'],12)
        self.assertEqual(summary['total_corr'],36)
        self.assertEqual(summary['total_median'],0.440)
        self.assertEqual(summary['total_mean'],0.440)
        self.assertEqual(summary['total_stdev'],0.000)
        self.assertEqual(summary['incongr_corr'],12)
        self.assertEqual(summary['incongr_median'],0.440)
        self.assertEqual(summary['incongr_mean'],0.440)
        self.assertEqual(summary['incongr_stdev'],0)
        self.assertEqual(summary['congr_corr'],24)
        self.assertEqual(summary['congr_median'],0.440)
        self.assertEqual(summary['congr_mean'],0.440)
        self.assertEqual(summary['congr_stdev'],0)
        self.assertEqual(summary['left_corr'],18)
        self.assertEqual(summary['left_median'],0.440)
        self.assertEqual(summary['left_mean'],0.440)
        self.assertEqual(summary['left_stdev'],0)
        self.assertEqual(summary['right_corr'],18)
        self.assertEqual(summary['right_median'],0.440)
        self.assertEqual(summary['right_mean'],0.440)
        self.assertEqual(summary['right_stdev'],0)
        self.assertEqual(summary['up_corr'],12)
        self.assertEqual(summary['up_median'],0.440)
        self.assertEqual(summary['up_mean'],0.440)
        self.assertEqual(summary['up_stdev'],0)
        self.assertEqual(summary['down_corr'],24)
        self.assertEqual(summary['down_median'],0.440)
        self.assertEqual(summary['down_mean'],0.440)
        self.assertEqual(summary['down_stdev'],0)

class TestFlankerVariations(unittest.TestCase):
    """Test Variations of the Flanker task.
    
    """
    
    def setUp(self):
        """create a sped up timer for tasks"""
        testConfig = lavatask.base.Configuration(['../../lavatask.cfg','Test.cfg'])
        self.task = examiner.flanker.FlankerTask(testConfig)
        self.task.taskClockFactory = lavatask.base.TestingTaskClockFactory(50.000)
        self.task.recordScreenShots = True
    
        
    def test_EnglishAdult(self):
        """Test Adult English flanker, fail the first and second practice."""
        self.task.sessionNum = "AdultEnglish"
        self.task.subjectId = "TestFlanker"
        self.task.defaultResponseMonitor = TestFlankerResponseMonitor(self.task,"FailSecondPractice")
        self.task.language = 'English'
        self.task.ageCohort = 'Adult'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,74)

    def test_SpanishAdult(self):
        """Test Adult Spanish flanker, fail the first and second practice."""
        self.task.sessionNum = "AdultSpanish"
        self.task.subjectId = "TestFlanker"
        self.task.defaultResponseMonitor = TestFlankerResponseMonitor(self.task,"FailSecondPractice")
        self.task.language = 'Spanish'
        self.task.ageCohort = 'Adult'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,74)

    def test_HebrewAdult(self):
        """Test Adult Hebrew flanker, fail the first and second practice."""
        self.task.sessionNum = "AdultHebrew"
        self.task.subjectId = "TestFlanker"
        self.task.defaultResponseMonitor = TestFlankerResponseMonitor(self.task,"FailSecondPractice")
        self.task.language = 'Hebrew'
        self.task.ageCohort = 'Adult'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,74)

    def test_EnglishChild(self):
        """Test Child English flanker, fail the first and second practice."""
        self.task.sessionNum = "ChildEnglish"
        self.task.subjectId = "TestFlanker"
        self.task.defaultResponseMonitor = TestFlankerResponseMonitor(self.task,"FailSecondPractice")
        self.task.language = 'English'
        self.task.ageCohort = 'Child'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,74)

    def test_SpanishChild(self):
        """Test Child Spanish flanker, fail the first and second practice."""
        self.task.sessionNum = "ChildSpanish"
        self.task.subjectId = "TestFlanker"
        self.task.defaultResponseMonitor = TestFlankerResponseMonitor(self.task,"FailSecondPractice")
        self.task.language = 'Spanish'
        self.task.ageCohort = 'Child'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,74)

    def test_HebrewChild(self):
        """Test Child Hebrew flanker, fail the first and second practice."""
        self.task.sessionNum = "ChildHebrew"
        self.task.subjectId = "TestFlanker"
        self.task.defaultResponseMonitor = TestFlankerResponseMonitor(self.task,"FailSecondPractice")
        self.task.language = 'Hebrew'
        self.task.ageCohort = 'Child'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,74)

def runCalcTests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFlankerCalc)
    unittest.TextTestRunner(verbosity=2).run(suite)

def runFlowTests():
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFlankerFlowAndOutput)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
def runVariationsTests():
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFlankerVariations)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
   runCalcTests()
   runFlowTests()
   runVariationsTests()
    
  