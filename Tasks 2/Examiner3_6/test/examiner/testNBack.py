#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Class library that provides unit testing classes for the Nback computer based task

:Classes:
    TestNbackCalc - test cases for the summary calculations for the Nback Task
    TestNbackFlowAndOutput - test cases for the practice trials flow. 
    TestNbackResponseMonitor - custom response provider for flanker testing
    
    
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
import examiner.nback
from scipy.stats import norm

class TestNbackResponseMonitor(lavatask.base.ResponseMonitor):
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
        elif(self.responseMethod == "FailNB1FirstPractice"):
            return self.check_FailNB1FirstPractice(block)
        elif(self.responseMethod == "FailNB1SecondPractice"):
            return self.check_FailNB1SecondPractice(block)
        elif(self.responseMethod == "FailNB2FirstPractice"):
            return self.check_FailNB2FirstPractice(block)
        elif(self.responseMethod == "FailNB2SecondPractice"):
            return self.check_FailNB2SecondPractice(block)
        elif(self.responseMethod == "FailNB2AllPractice"):
            return self.check_FailNB2AllPractice(block)
        return False
    
    def check_AllCorrect(self,block):
        if(block.responseEnabled==False):return False
        
        if(block.name in ["nb1DemoBlock","nb1PracticeBlock","nb1Practice2Block","nb1TestingBlock","nb2DemoBlock","nb2PracticeBlock","nb2Practice2Block","nb2Practice3Block","nb2TestingBlock",]):
            if(block.getTime() >= .2):
                block.lastResponse = block.currentTrial.corr_resp
                block.lastResponseTime = block.getTime()
                return True
        else:
            if(block.getTime() > .5):
                block.lastResponse = "space"
                block.lastResponseTime = block.getTime()
                return True

    def check_FailNB2FirstPractice(self,block):
        if(block.responseEnabled==False):return False
        
        if(block.name in ["nb2PracticeBlock",]):
            if(block.getTime() >= .2):
                block.lastResponse = 'left'
                block.lastResponseTime = block.getTime()
                return True
        
        elif(block.name in ["nb1DemoBlock","nb1PracticeBlock","nb1Practice2Block","nb1TestingBlock","nb2DemoBlock","nb2Practice2Block","nb2Practice3Block","nb2TestingBlock",]):
            if(block.getTime() >= .2):
                block.lastResponse = block.currentTrial.corr_resp
                block.lastResponseTime = block.getTime()
                return True
        else:
            if(block.getTime() > .5):
                block.lastResponse = "space"
                block.lastResponseTime = block.getTime()
                return True
    
    def check_FailNB2SecondPractice(self,block):
        if(block.responseEnabled==False):return False
        
        if(block.name in ["nb2PracticeBlock","nb2Practice2Block",]):
            if(block.getTime() >= .2):
                block.lastResponse = 'left'
                block.lastResponseTime = block.getTime()
                return True
        
        elif(block.name in ["nb1DemoBlock","nb1PracticeBlock","nb1Practice2Block","nb1TestingBlock","nb2DemoBlock","nb2Practice3Block","nb2TestingBlock",]):
            if(block.getTime() >= .2):
                block.lastResponse = block.currentTrial.corr_resp
                block.lastResponseTime = block.getTime()
                return True
        else:
            if(block.getTime() > .5):
                block.lastResponse = "space"
                block.lastResponseTime = block.getTime()
                return True
    

        
    def check_FailNB2AllPractice(self,block):
        if(block.responseEnabled==False):return False
        
        if(block.name in ["nb2PracticeBlock","nb2Practice2Block","nb2Practice3Block",]):
            if(block.getTime() >= .2):
                block.lastResponse = 'left'
                block.lastResponseTime = block.getTime()
                return True
        
        elif(block.name in ["nb1DemoBlock","nb1PracticeBlock","nb1Practice2Block","nb1TestingBlock","nb2DemoBlock","nb2TestingBlock",]):
            if(block.getTime() >= .2):
                block.lastResponse = block.currentTrial.corr_resp
                block.lastResponseTime = block.getTime()
                return True
        else:
            if(block.getTime() > .5):
                block.lastResponse = "space"
                block.lastResponseTime = block.getTime()
                return True
   
    def check_FailNB1FirstPractice(self,block):
        if(block.responseEnabled==False):return False
        
        if(block.name in ["nb1PracticeBlock",]):
            if(block.getTime() >= .2):
                block.lastResponse = 'left'
                block.lastResponseTime = block.getTime()
                return True
        
        elif(block.name in ["nb1DemoBlock","nb1Practice2Block","nb1TestingBlock","nb2DemoBlock","nb2PracticeBlock","nb2Practice2Block","nb2Practice3Block","nb2TestingBlock",]):
            if(block.getTime() >= .2):
                block.lastResponse = block.currentTrial.corr_resp
                block.lastResponseTime = block.getTime()
                return True
        else:
            if(block.getTime() > .5):
                block.lastResponse = "space"
                block.lastResponseTime = block.getTime()
                return True
    
    def check_FailNB1SecondPractice(self,block):
        if(block.responseEnabled==False):return False
        
        if(block.name in ["nb1PracticeBlock","nb1Practice2Block",]):
            if(block.getTime() >= .2):
                block.lastResponse = 'left'
                block.lastResponseTime = block.getTime()
                return True
        
        elif(block.name in ["nb1DemoBlock","nb1TestingBlock","nb2DemoBlock","nb2PracticeBlock","nb2Practice2Block","nb2Practice3Block","nb2TestingBlock",]):
            if(block.getTime() >= .2):
                block.lastResponse = block.currentTrial.corr_resp
                block.lastResponseTime = block.getTime()
                return True
        else:
            if(block.getTime() > .5):
                block.lastResponse = "space"
                block.lastResponseTime = block.getTime()
                return True
    

        


class TestNbackFlowAndOutput(unittest.TestCase):
    """Test cases for the Nback task application flow and output files,
    
    """
    
    def setUp(self):
        """create a sped up timer for tasks"""
        testConfig = lavatask.base.Configuration(['../../lavatask.cfg','Test.cfg'])
        self.task = examiner.nback.NBackTask(testConfig)
        self.task.taskClockFactory = lavatask.base.TestingTaskClockFactory(50.000)

    def test_AllCorrectEnglishAdult(self):
        """Test Nback flow when all responses correct"""
        self.task.sessionNum = "AllCorrect"
        self.task.subjectId = "TestNBack"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"AllCorrect")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,169)
    
    def test_FailNB1FirstPracticeEnglishAdult(self):
        """Test Nback fail the first NB1 practice"""
        self.task.sessionNum = "FailNB1FirstPractice"
        self.task.subjectId = "TestNBack"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB1FirstPractice")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,180)
        
    def test_FailNB1SecondPracticeEnglishAdult(self):
        """Test Nback flow, fail the first and second NB1 practice."""
        self.task.sessionNum = "FailNB1SecondPractice"
        self.task.subjectId = "TestNBack"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB1SecondPractice")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,33)
   
    def test_FailNB2FirstPracticeEnglishAdult(self):
        """Test Nback fail the first NB2 practice"""
        self.task.sessionNum = "FailNB2FirstPractice"
        self.task.subjectId = "TestNBack"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB2FirstPractice")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,181)
        
    def test_FailNB2SecondPracticeEnglishAdult(self):
        """Test Nback flow, fail the first and second NB2 practice."""
        self.task.sessionNum = "FailNB2SecondPractice"
        self.task.subjectId = "TestNBack"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB2SecondPractice")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,193)
    
    def test_FailNB2AllPracticeEnglishAdult(self):
        """Test Nback flow, fail all practice."""
        self.task.sessionNum = "FailNB2AllPractice"
        self.task.subjectId = "TestNBack"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB2AllPractice")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,101)
            

class TestNbackCalc(unittest.TestCase):
    """Test cases for the summary calculations for the Nback Task.
    
    """
    def setUp(self):
        """create a standard flanker task for unit tests."""
        testConfig = lavatask.base.Configuration(['../../lavatask.cfg','Test.cfg'])
        self.task = examiner.nback.NBackTask(testConfig)
        self.task.sessionNum = "Calculations"
        self.task.subjectId = "TestNBack"
        self.task.initializeTask()
        
        self.nb1TestingBlock = self.task.getBlockByName("nb1TestingBlock")
        self.nb1TestingBlock.initializeTrialData('a',"testing")
        self.nb2TestingBlock = self.task.getBlockByName("nb2TestingBlock")
        self.nb2TestingBlock.initializeTrialData('a',"testing")
    
#    def testNormPPF(self):
#        """output norm.ppf values""" 
#        for i in range(30):
#            for j in range(10):
#                nb1_hits = ((j*10.000) +.500) / 101.000
#                nb1_nonmatch_corr = i
#                nb1_false_alarms = (((20.000 - nb1_nonmatch_corr)*5.000) + .500) / 101.000
#                nb1_z_fa = norm.ppf(nb1_false_alarms)
#                nb1_z_hit = norm.ppf(nb1_hits)
#                nb1_score = nb1_z_hit - nb1_z_fa
#                nb1_bias = (nb1_z_hit + nb1_z_fa) / 2.000
#                print "nb1 nonmatch="+str(i) + " and match=" + str(j)
#                print "      nb1 hits=" + str(nb1_hits)
#                print "      nb1 hits z=" + str(nb1_z_hit)
#                print "      nb1 false alarms=" + str(nb1_false_alarms)
#                print "      nb1 false alarms z=" + str(nb1_z_fa)
#                print "      nb1 bias = " + str(nb1_bias)
#                print "      nb1 score = " + str(nb1_score)
#    
#        for i in range(12,14):
#            for j in range(22,24):
#                nb2_hits = ((j*(100.000/30.000)) +.500) / 101.000
#                nb2_nonmatch_corr = i
#                nb2_false_alarms = (((60.000 - nb2_nonmatch_corr)*(100.000/60.000)) + .500) / 101.000
#                nb2_fa_part1 = (60.000 - nb2_nonmatch_corr)
#                nb2_fa_part2 = ((60.000 - nb2_nonmatch_corr)*(100.000/60.000))
#                
#                
#                nb2_z_fa = norm.ppf(nb2_false_alarms)
#                nb2_z_hit = norm.ppf(nb2_hits)
#                nb2_score = nb2_z_hit - nb2_z_fa
#                nb2_bias = (nb2_z_hit + nb2_z_fa) / 2.000
#                print "nb2 nonmatch="+str(i) + " and match=" + str(j)
#                print "      nb2 hits=" + str(nb2_hits)
#                print "      nb2 hits z=" + str(nb2_z_hit)
#                print "      nb2 false alarms1=" + str(nb2_fa_part1)
#                print "      nb2 false alarms2=" + str(nb2_fa_part2)
#                print "      nb2 false alarms=" + str(nb2_false_alarms)
#                print "      nb2 false alarms z=" + str(nb2_z_fa)
#                print "      nb2 bias = " + str(nb2_bias)
#                print "      nb2 score = " + str(nb2_score)
#    
#        
#    def printDPrimeCalcs(self,summary,test):
#        print "\n"
#        print test
#        print 'nb1_score=' + str(summary['nb1_score'] )
#        print 'nb1_bias='  + str(summary['nb1_bias'] )
#        print 'nb2_score=' + str(summary['nb2_score'] )
#        print 'nb2_bias=' + str(summary['nb2_bias'] )
#    
#    def printSummary(self,summary,test):
#        sorted_keys = summary.keys()
#        sorted_keys.sort()
#
#        print "\n"
#        print test
#        for key in sorted_keys:
#            print key + "=" + str(summary[key])
        
      
            
    def test_calculation01(self):
        """Test calculations: test summary stats when no responses present."""
        responses = self.task.responses
        summary = responses.getSummaryStatsFields()

        self.assertEqual(summary['nb1_total_trials'],0)
        self.assertEqual(summary['nb1_score'],-5)
        self.assertEqual(summary['nb1_bias'],-5)
        self.assertEqual(summary['nb1_corr'],0)
        self.assertEqual(summary['nb1_errors'],0)
        self.assertEqual(summary['nb1_mean'],-5)
        self.assertEqual(summary['nb1_median'],-5)
        self.assertEqual(summary['nb1_stdev'],-5)
        self.assertEqual(summary['nb1sm_corr'],0)
        self.assertEqual(summary['nb1sm_errors'],0)
        self.assertEqual(summary['nb1sm_mean'],-5)
        self.assertEqual(summary['nb1sm_median'],-5)
        self.assertEqual(summary['nb1sm_stdev'],-5)
        self.assertEqual(summary['nb1s1_corr'],0)
        self.assertEqual(summary['nb1s1_errors'],0)
        self.assertEqual(summary['nb1s1_mean'],-5)
        self.assertEqual(summary['nb1s1_median'],-5)
        self.assertEqual(summary['nb1s1_stdev'],-5)
        self.assertEqual(summary['nb1s2_corr'],0)
        self.assertEqual(summary['nb1s2_errors'],0)
        self.assertEqual(summary['nb1s2_mean'],-5)
        self.assertEqual(summary['nb1s2_median'],-5)
        self.assertEqual(summary['nb1s2_stdev'],-5)
        self.assertEqual(summary['nb1s3_corr'],0)
        self.assertEqual(summary['nb1s3_errors'],0)
        self.assertEqual(summary['nb1s3_mean'],-5)
        self.assertEqual(summary['nb1s3_median'],-5)
        self.assertEqual(summary['nb1s3_stdev'],-5)
        self.assertEqual(summary['nb1s4_corr'],0)
        self.assertEqual(summary['nb1s4_errors'],0)
        self.assertEqual(summary['nb1s4_mean'],-5)
        self.assertEqual(summary['nb1s4_median'],-5)
        self.assertEqual(summary['nb1s4_stdev'],-5)
        self.assertEqual(summary['nb1vhL_corr'],0)
        self.assertEqual(summary['nb1vhL_errors'],0)
        self.assertEqual(summary['nb1vhL_mean'],-5)
        self.assertEqual(summary['nb1vhL_median'],-5)
        self.assertEqual(summary['nb1vhL_stdev'],-5)
        self.assertEqual(summary['nb1vhR_corr'],0)
        self.assertEqual(summary['nb1vhR_errors'],0)
        self.assertEqual(summary['nb1vhR_mean'],-5)
        self.assertEqual(summary['nb1vhR_median'],-5)
        self.assertEqual(summary['nb1vhR_stdev'],-5)
        self.assertEqual(summary['nb2_total_trials'],0)
        self.assertEqual(summary['nb2_score'],-5)
        self.assertEqual(summary['nb2_bias'],-5)
        self.assertEqual(summary['nb2_corr'],0)
        self.assertEqual(summary['nb2_errors'],0)
        self.assertEqual(summary['nb2_mean'],-5)
        self.assertEqual(summary['nb2_median'],-5)
        self.assertEqual(summary['nb2_stdev'],-5)
        self.assertEqual(summary['nb2sm_corr'],0)
        self.assertEqual(summary['nb2sm_errors'],0)
        self.assertEqual(summary['nb2sm_mean'],-5)
        self.assertEqual(summary['nb2sm_median'],-5)
        self.assertEqual(summary['nb2sm_stdev'],-5)
        self.assertEqual(summary['nb2s1_corr'],0)
        self.assertEqual(summary['nb2s1_errors'],0)
        self.assertEqual(summary['nb2s1_mean'],-5)
        self.assertEqual(summary['nb2s1_median'],-5)
        self.assertEqual(summary['nb2s1_stdev'],-5)
        self.assertEqual(summary['nb2s2_corr'],0)
        self.assertEqual(summary['nb2s2_errors'],0)
        self.assertEqual(summary['nb2s2_mean'],-5)
        self.assertEqual(summary['nb2s2_median'],-5)
        self.assertEqual(summary['nb2s2_stdev'],-5)
        self.assertEqual(summary['nb2s3_corr'],0)
        self.assertEqual(summary['nb2s3_errors'],0)
        self.assertEqual(summary['nb2s3_mean'],-5)
        self.assertEqual(summary['nb2s3_median'],-5)
        self.assertEqual(summary['nb2s3_stdev'],-5)
        self.assertEqual(summary['nb2s4_corr'],0)
        self.assertEqual(summary['nb2s4_errors'],0)
        self.assertEqual(summary['nb2s4_mean'],-5)
        self.assertEqual(summary['nb2s4_median'],-5)
        self.assertEqual(summary['nb2s4_stdev'],-5)
        self.assertEqual(summary['nb2vhL_corr'],0)
        self.assertEqual(summary['nb2vhL_errors'],0)
        self.assertEqual(summary['nb2vhL_mean'],-5)
        self.assertEqual(summary['nb2vhL_median'],-5)
        self.assertEqual(summary['nb2vhL_stdev'],-5)
        self.assertEqual(summary['nb2vhR_corr'],0)
        self.assertEqual(summary['nb2vhR_errors'],0)
        self.assertEqual(summary['nb2vhR_mean'],-5)
        self.assertEqual(summary['nb2vhR_median'],-5)
        self.assertEqual(summary['nb2vhR_stdev'],-5)
        self.assertEqual(summary['nb2int_corr'],0)
        self.assertEqual(summary['nb2int_errors'],0)
        self.assertEqual(summary['nb2int_mean'],-5)
        self.assertEqual(summary['nb2int_median'],-5)
        self.assertEqual(summary['nb2int_stdev'],-5)
        self.assertEqual(summary['nb2noint_corr'],0)
        self.assertEqual(summary['nb2noint_errors'],0)
        self.assertEqual(summary['nb2noint_mean'],-5)
        self.assertEqual(summary['nb2noint_median'],-5)
        self.assertEqual(summary['nb2noint_stdev'],-5)
    
        
    
    def test_calculation02(self):
        """Test calculations: test summary stats when all responses are correct and given at 1.2345 seconds."""
        responses = self.task.responses
        for trialData in self.nb1TestingBlock.trialHandler:
            response = examiner.nback.NBackResponse()
            response.block=self.nb1TestingBlock
            response.trialData = trialData
            response.key=trialData.corr_resp
            response.rt=1.2345
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corr_resp and response.trialData.corr_resp <> 'none'):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        for trialData in self.nb2TestingBlock.trialHandler:
            response = examiner.nback.NBackResponse()
            response.block=self.nb2TestingBlock
            response.trialData = trialData
            response.key=trialData.corr_resp
            response.rt=1.2345
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corr_resp and response.trialData.corr_resp <> 'none'):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        
        summary = responses.getSummaryStatsFields()
        
        self.assertEqual(summary['nb1_total_trials'],30)
        self.assertEqual(round(summary['nb1_score'],3),3.671)
        self.assertEqual(round(summary['nb1_bias'],3),-0.145)
        self.assertEqual(summary['nb1_corr'],30)
        self.assertEqual(summary['nb1_errors'],0)
        self.assertEqual(summary['nb1_mean'],1.2345)
        self.assertEqual(summary['nb1_median'],1.2345)
        self.assertEqual(summary['nb1_stdev'],0)
        self.assertEqual(summary['nb1sm_corr'],10)
        self.assertEqual(summary['nb1sm_errors'],0)
        self.assertEqual(summary['nb1sm_mean'],1.2345)
        self.assertEqual(summary['nb1sm_median'],1.2345)
        self.assertEqual(summary['nb1sm_stdev'],0)
        self.assertEqual(summary['nb1s1_corr'],5)
        self.assertEqual(summary['nb1s1_errors'],0)
        self.assertEqual(summary['nb1s1_mean'],1.2345)
        self.assertEqual(summary['nb1s1_median'],1.2345)
        self.assertEqual(summary['nb1s1_stdev'],0)
        self.assertEqual(summary['nb1s2_corr'],5)
        self.assertEqual(summary['nb1s2_errors'],0)
        self.assertEqual(summary['nb1s2_mean'],1.2345)
        self.assertEqual(summary['nb1s2_median'],1.2345)
        self.assertEqual(summary['nb1s2_stdev'],0)
        self.assertEqual(summary['nb1s3_corr'],5)
        self.assertEqual(summary['nb1s3_errors'],0)
        self.assertEqual(summary['nb1s3_mean'],1.2345)
        self.assertEqual(summary['nb1s3_median'],1.2345)
        self.assertEqual(summary['nb1s3_stdev'],0)
        self.assertEqual(summary['nb1s4_corr'],5)
        self.assertEqual(summary['nb1s4_errors'],0)
        self.assertEqual(summary['nb1s4_mean'],1.2345)
        self.assertEqual(summary['nb1s4_median'],1.2345)
        self.assertEqual(summary['nb1s4_stdev'],0)
        self.assertEqual(summary['nb1vhL_corr'],11)
        self.assertEqual(summary['nb1vhL_errors'],0)
        self.assertEqual(summary['nb1vhL_mean'],1.2345)
        self.assertEqual(summary['nb1vhL_median'],1.2345)
        self.assertEqual(summary['nb1vhL_stdev'],0)
        self.assertEqual(summary['nb1vhR_corr'],11)
        self.assertEqual(summary['nb1vhR_errors'],0)
        self.assertEqual(summary['nb1vhR_mean'],1.2345)
        self.assertEqual(summary['nb1vhR_median'],1.2345)
        self.assertEqual(summary['nb1vhR_stdev'],0)        
        self.assertEqual(summary['nb2_total_trials'],90)
        self.assertEqual(round(summary['nb2_score'],3),4.541)
        self.assertEqual(round(summary['nb2_bias'],3),-0.129)
        self.assertEqual(summary['nb2_corr'],90)
        self.assertEqual(summary['nb2_errors'],0)
        self.assertEqual(summary['nb2_mean'],1.2345)
        self.assertEqual(summary['nb2_median'],1.2345)
        self.assertEqual(summary['nb2_stdev'],0)
        self.assertEqual(summary['nb2sm_corr'],30)
        self.assertEqual(summary['nb2sm_errors'],0)
        self.assertEqual(summary['nb2sm_mean'],1.2345)
        self.assertEqual(summary['nb2sm_median'],1.2345)
        self.assertEqual(summary['nb2sm_stdev'],0)
        self.assertEqual(summary['nb2s1_corr'],15)
        self.assertEqual(summary['nb2s1_errors'],0)
        self.assertEqual(summary['nb2s1_mean'],1.2345)
        self.assertEqual(summary['nb2s1_median'],1.2345)
        self.assertEqual(summary['nb2s1_stdev'],0)
        self.assertEqual(summary['nb2s2_errors'],0)
        self.assertEqual(summary['nb2s2_corr'],15)
        self.assertEqual(summary['nb2s2_mean'],1.2345)
        self.assertEqual(summary['nb2s2_median'],1.2345)
        self.assertEqual(summary['nb2s2_stdev'],0)
        self.assertEqual(summary['nb2s3_corr'],15)
        self.assertEqual(summary['nb2s3_errors'],0)
        self.assertEqual(summary['nb2s3_mean'],1.2345)
        self.assertEqual(summary['nb2s3_median'],1.2345)
        self.assertEqual(summary['nb2s3_stdev'],0)
        self.assertEqual(summary['nb2s4_corr'],15)
        self.assertEqual(summary['nb2s4_errors'],0)
        self.assertEqual(summary['nb2s4_mean'],1.2345)
        self.assertEqual(summary['nb2s4_median'],1.2345)
        self.assertEqual(summary['nb2s4_stdev'],0)
        self.assertEqual(summary['nb2vhL_corr'],34)
        self.assertEqual(summary['nb2vhL_errors'],0)
        self.assertEqual(summary['nb2vhL_mean'],1.2345)
        self.assertEqual(summary['nb2vhL_median'],1.2345)
        self.assertEqual(summary['nb2vhL_stdev'],0)
        self.assertEqual(summary['nb2vhR_corr'],34)
        self.assertEqual(summary['nb2vhR_errors'],0)
        self.assertEqual(summary['nb2vhR_mean'],1.2345)
        self.assertEqual(summary['nb2vhR_median'],1.2345)
        self.assertEqual(summary['nb2vhR_stdev'],0)
        self.assertEqual(summary['nb2int_corr'],8)
        self.assertEqual(summary['nb2int_errors'],0)
        self.assertEqual(summary['nb2int_mean'],1.2345)
        self.assertEqual(summary['nb2int_median'],1.2345)
        self.assertEqual(summary['nb2int_stdev'],0)
        self.assertEqual(summary['nb2noint_corr'],82)
        self.assertEqual(summary['nb2noint_errors'],0)
        self.assertEqual(summary['nb2noint_mean'],1.2345)
        self.assertEqual(summary['nb2noint_median'],1.2345)
        self.assertEqual(summary['nb2noint_stdev'],0)

        
    def test_calculation03(self):
        """Test calculations: test summary stats when all responses are left and given at 1.2345 seconds."""
        responses = self.task.responses
        for trialData in self.nb1TestingBlock.trialHandler:
            response = examiner.nback.NBackResponse()
            response.block=self.nb1TestingBlock
            response.trialData = trialData
            response.key='left'
            response.rt=1.2345
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corr_resp and response.trialData.corr_resp <> 'none'):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        for trialData in self.nb2TestingBlock.trialHandler:
            response = examiner.nback.NBackResponse()
            response.block=self.nb2TestingBlock
            response.trialData = trialData
            response.key='left'
            response.rt=1.2345
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corr_resp and response.trialData.corr_resp <> 'none'):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        
        summary = responses.getSummaryStatsFields()

        self.assertEqual(summary['nb1_total_trials'],30)
        self.assertEqual(round(summary['nb1_score'],3),-0.29)
        self.assertEqual(round(summary['nb1_bias'],3),1.836)
        self.assertEqual(summary['nb1_corr'],10)
        self.assertEqual(summary['nb1_errors'],20)
        self.assertEqual(summary['nb1_mean'],1.2345)
        self.assertEqual(summary['nb1_median'],1.2345)
        self.assertEqual(summary['nb1_stdev'],0)
        self.assertEqual(summary['nb1sm_corr'],10)
        self.assertEqual(summary['nb1sm_errors'],0)
        self.assertEqual(summary['nb1sm_mean'],1.2345)
        self.assertEqual(summary['nb1sm_median'],1.2345)
        self.assertEqual(summary['nb1sm_stdev'],0)
        self.assertEqual(summary['nb1s1_corr'],0)
        self.assertEqual(summary['nb1s1_errors'],5)
        self.assertEqual(summary['nb1s1_mean'],-5)
        self.assertEqual(summary['nb1s1_median'],-5)
        self.assertEqual(summary['nb1s1_stdev'],-5)
        self.assertEqual(summary['nb1s2_corr'],0)
        self.assertEqual(summary['nb1s2_errors'],5)
        self.assertEqual(summary['nb1s2_mean'],-5)
        self.assertEqual(summary['nb1s2_median'],-5)
        self.assertEqual(summary['nb1s2_stdev'],-5)
        self.assertEqual(summary['nb1s3_corr'],0)
        self.assertEqual(summary['nb1s3_errors'],5)
        self.assertEqual(summary['nb1s3_mean'],-5)
        self.assertEqual(summary['nb1s3_median'],-5)
        self.assertEqual(summary['nb1s3_stdev'],-5)
        self.assertEqual(summary['nb1s4_corr'],0)
        self.assertEqual(summary['nb1s4_errors'],5)
        self.assertEqual(summary['nb1s4_mean'],-5)
        self.assertEqual(summary['nb1s4_median'],-5)
        self.assertEqual(summary['nb1s4_stdev'],-5)
        self.assertEqual(summary['nb1vhL_corr'],4)
        self.assertEqual(summary['nb1vhL_errors'],7)
        self.assertEqual(summary['nb1vhL_mean'],1.2345)
        self.assertEqual(summary['nb1vhL_median'],1.2345)
        self.assertEqual(summary['nb1vhL_stdev'],0)
        self.assertEqual(summary['nb1vhR_corr'],4)
        self.assertEqual(summary['nb1vhR_errors'],7)
        self.assertEqual(summary['nb1vhR_mean'],1.2345)
        self.assertEqual(summary['nb1vhR_median'],1.2345)
        self.assertEqual(summary['nb1vhR_stdev'],0)
        self.assertEqual(summary['nb2_total_trials'],90)
        self.assertEqual(round(summary['nb2_score'],3),-0.259)
        self.assertEqual(round(summary['nb2_bias'],3),2.271)
        self.assertEqual(summary['nb2_corr'],30)
        self.assertEqual(summary['nb2_errors'],60)
        self.assertEqual(summary['nb2_mean'],1.2345)
        self.assertEqual(summary['nb2_median'],1.2345)
        self.assertEqual(summary['nb2_stdev'],0)
        self.assertEqual(summary['nb2sm_corr'],30)
        self.assertEqual(summary['nb2sm_errors'],0)
        self.assertEqual(summary['nb2sm_mean'],1.2345)
        self.assertEqual(summary['nb2sm_median'],1.2345)
        self.assertEqual(summary['nb2sm_stdev'],0)
        self.assertEqual(summary['nb2s1_corr'],0)
        self.assertEqual(summary['nb2s1_errors'],15)
        self.assertEqual(summary['nb2s1_mean'],-5)
        self.assertEqual(summary['nb2s1_median'],-5)
        self.assertEqual(summary['nb2s1_stdev'],-5)
        self.assertEqual(summary['nb2s2_corr'],0)
        self.assertEqual(summary['nb2s2_errors'],15)
        self.assertEqual(summary['nb2s2_mean'],-5)
        self.assertEqual(summary['nb2s2_median'],-5)
        self.assertEqual(summary['nb2s2_stdev'],-5)
        self.assertEqual(summary['nb2s3_corr'],0)
        self.assertEqual(summary['nb2s3_errors'],15)
        self.assertEqual(summary['nb2s3_mean'],-5)
        self.assertEqual(summary['nb2s3_median'],-5)
        self.assertEqual(summary['nb2s3_stdev'],-5)
        self.assertEqual(summary['nb2s4_corr'],0)
        self.assertEqual(summary['nb2s4_errors'],15)
        self.assertEqual(summary['nb2s4_mean'],-5)
        self.assertEqual(summary['nb2s4_median'],-5)
        self.assertEqual(summary['nb2s4_stdev'],-5)
        self.assertEqual(summary['nb2vhL_corr'],13)
        self.assertEqual(summary['nb2vhL_errors'],21)
        self.assertEqual(summary['nb2vhL_mean'],1.2345)
        self.assertEqual(summary['nb2vhL_median'],1.2345)
        self.assertEqual(summary['nb2vhL_stdev'],0)
        self.assertEqual(summary['nb2vhR_corr'],13)
        self.assertEqual(summary['nb2vhR_errors'],21)
        self.assertEqual(summary['nb2vhR_mean'],1.2345)
        self.assertEqual(summary['nb2vhR_median'],1.2345)
        self.assertEqual(summary['nb2vhR_stdev'],0)
        self.assertEqual(summary['nb2int_corr'],0)
        self.assertEqual(summary['nb2int_errors'],8)
        self.assertEqual(summary['nb2int_mean'],-5)
        self.assertEqual(summary['nb2int_median'],-5)
        self.assertEqual(summary['nb2int_stdev'],-5)
        self.assertEqual(summary['nb2noint_corr'],30)
        self.assertEqual(summary['nb2noint_errors'],52)
        self.assertEqual(summary['nb2noint_mean'],1.2345)
        self.assertEqual(summary['nb2noint_median'],1.2345)
        self.assertEqual(summary['nb2noint_stdev'],0)

        
        
        
    def test_calculation04(self):
        """Test calculations: test summary stats when all responses are right and given at 1.2345 seconds."""
        responses = self.task.responses
        for trialData in self.nb1TestingBlock.trialHandler:
            response = examiner.nback.NBackResponse()
            response.block=self.nb1TestingBlock
            response.trialData = trialData
            response.key='right'
            response.rt=1.2345
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corr_resp and response.trialData.corr_resp <> 'none'):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        for trialData in self.nb2TestingBlock.trialHandler:
            response = examiner.nback.NBackResponse()
            response.block=self.nb2TestingBlock
            response.trialData = trialData
            response.key='right'
            response.rt=1.2345
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corr_resp and response.trialData.corr_resp <> 'none'):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['nb1_total_trials'],30)
        self.assertEqual(round(summary['nb1_score'],3),0.29)
        self.assertEqual(round(summary['nb1_bias'],3),-1.836)
        self.assertEqual(summary['nb1_corr'],20)
        self.assertEqual(summary['nb1_errors'],10)
        self.assertEqual(summary['nb1_mean'],1.2345)
        self.assertEqual(summary['nb1_median'],1.2345)
        self.assertEqual(summary['nb1_stdev'],0)
        self.assertEqual(summary['nb1sm_corr'],0)
        self.assertEqual(summary['nb1sm_errors'],10)
        self.assertEqual(summary['nb1sm_mean'],-5)
        self.assertEqual(summary['nb1sm_median'],-5)
        self.assertEqual(summary['nb1sm_stdev'],-5)
        self.assertEqual(summary['nb1s1_corr'],5)
        self.assertEqual(summary['nb1s1_errors'],0)
        self.assertEqual(summary['nb1s1_mean'],1.2345)
        self.assertEqual(summary['nb1s1_median'],1.2345)
        self.assertEqual(summary['nb1s1_stdev'],0)
        self.assertEqual(summary['nb1s2_corr'],5)
        self.assertEqual(summary['nb1s2_errors'],0)
        self.assertEqual(summary['nb1s2_mean'],1.2345)
        self.assertEqual(summary['nb1s2_median'],1.2345)
        self.assertEqual(summary['nb1s2_stdev'],0)
        self.assertEqual(summary['nb1s3_corr'],5)
        self.assertEqual(summary['nb1s3_errors'],0)
        self.assertEqual(summary['nb1s3_mean'],1.2345)
        self.assertEqual(summary['nb1s3_median'],1.2345)
        self.assertEqual(summary['nb1s3_stdev'],0)
        self.assertEqual(summary['nb1s4_corr'],5)
        self.assertEqual(summary['nb1s4_errors'],0)
        self.assertEqual(summary['nb1s4_mean'],1.2345)
        self.assertEqual(summary['nb1s4_median'],1.2345)
        self.assertEqual(summary['nb1s4_stdev'],0)
        self.assertEqual(summary['nb1vhL_corr'],7)
        self.assertEqual(summary['nb1vhL_errors'],4)
        self.assertEqual(summary['nb1vhL_mean'],1.2345)
        self.assertEqual(summary['nb1vhL_median'],1.2345)
        self.assertEqual(summary['nb1vhL_stdev'],0)
        self.assertEqual(summary['nb1vhR_corr'],7)
        self.assertEqual(summary['nb1vhR_errors'],4)
        self.assertEqual(summary['nb1vhR_mean'],1.2345)
        self.assertEqual(summary['nb1vhR_median'],1.2345)
        self.assertEqual(summary['nb1vhR_stdev'],0)
        self.assertEqual(summary['nb2_total_trials'],90)
        self.assertEqual(round(summary['nb2_score'],3),0.259)
        self.assertEqual(round(summary['nb2_bias'],3),-2.271)
        self.assertEqual(summary['nb2_corr'],60)
        self.assertEqual(summary['nb2_errors'],30)
        self.assertEqual(summary['nb2_mean'],1.2345)
        self.assertEqual(summary['nb2_median'],1.2345)
        self.assertEqual(summary['nb2_stdev'],0)
        self.assertEqual(summary['nb2sm_corr'],0)
        self.assertEqual(summary['nb2sm_errors'],30)
        self.assertEqual(summary['nb2sm_mean'],-5)
        self.assertEqual(summary['nb2sm_median'],-5)
        self.assertEqual(summary['nb2sm_stdev'],-5)
        self.assertEqual(summary['nb2s1_corr'],15)
        self.assertEqual(summary['nb2s1_errors'],0)
        self.assertEqual(summary['nb2s1_mean'],1.2345)
        self.assertEqual(summary['nb2s1_median'],1.2345)
        self.assertEqual(summary['nb2s1_stdev'],0)
        self.assertEqual(summary['nb2s2_corr'],15)
        self.assertEqual(summary['nb2s2_errors'],0)
        self.assertEqual(summary['nb2s2_mean'],1.2345)
        self.assertEqual(summary['nb2s2_median'],1.2345)
        self.assertEqual(summary['nb2s2_stdev'],0)
        self.assertEqual(summary['nb2s3_corr'],15)
        self.assertEqual(summary['nb2s3_errors'],0)
        self.assertEqual(summary['nb2s3_mean'],1.2345)
        self.assertEqual(summary['nb2s3_median'],1.2345)
        self.assertEqual(summary['nb2s3_stdev'],0)
        self.assertEqual(summary['nb2s4_corr'],15)
        self.assertEqual(summary['nb2s4_errors'],0)
        self.assertEqual(summary['nb2s4_mean'],1.2345)
        self.assertEqual(summary['nb2s4_median'],1.2345)
        self.assertEqual(summary['nb2s4_stdev'],0)
        self.assertEqual(summary['nb2vhL_corr'],21)
        self.assertEqual(summary['nb2vhL_errors'],13)
        self.assertEqual(summary['nb2vhL_mean'],1.2345)
        self.assertEqual(summary['nb2vhL_median'],1.2345)
        self.assertEqual(summary['nb2vhL_stdev'],0)
        self.assertEqual(summary['nb2vhR_corr'],21)
        self.assertEqual(summary['nb2vhR_errors'],13)
        self.assertEqual(summary['nb2vhR_mean'],1.2345)
        self.assertEqual(summary['nb2vhR_median'],1.2345)
        self.assertEqual(summary['nb2vhR_stdev'],0)
        self.assertEqual(summary['nb2int_corr'],8)
        self.assertEqual(summary['nb2int_errors'],0)
        self.assertEqual(summary['nb2int_mean'],1.2345)
        self.assertEqual(summary['nb2int_median'],1.2345)
        self.assertEqual(summary['nb2int_stdev'],0)
        self.assertEqual(summary['nb2noint_corr'],52)
        self.assertEqual(summary['nb2noint_errors'],30)
        self.assertEqual(summary['nb2noint_mean'],1.2345)
        self.assertEqual(summary['nb2noint_median'],1.2345)
        self.assertEqual(summary['nb2noint_stdev'],0) 



    def test_calculation05(self):
        """Test calculations: test summary stats when first 10 responses are correct and the remaining are left at 1.2345 seconds."""
        responses = self.task.responses
        for trialData in self.nb1TestingBlock.trialHandler:
            response = examiner.nback.NBackResponse()
            response.block=self.nb1TestingBlock
            response.trialData = trialData
            if(trialData.trial_number <= 10):
                response.key=trialData.corr_resp
            else:
                response.key='left'
            response.rt=1.2345
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corr_resp and response.trialData.corr_resp <> 'none'):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        for trialData in self.nb2TestingBlock.trialHandler:
            response = examiner.nback.NBackResponse()
            response.block=self.nb2TestingBlock
            response.trialData = trialData
            if(trialData.trial_number <= 10):
                response.key=trialData.corr_resp
            else:
                response.key='left'
            response.rt=1.2345
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corr_resp and response.trialData.corr_resp <> 'none'):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
        
        self.assertEqual(summary['nb1_total_trials'],30)
        self.assertEqual(round(summary['nb1_score'],3),1.325)
        self.assertEqual(round(summary['nb1_bias'],3),1.028)
        self.assertEqual(summary['nb1_corr'],17)
        self.assertEqual(summary['nb1_errors'],13)
        self.assertEqual(summary['nb1_mean'],1.2345)
        self.assertEqual(summary['nb1_median'],1.2345)
        self.assertEqual(summary['nb1_stdev'],0)
        self.assertEqual(summary['nb1sm_corr'],10)
        self.assertEqual(summary['nb1sm_errors'],0)
        self.assertEqual(summary['nb1sm_mean'],1.2345)
        self.assertEqual(summary['nb1sm_median'],1.2345)
        self.assertEqual(summary['nb1sm_stdev'],0)
        self.assertEqual(summary['nb1s1_corr'],3)
        self.assertEqual(summary['nb1s1_errors'],2)
        self.assertEqual(summary['nb1s1_mean'],1.2345)
        self.assertEqual(summary['nb1s1_median'],1.2345)
        self.assertEqual(summary['nb1s1_stdev'],0)
        self.assertEqual(summary['nb1s2_corr'],1)
        self.assertEqual(summary['nb1s2_errors'],4)
        self.assertEqual(summary['nb1s2_mean'],1.2345)
        self.assertEqual(summary['nb1s2_median'],1.2345)
        self.assertEqual(summary['nb1s2_stdev'],0)
        self.assertEqual(summary['nb1s3_corr'],1)
        self.assertEqual(summary['nb1s3_errors'],4)
        self.assertEqual(summary['nb1s3_mean'],1.2345)
        self.assertEqual(summary['nb1s3_median'],1.2345)
        self.assertEqual(summary['nb1s3_stdev'],0)
        self.assertEqual(summary['nb1s4_corr'],2)
        self.assertEqual(summary['nb1s4_errors'],3)
        self.assertEqual(summary['nb1s4_mean'],1.2345)
        self.assertEqual(summary['nb1s4_median'],1.2345)
        self.assertEqual(summary['nb1s4_stdev'],0)
        self.assertEqual(summary['nb1vhL_corr'],6)
        self.assertEqual(summary['nb1vhL_errors'],5)
        self.assertEqual(summary['nb1vhL_mean'],1.2345)
        self.assertEqual(summary['nb1vhL_median'],1.2345)
        self.assertEqual(summary['nb1vhL_stdev'],0)
        self.assertEqual(summary['nb1vhR_corr'],7)
        self.assertEqual(summary['nb1vhR_errors'],4)
        self.assertEqual(summary['nb1vhR_mean'],1.2345)
        self.assertEqual(summary['nb1vhR_median'],1.2345)
        self.assertEqual(summary['nb1vhR_stdev'],0)
        self.assertEqual(summary['nb2_total_trials'],90)
        self.assertEqual(round(summary['nb2_score'],3),0.981)
        self.assertEqual(round(summary['nb2_bias'],3),1.651)
        self.assertEqual(summary['nb2_corr'],37)
        self.assertEqual(summary['nb2_errors'],53)
        self.assertEqual(summary['nb2_mean'],1.2345)
        self.assertEqual(summary['nb2_median'],1.2345)
        self.assertEqual(summary['nb2_stdev'],0)
        self.assertEqual(summary['nb2sm_corr'],30)
        self.assertEqual(summary['nb2sm_errors'],0)
        self.assertEqual(summary['nb2sm_mean'],1.2345)
        self.assertEqual(summary['nb2sm_median'],1.2345)
        self.assertEqual(summary['nb2sm_stdev'],0)
        self.assertEqual(summary['nb2s1_corr'],3)
        self.assertEqual(summary['nb2s1_errors'],12)
        self.assertEqual(summary['nb2s1_mean'],1.2345)
        self.assertEqual(summary['nb2s1_median'],1.2345)
        self.assertEqual(summary['nb2s1_stdev'],0)
        self.assertEqual(summary['nb2s2_corr'],2)
        self.assertEqual(summary['nb2s2_errors'],13)
        self.assertEqual(summary['nb2s2_mean'],1.2345)
        self.assertEqual(summary['nb2s2_median'],1.2345)
        self.assertEqual(summary['nb2s2_stdev'],0)
        self.assertEqual(summary['nb2s3_corr'],1)
        self.assertEqual(summary['nb2s3_errors'],14)
        self.assertEqual(summary['nb2s3_mean'],1.2345)
        self.assertEqual(summary['nb2s3_median'],1.2345)
        self.assertEqual(summary['nb2s3_stdev'],0)
        self.assertEqual(summary['nb2s4_corr'],1)
        self.assertEqual(summary['nb2s4_errors'],14)
        self.assertEqual(summary['nb2s4_mean'],1.2345)
        self.assertEqual(summary['nb2s4_median'],1.2345)
        self.assertEqual(summary['nb2s4_stdev'],0)
        self.assertEqual(summary['nb2vhL_corr'],17)
        self.assertEqual(summary['nb2vhL_errors'],17)
        self.assertEqual(summary['nb2vhL_mean'],1.2345)
        self.assertEqual(summary['nb2vhL_median'],1.2345)
        self.assertEqual(summary['nb2vhL_stdev'],0)
        self.assertEqual(summary['nb2vhR_corr'],15)
        self.assertEqual(summary['nb2vhR_errors'],19)
        self.assertEqual(summary['nb2vhR_mean'],1.2345)
        self.assertEqual(summary['nb2vhR_median'],1.2345)
        self.assertEqual(summary['nb2vhR_stdev'],0)
        self.assertEqual(summary['nb2int_corr'],1)
        self.assertEqual(summary['nb2int_errors'],7)
        self.assertEqual(summary['nb2int_mean'],1.2345)
        self.assertEqual(summary['nb2int_median'],1.2345)
        self.assertEqual(summary['nb2int_stdev'],0)
        self.assertEqual(summary['nb2noint_corr'],36)
        self.assertEqual(summary['nb2noint_errors'],46)
        self.assertEqual(summary['nb2noint_mean'],1.2345)
        self.assertEqual(summary['nb2noint_median'],1.2345)
        self.assertEqual(summary['nb2noint_stdev'],0)        
        
    def test_calculation06(self):
        """Test calculations: test summary stats when first 10 responses are correct and the remaining are right at 1.2345 seconds."""
        responses = self.task.responses
        for trialData in self.nb1TestingBlock.trialHandler:
            response = examiner.nback.NBackResponse()
            response.block=self.nb1TestingBlock
            response.trialData = trialData
            if(trialData.trial_number <= 10):
                response.key=trialData.corr_resp
            else:
                response.key='right'
            response.rt=1.2345
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corr_resp and response.trialData.corr_resp <> 'none'):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        for trialData in self.nb2TestingBlock.trialHandler:
            response = examiner.nback.NBackResponse()
            response.block=self.nb2TestingBlock
            response.trialData = trialData
            if(trialData.trial_number <= 10):
                response.key=trialData.corr_resp
            else:
                response.key='right'
            response.rt=1.2345
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corr_resp and response.trialData.corr_resp <> 'none'):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
        
        self.assertEqual(summary['nb1_total_trials'],30)
        self.assertEqual(round(summary['nb1_score'],3),1.508)
        self.assertEqual(round(summary['nb1_bias'],3),-1.227)
        self.assertEqual(summary['nb1_corr'],23)
        self.assertEqual(summary['nb1_errors'],7)
        self.assertEqual(summary['nb1_mean'],1.2345)
        self.assertEqual(summary['nb1_median'],1.2345)
        self.assertEqual(summary['nb1_stdev'],0)
        self.assertEqual(summary['nb1sm_corr'],3)
        self.assertEqual(summary['nb1sm_errors'],7)
        self.assertEqual(summary['nb1sm_mean'],1.2345)
        self.assertEqual(summary['nb1sm_median'],1.2345)
        self.assertEqual(summary['nb1sm_stdev'],0)
        self.assertEqual(summary['nb1s1_corr'],5)
        self.assertEqual(summary['nb1s1_errors'],0)
        self.assertEqual(summary['nb1s1_mean'],1.2345)
        self.assertEqual(summary['nb1s1_median'],1.2345)
        self.assertEqual(summary['nb1s1_stdev'],0)
        self.assertEqual(summary['nb1s2_corr'],5)
        self.assertEqual(summary['nb1s2_errors'],0)
        self.assertEqual(summary['nb1s2_mean'],1.2345)
        self.assertEqual(summary['nb1s2_median'],1.2345)
        self.assertEqual(summary['nb1s2_stdev'],0)
        self.assertEqual(summary['nb1s3_corr'],5)
        self.assertEqual(summary['nb1s3_errors'],0)
        self.assertEqual(summary['nb1s3_mean'],1.2345)
        self.assertEqual(summary['nb1s3_median'],1.2345)
        self.assertEqual(summary['nb1s3_stdev'],0)
        self.assertEqual(summary['nb1s4_corr'],5)
        self.assertEqual(summary['nb1s4_errors'],0)
        self.assertEqual(summary['nb1s4_mean'],1.2345)
        self.assertEqual(summary['nb1s4_median'],1.2345)
        self.assertEqual(summary['nb1s4_stdev'],0)
        self.assertEqual(summary['nb1vhL_corr'],7)
        self.assertEqual(summary['nb1vhL_errors'],4)
        self.assertEqual(summary['nb1vhL_mean'],1.2345)
        self.assertEqual(summary['nb1vhL_median'],1.2345)
        self.assertEqual(summary['nb1vhL_stdev'],0)
        self.assertEqual(summary['nb1vhR_corr'],9)
        self.assertEqual(summary['nb1vhR_errors'],2)
        self.assertEqual(summary['nb1vhR_mean'],1.2345)
        self.assertEqual(summary['nb1vhR_median'],1.2345)
        self.assertEqual(summary['nb1vhR_stdev'],0)
        self.assertEqual(summary['nb2_total_trials'],90)
        self.assertEqual(round(summary['nb2_score'],3),0.999)
        self.assertEqual(round(summary['nb2_bias'],3),-1.9)
        self.assertEqual(summary['nb2_corr'],62)
        self.assertEqual(summary['nb2_errors'],28)
        self.assertEqual(summary['nb2_mean'],1.2345)
        self.assertEqual(summary['nb2_median'],1.2345)
        self.assertEqual(summary['nb2_stdev'],0)
        self.assertEqual(summary['nb2sm_corr'],2)
        self.assertEqual(summary['nb2sm_errors'],28)
        self.assertEqual(summary['nb2sm_mean'],1.2345)
        self.assertEqual(summary['nb2sm_median'],1.2345)
        self.assertEqual(summary['nb2sm_stdev'],0)
        self.assertEqual(summary['nb2s1_corr'],15)
        self.assertEqual(summary['nb2s1_errors'],0)
        self.assertEqual(summary['nb2s1_mean'],1.2345)
        self.assertEqual(summary['nb2s1_median'],1.2345)
        self.assertEqual(summary['nb2s1_stdev'],0)
        self.assertEqual(summary['nb2s2_corr'],15)
        self.assertEqual(summary['nb2s2_errors'],0)
        self.assertEqual(summary['nb2s2_mean'],1.2345)
        self.assertEqual(summary['nb2s2_median'],1.2345)
        self.assertEqual(summary['nb2s2_stdev'],0)
        self.assertEqual(summary['nb2s3_corr'],15)
        self.assertEqual(summary['nb2s3_errors'],0)
        self.assertEqual(summary['nb2s3_mean'],1.2345)
        self.assertEqual(summary['nb2s3_median'],1.2345)
        self.assertEqual(summary['nb2s3_stdev'],0)
        self.assertEqual(summary['nb2s4_corr'],15)
        self.assertEqual(summary['nb2s4_errors'],0)
        self.assertEqual(summary['nb2s4_mean'],1.2345)
        self.assertEqual(summary['nb2s4_median'],1.2345)
        self.assertEqual(summary['nb2s4_stdev'],0)
        self.assertEqual(summary['nb2vhL_corr'],22)
        self.assertEqual(summary['nb2vhL_errors'],12)
        self.assertEqual(summary['nb2vhL_mean'],1.2345)
        self.assertEqual(summary['nb2vhL_median'],1.2345)
        self.assertEqual(summary['nb2vhL_stdev'],0)
        self.assertEqual(summary['nb2vhR_corr'],22)
        self.assertEqual(summary['nb2vhR_errors'],12)
        self.assertEqual(summary['nb2vhR_mean'],1.2345)
        self.assertEqual(summary['nb2vhR_median'],1.2345)
        self.assertEqual(summary['nb2vhR_stdev'],0)
        self.assertEqual(summary['nb2int_corr'],8)
        self.assertEqual(summary['nb2int_errors'],0)
        self.assertEqual(summary['nb2int_mean'],1.2345)
        self.assertEqual(summary['nb2int_median'],1.2345)
        self.assertEqual(summary['nb2int_stdev'],0)
        self.assertEqual(summary['nb2noint_corr'],54)
        self.assertEqual(summary['nb2noint_errors'],28)
        self.assertEqual(summary['nb2noint_mean'],1.2345)
        self.assertEqual(summary['nb2noint_median'],1.2345)
        self.assertEqual(summary['nb2noint_stdev'],0)


    def test_calculation07(self):
        """Test calculations: test summary stats when all responses are in the directions of the side of the screen that the probe is on at 1.2345 seconds."""
        responses = self.task.responses
        for trialData in self.nb1TestingBlock.trialHandler:
            response = examiner.nback.NBackResponse()
            response.block=self.nb1TestingBlock
            response.trialData = trialData
            if(trialData.location <= 7):
                response.key='right'
            else:
                response.key='left'
            response.rt=1.2345
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corr_resp and response.trialData.corr_resp <> 'none'):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        for trialData in self.nb2TestingBlock.trialHandler:
            response = examiner.nback.NBackResponse()
            response.block=self.nb2TestingBlock
            response.trialData = trialData
            if(trialData.location <= 7):
                response.key='right'
            else:
                response.key='left'
            response.rt=1.2345
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corr_resp and response.trialData.corr_resp <> 'none'):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['nb1_total_trials'],30)
        self.assertEqual(round(summary['nb1_score'],3),0.12)
        self.assertEqual(round(summary['nb1_bias'],3),-0.06)
        self.assertEqual(summary['nb1_corr'],16)
        self.assertEqual(summary['nb1_errors'],14)
        self.assertEqual(summary['nb1_mean'],1.2345)
        self.assertEqual(summary['nb1_median'],1.2345)
        self.assertEqual(summary['nb1_stdev'],0)
        self.assertEqual(summary['nb1sm_corr'],5)
        self.assertEqual(summary['nb1sm_errors'],5)
        self.assertEqual(summary['nb1sm_mean'],1.2345)
        self.assertEqual(summary['nb1sm_median'],1.2345)
        self.assertEqual(summary['nb1sm_stdev'],0)
        self.assertEqual(summary['nb1s1_corr'],3)
        self.assertEqual(summary['nb1s1_errors'],2)
        self.assertEqual(summary['nb1s1_mean'],1.2345)
        self.assertEqual(summary['nb1s1_median'],1.2345)
        self.assertEqual(summary['nb1s1_stdev'],0)
        self.assertEqual(summary['nb1s2_corr'],3)
        self.assertEqual(summary['nb1s2_errors'],2)
        self.assertEqual(summary['nb1s2_mean'],1.2345)
        self.assertEqual(summary['nb1s2_median'],1.2345)
        self.assertEqual(summary['nb1s2_stdev'],0)
        self.assertEqual(summary['nb1s3_corr'],2)
        self.assertEqual(summary['nb1s3_errors'],3)
        self.assertEqual(summary['nb1s3_mean'],1.2345)
        self.assertEqual(summary['nb1s3_median'],1.2345)
        self.assertEqual(summary['nb1s3_stdev'],0)
        self.assertEqual(summary['nb1s4_corr'],3)
        self.assertEqual(summary['nb1s4_errors'],2)
        self.assertEqual(summary['nb1s4_mean'],1.2345)
        self.assertEqual(summary['nb1s4_median'],1.2345)
        self.assertEqual(summary['nb1s4_stdev'],0)
        self.assertEqual(summary['nb1vhL_corr'],3)
        self.assertEqual(summary['nb1vhL_errors'],8)
        self.assertEqual(summary['nb1vhL_mean'],1.2345)
        self.assertEqual(summary['nb1vhL_median'],1.2345)
        self.assertEqual(summary['nb1vhL_stdev'],0)
        self.assertEqual(summary['nb1vhR_corr'],8)
        self.assertEqual(summary['nb1vhR_errors'],3)
        self.assertEqual(summary['nb1vhR_mean'],1.2345)
        self.assertEqual(summary['nb1vhR_median'],1.2345)
        self.assertEqual(summary['nb1vhR_stdev'],0)
        self.assertEqual(summary['nb2_total_trials'],90)
        self.assertEqual(round(summary['nb2_score'],3),0.165)
        self.assertEqual(round(summary['nb2_bias'],3),-0.083)
        self.assertEqual(summary['nb2_corr'],49)
        self.assertEqual(summary['nb2_errors'],41)
        self.assertEqual(summary['nb2_mean'],1.2345)
        self.assertEqual(summary['nb2_median'],1.2345)
        self.assertEqual(summary['nb2_stdev'],0)
        self.assertEqual(summary['nb2sm_corr'],15)
        self.assertEqual(summary['nb2sm_errors'],15)
        self.assertEqual(summary['nb2sm_mean'],1.2345)
        self.assertEqual(summary['nb2sm_median'],1.2345)
        self.assertEqual(summary['nb2sm_stdev'],0)
        self.assertEqual(summary['nb2s1_corr'],9)
        self.assertEqual(summary['nb2s1_errors'],6)
        self.assertEqual(summary['nb2s1_mean'],1.2345)
        self.assertEqual(summary['nb2s1_median'],1.2345)
        self.assertEqual(summary['nb2s1_stdev'],0)
        self.assertEqual(summary['nb2s2_corr'],8)
        self.assertEqual(summary['nb2s2_errors'],7)
        self.assertEqual(summary['nb2s2_mean'],1.2345)
        self.assertEqual(summary['nb2s2_median'],1.2345)
        self.assertEqual(summary['nb2s2_stdev'],0)
        self.assertEqual(summary['nb2s3_corr'],8)
        self.assertEqual(summary['nb2s3_errors'],7)
        self.assertEqual(summary['nb2s3_mean'],1.2345)
        self.assertEqual(summary['nb2s3_median'],1.2345)
        self.assertEqual(summary['nb2s3_stdev'],0)
        self.assertEqual(summary['nb2s4_corr'],9)
        self.assertEqual(summary['nb2s4_errors'],6)
        self.assertEqual(summary['nb2s4_mean'],1.2345)
        self.assertEqual(summary['nb2s4_median'],1.2345)
        self.assertEqual(summary['nb2s4_stdev'],0)
        self.assertEqual(summary['nb2vhL_corr'],17)
        self.assertEqual(summary['nb2vhL_errors'],17)
        self.assertEqual(summary['nb2vhL_mean'],1.2345)
        self.assertEqual(summary['nb2vhL_median'],1.2345)
        self.assertEqual(summary['nb2vhL_stdev'],0)
        self.assertEqual(summary['nb2vhR_corr'],18)
        self.assertEqual(summary['nb2vhR_errors'],16)
        self.assertEqual(summary['nb2vhR_mean'],1.2345)
        self.assertEqual(summary['nb2vhR_median'],1.2345)
        self.assertEqual(summary['nb2vhR_stdev'],0)
        self.assertEqual(summary['nb2int_corr'],4)
        self.assertEqual(summary['nb2int_errors'],4)
        self.assertEqual(summary['nb2int_mean'],1.2345)
        self.assertEqual(summary['nb2int_median'],1.2345)
        self.assertEqual(summary['nb2int_stdev'],0)
        self.assertEqual(summary['nb2noint_corr'],45)
        self.assertEqual(summary['nb2noint_errors'],37)
        self.assertEqual(summary['nb2noint_mean'],1.2345)
        self.assertEqual(summary['nb2noint_median'],1.2345)
        self.assertEqual(summary['nb2noint_stdev'],0)        


    def test_calculation08(self):
        """Test calculations:correct except on nb2 interference trials at 1.2345 seconds."""
        responses = self.task.responses
        for trialData in self.nb1TestingBlock.trialHandler:
            response = examiner.nback.NBackResponse()
            response.block=self.nb1TestingBlock
            response.trialData = trialData
            response.key = response.trialData.corr_resp
            response.rt=1.2345
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corr_resp and response.trialData.corr_resp <> 'none'):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        for trialData in self.nb2TestingBlock.trialHandler:
            response = examiner.nback.NBackResponse()
            response.block=self.nb2TestingBlock
            response.trialData = trialData
            if(trialData.interference == 1):
                if(response.trialData.corr_resp=="left"):
                    response.key='right'
                else:
                    response.key='left'
            else:
                response.key = response.trialData.corr_resp
            response.rt=1.2345
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corr_resp and response.trialData.corr_resp <> 'none'):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['nb1_total_trials'],30)
        self.assertEqual(round(summary['nb1_score'],3),3.671)
        self.assertEqual(round(summary['nb1_bias'],3),-0.145)
        self.assertEqual(summary['nb1_corr'],30)
        self.assertEqual(summary['nb1_errors'],0)
        self.assertEqual(summary['nb1_mean'],1.2345)
        self.assertEqual(summary['nb1_median'],1.2345)
        self.assertEqual(summary['nb1_stdev'],0)
        self.assertEqual(summary['nb1sm_corr'],10)
        self.assertEqual(summary['nb1sm_errors'],0)
        self.assertEqual(summary['nb1sm_mean'],1.2345)
        self.assertEqual(summary['nb1sm_median'],1.2345)
        self.assertEqual(summary['nb1sm_stdev'],0)
        self.assertEqual(summary['nb1s1_corr'],5)
        self.assertEqual(summary['nb1s1_errors'],0)
        self.assertEqual(summary['nb1s1_mean'],1.2345)
        self.assertEqual(summary['nb1s1_median'],1.2345)
        self.assertEqual(summary['nb1s1_stdev'],0)
        self.assertEqual(summary['nb1s2_corr'],5)
        self.assertEqual(summary['nb1s2_errors'],0)
        self.assertEqual(summary['nb1s2_mean'],1.2345)
        self.assertEqual(summary['nb1s2_median'],1.2345)
        self.assertEqual(summary['nb1s2_stdev'],0)
        self.assertEqual(summary['nb1s3_corr'],5)
        self.assertEqual(summary['nb1s3_errors'],0)
        self.assertEqual(summary['nb1s3_mean'],1.2345)
        self.assertEqual(summary['nb1s3_median'],1.2345)
        self.assertEqual(summary['nb1s3_stdev'],0)
        self.assertEqual(summary['nb1s4_corr'],5)
        self.assertEqual(summary['nb1s4_errors'],0)
        self.assertEqual(summary['nb1s4_mean'],1.2345)
        self.assertEqual(summary['nb1s4_median'],1.2345)
        self.assertEqual(summary['nb1s4_stdev'],0)
        self.assertEqual(summary['nb1vhL_corr'],11)
        self.assertEqual(summary['nb1vhL_errors'],0)
        self.assertEqual(summary['nb1vhL_mean'],1.2345)
        self.assertEqual(summary['nb1vhL_median'],1.2345)
        self.assertEqual(summary['nb1vhL_stdev'],0)
        self.assertEqual(summary['nb1vhR_corr'],11)
        self.assertEqual(summary['nb1vhR_errors'],0)
        self.assertEqual(summary['nb1vhR_mean'],1.2345)
        self.assertEqual(summary['nb1vhR_median'],1.2345)
        self.assertEqual(summary['nb1vhR_stdev'],0)
        self.assertEqual(summary['nb2_total_trials'],90)
        self.assertEqual(round(summary['nb2_score'],3),3.224)
        self.assertEqual(round(summary['nb2_bias'],3),0.529)
        self.assertEqual(summary['nb2_corr'],82)
        self.assertEqual(summary['nb2_errors'],8)
        self.assertEqual(summary['nb2_mean'],1.2345)
        self.assertEqual(summary['nb2_median'],1.2345)
        self.assertEqual(summary['nb2_stdev'],0)
        self.assertEqual(summary['nb2sm_corr'],30)
        self.assertEqual(summary['nb2sm_errors'],0)
        self.assertEqual(summary['nb2sm_mean'],1.2345)
        self.assertEqual(summary['nb2sm_median'],1.2345)
        self.assertEqual(summary['nb2sm_stdev'],0)
        self.assertEqual(summary['nb2s1_corr'],13)
        self.assertEqual(summary['nb2s1_errors'],2)
        self.assertEqual(summary['nb2s1_mean'],1.2345)
        self.assertEqual(summary['nb2s1_median'],1.2345)
        self.assertEqual(summary['nb2s1_stdev'],0)
        self.assertEqual(summary['nb2s2_corr'],13)
        self.assertEqual(summary['nb2s2_errors'],2)
        self.assertEqual(summary['nb2s2_mean'],1.2345)
        self.assertEqual(summary['nb2s2_median'],1.2345)
        self.assertEqual(summary['nb2s2_stdev'],0)
        self.assertEqual(summary['nb2s3_corr'],13)
        self.assertEqual(summary['nb2s3_errors'],2)
        self.assertEqual(summary['nb2s3_mean'],1.2345)
        self.assertEqual(summary['nb2s3_median'],1.2345)
        self.assertEqual(summary['nb2s3_stdev'],0)
        self.assertEqual(summary['nb2s4_corr'],13)
        self.assertEqual(summary['nb2s4_errors'],2)
        self.assertEqual(summary['nb2s4_mean'],1.2345)
        self.assertEqual(summary['nb2s4_median'],1.2345)
        self.assertEqual(summary['nb2s4_stdev'],0)
        self.assertEqual(summary['nb2vhL_corr'],32)
        self.assertEqual(summary['nb2vhL_errors'],2)
        self.assertEqual(summary['nb2vhL_mean'],1.2345)
        self.assertEqual(summary['nb2vhL_median'],1.2345)
        self.assertEqual(summary['nb2vhL_stdev'],0)
        self.assertEqual(summary['nb2vhR_corr'],32)
        self.assertEqual(summary['nb2vhR_errors'],2)
        self.assertEqual(summary['nb2vhR_mean'],1.2345)
        self.assertEqual(summary['nb2vhR_median'],1.2345)
        self.assertEqual(summary['nb2vhR_stdev'],0)
        self.assertEqual(summary['nb2int_corr'],0)
        self.assertEqual(summary['nb2int_errors'],8)
        self.assertEqual(summary['nb2int_mean'],-5)
        self.assertEqual(summary['nb2int_median'],-5)
        self.assertEqual(summary['nb2int_stdev'],-5)
        self.assertEqual(summary['nb2noint_corr'],82)
        self.assertEqual(summary['nb2noint_errors'],0)
        self.assertEqual(summary['nb2noint_mean'],1.2345)
        self.assertEqual(summary['nb2noint_median'],1.2345)
        self.assertEqual(summary['nb2noint_stdev'],0)


    def test_calculation09(self):
        """Test calculations: test summary stats when all responses are correct and the times are 1.5 seconds for match and 2 seconds minus 100 milliseconds for each similarity position."""
        responses = self.task.responses
        for trialData in self.nb1TestingBlock.trialHandler:
            response = examiner.nback.NBackResponse()
            response.block=self.nb1TestingBlock
            response.trialData = trialData
            response.key=trialData.corr_resp
            
            if(trialData.similarity == 4):
                response.rt=1.600
            elif(trialData.similarity == 3):
                response.rt=1.700
            elif(trialData.similarity == 2):
                response.rt=1.800
            elif(trialData.similarity == 1):
                response.rt=1.900
            elif(trialData.similarity == 0):
                response.rt=1.500
                
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corr_resp and response.trialData.corr_resp <> 'none'):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        for trialData in self.nb2TestingBlock.trialHandler:
            response = examiner.nback.NBackResponse()
            response.block=self.nb2TestingBlock
            response.trialData = trialData
            response.key=trialData.corr_resp
            
            if(trialData.similarity == 4):
                response.rt=1.600
            elif(trialData.similarity == 3):
                response.rt=1.700
            elif(trialData.similarity == 2):
                response.rt=1.800
            elif(trialData.similarity == 1):
                response.rt=1.900
            elif(trialData.similarity == 0):
                response.rt=1.500
            response.taskTime=0 #not needed for calc testing
            response.trialNum=0 #not needed for calc testing
            if(response.key == response.trialData.corr_resp and response.trialData.corr_resp <> 'none'):
                response.corr=1
            else:
                response.corr=0
            responses.addResponse(response)
        
        summary = responses.getSummaryStatsFields()
        self.assertEqual(summary['nb1_total_trials'],30)
        self.assertEqual(round(summary['nb1_score'],3),3.671)
        self.assertEqual(round(summary['nb1_bias'],3),-0.145)
        self.assertEqual(summary['nb1_corr'],30)
        self.assertEqual(summary['nb1_errors'],0)
        self.assertEqual(summary['nb1_mean'],1.6667)
        self.assertEqual(summary['nb1_median'],1.65)
        self.assertEqual(summary['nb1_stdev'],0.1491)
        self.assertEqual(summary['nb1sm_corr'],10)
        self.assertEqual(summary['nb1sm_errors'],0)
        self.assertEqual(summary['nb1sm_mean'],1.5)
        self.assertEqual(summary['nb1sm_median'],1.5)
        self.assertEqual(summary['nb1sm_stdev'],0)
        self.assertEqual(summary['nb1s1_corr'],5)
        self.assertEqual(summary['nb1s1_errors'],0)
        self.assertEqual(summary['nb1s1_mean'],1.9)
        self.assertEqual(summary['nb1s1_median'],1.9)
        self.assertEqual(summary['nb1s1_stdev'],0)
        self.assertEqual(summary['nb1s2_corr'],5)
        self.assertEqual(summary['nb1s2_errors'],0)
        self.assertEqual(summary['nb1s2_mean'],1.8)
        self.assertEqual(summary['nb1s2_median'],1.8)
        self.assertEqual(summary['nb1s2_stdev'],0)
        self.assertEqual(summary['nb1s3_corr'],5)
        self.assertEqual(summary['nb1s3_errors'],0)
        self.assertEqual(summary['nb1s3_mean'],1.7)
        self.assertEqual(summary['nb1s3_median'],1.7)
        self.assertEqual(summary['nb1s3_stdev'],0)
        self.assertEqual(summary['nb1s4_corr'],5)
        self.assertEqual(summary['nb1s4_errors'],0)
        self.assertEqual(summary['nb1s4_mean'],1.6)
        self.assertEqual(summary['nb1s4_median'],1.6)
        self.assertEqual(summary['nb1s4_stdev'],0)
        self.assertEqual(summary['nb1vhL_corr'],11)
        self.assertEqual(summary['nb1vhL_errors'],0)
        self.assertEqual(summary['nb1vhL_mean'],1.6455)
        self.assertEqual(summary['nb1vhL_median'],1.6)
        self.assertEqual(summary['nb1vhL_stdev'],0.1373)
        self.assertEqual(summary['nb1vhR_corr'],11)
        self.assertEqual(summary['nb1vhR_errors'],0)
        self.assertEqual(summary['nb1vhR_mean'],1.6455)
        self.assertEqual(summary['nb1vhR_median'],1.6)
        self.assertEqual(summary['nb1vhR_stdev'],0.1373)
        self.assertEqual(summary['nb2_total_trials'],90)
        self.assertEqual(round(summary['nb2_score'],3),4.541)
        self.assertEqual(round(summary['nb2_bias'],3),-0.129)
        self.assertEqual(summary['nb2_corr'],90)
        self.assertEqual(summary['nb2_errors'],0)
        self.assertEqual(summary['nb2_mean'],1.6667)
        self.assertEqual(summary['nb2_median'],1.65)
        self.assertEqual(summary['nb2_stdev'],0.1491)
        self.assertEqual(summary['nb2sm_corr'],30)
        self.assertEqual(summary['nb2sm_errors'],0)
        self.assertEqual(summary['nb2sm_mean'],1.5)
        self.assertEqual(summary['nb2sm_median'],1.5)
        self.assertEqual(summary['nb2sm_stdev'],0)
        self.assertEqual(summary['nb2s1_corr'],15)
        self.assertEqual(summary['nb2s1_errors'],0)
        self.assertEqual(summary['nb2s1_mean'],1.9)
        self.assertEqual(summary['nb2s1_median'],1.9)
        self.assertEqual(summary['nb2s1_stdev'],0)
        self.assertEqual(summary['nb2s2_corr'],15)
        self.assertEqual(summary['nb2s2_errors'],0)
        self.assertEqual(summary['nb2s2_mean'],1.8)
        self.assertEqual(summary['nb2s2_median'],1.8)
        self.assertEqual(summary['nb2s2_stdev'],0)
        self.assertEqual(summary['nb2s3_corr'],15)
        self.assertEqual(summary['nb2s3_errors'],0)
        self.assertEqual(summary['nb2s3_mean'],1.7)
        self.assertEqual(summary['nb2s3_median'],1.7)
        self.assertEqual(summary['nb2s3_stdev'],0)
        self.assertEqual(summary['nb2s4_corr'],15)
        self.assertEqual(summary['nb2s4_errors'],0)
        self.assertEqual(summary['nb2s4_mean'],1.6)
        self.assertEqual(summary['nb2s4_median'],1.6)
        self.assertEqual(summary['nb2s4_stdev'],0)
        self.assertEqual(summary['nb2vhL_corr'],34)
        self.assertEqual(summary['nb2vhL_errors'],0)
        self.assertEqual(summary['nb2vhL_mean'],1.6647)
        self.assertEqual(summary['nb2vhL_median'],1.7)
        self.assertEqual(summary['nb2vhL_stdev'],0.1512)
        self.assertEqual(summary['nb2vhR_corr'],34)
        self.assertEqual(summary['nb2vhR_errors'],0)
        self.assertEqual(summary['nb2vhR_mean'],1.6647)
        self.assertEqual(summary['nb2vhR_median'],1.7)
        self.assertEqual(summary['nb2vhR_stdev'],0.1512)
        self.assertEqual(summary['nb2int_corr'],8)
        self.assertEqual(summary['nb2int_errors'],0)
        self.assertEqual(summary['nb2int_mean'],1.75)
        self.assertEqual(summary['nb2int_median'],1.75)
        self.assertEqual(summary['nb2int_stdev'],0.1118)
        self.assertEqual(summary['nb2noint_corr'],82)
        self.assertEqual(summary['nb2noint_errors'],0)
        self.assertEqual(summary['nb2noint_mean'],1.6585)
        self.assertEqual(summary['nb2noint_median'],1.6)
        self.assertEqual(summary['nb2noint_stdev'],0.1498)




class TestNbackVariations(unittest.TestCase):
    """Test Variations of the Nback task.
    
    """
    
    def setUp(self):
        """create a sped up timer for tasks"""
        testConfig = lavatask.base.Configuration(['../../lavatask.cfg','Test.cfg'])
        self.task = examiner.nback.NBackTask(testConfig)
        self.task.taskClockFactory = lavatask.base.TestingTaskClockFactory(50.000)
        self.task.recordScreenShots = True
    
    def test_EnglishAdultNB1(self):
        """Test English Adult Nback1, fail the first NB1 practice"""
        self.task.sessionNum = "EnglishAdultNB1"
        self.task.subjectId = "NBackTest"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB1FirstPractice")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,180)
       
    def test_EnglishAdultNB2(self):
        """Test English Adult Nback 2, fail the first and second NB2 practice."""
        self.task.sessionNum = "EnglishAdultNB2"
        self.task.subjectId = "NBackTest"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB2SecondPractice")
        self.task.runTask()
        self.assertEqual(self.task.responses.count,193)

    def test_EnglishAdultNB2B(self):
        """Test English Adult Nback2 form B, fail the first and second NB2 practice."""
        self.task.sessionNum = "EnglishAdultNB2B"
        self.task.subjectId = "NBackTest"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB2SecondPractice")
        self.task.form = 'B'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,193)

    def test_EnglishAdultNB2C(self):
        """Test English Adult Nback2 form C, fail the first and second NB2 practice."""
        self.task.sessionNum = "EnglishAdultNB2B"
        self.task.subjectId = "NBackTest"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB2SecondPractice")
        self.task.form = 'C'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,193)
                    
    def test_SpanishAdultNB1(self):
        """Test Spanish Adult Nback1, fail the first NB1 practice"""
        self.task.sessionNum = "SpanishAdultNB1"
        self.task.subjectId = "NBackTest"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB1FirstPractice")
        self.task.language = 'Spanish'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,180)
       
    def test_SpanishAdultNB2(self):
        """Test Spanish Adult Nback2, fail the first and second NB2 practice."""
        self.task.sessionNum = "SpanishAdultNB2"
        self.task.subjectId = "NBackTest"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB2SecondPractice")
        self.task.language = 'Spanish'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,193)

    def test_SpanishAdultNB2B(self):
        """Test Spanish Adult Nback2 form B, fail the first and second NB2 practice."""
        self.task.sessionNum = "SpanishAdultNB2B"
        self.task.subjectId = "NBackTest"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB2SecondPractice")
        self.task.language = 'Spanish'
        self.task.form = 'B'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,193)

    def test_SpanishAdultNB2C(self):
        """Test Spanish Adult Nback2 form C, fail the first and second NB2 practice."""
        self.task.sessionNum = "SpanishAdultNB2B"
        self.task.subjectId = "NBackTest"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB2SecondPractice")
        self.task.language = 'Spanish'
        self.task.form = 'C'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,193)
                    
    def test_HebrewAdultNB1(self):
        """Test Hebrew Adult Nback1, fail the first NB1 practice"""
        self.task.sessionNum = "HebrewAdultNB1"
        self.task.subjectId = "NBackTest"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB1FirstPractice")
        self.task.language = 'Hebrew'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,180)
       
    def test_HebrewAdultNB2(self):
        """Test Hebrew Adult Nback2, fail the first and second NB2 practice."""
        self.task.sessionNum = "HebrewAdultNB2"
        self.task.subjectId = "NBackTest"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB2SecondPractice")
        self.task.language = 'Hebrew'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,193)

    def test_HebrewAdultNB2B(self):
        """Test Hebrew Adult Nback2 form B, fail the first and second NB2 practice."""
        self.task.sessionNum = "HebrewAdultNB2B"
        self.task.subjectId = "NBackTest"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB2SecondPractice")
        self.task.language = 'Hebrew'
        self.task.form = 'B'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,193)

    def test_HebrewAdultNB2C(self):
        """Test Hebrew Adult Nback2 form C, fail the first and second NB2 practice."""
        self.task.sessionNum = "HebrewAdultNB2B"
        self.task.subjectId = "NBackTest"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB2SecondPractice")
        self.task.language = 'Hebrew'
        self.task.form = 'C'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,193)
                
    def test_EnglishChildNB1(self):
        """Test English Child Nback1, fail the first NB1 practice"""
        self.task.sessionNum = "EnglishChildNB1"
        self.task.subjectId = "NBackTest"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB1FirstPractice")
        self.task.ageCohort = 'Child'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,64)
    
    def test_SpanishChildNB1(self):
        """Test Spanish Child Nback1, fail the first NB1 practice"""
        self.task.sessionNum = "SpanishChildNB1"
        self.task.subjectId = "NBackTest"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB1FirstPractice")
        self.task.language = 'Spanish'
        self.task.ageCohort = 'Child'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,64)
    
    def test_HebrewChildNB1(self):
        """Test Hebrew Child Nback1, fail the first NB1 practice"""
        self.task.sessionNum = "HebrewChildNB1"
        self.task.subjectId = "NBackTest"
        self.task.defaultResponseMonitor = TestNbackResponseMonitor(self.task,"FailNB1FirstPractice")
        self.task.language = 'Hebrew'
        self.task.ageCohort = 'Child'
        self.task.runTask()
        self.assertEqual(self.task.responses.count,64)

def runCalcTests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNbackCalc)
    unittest.TextTestRunner(verbosity=2).run(suite)

def runFlowTests():
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNbackFlowAndOutput)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
def runVariationsTests():
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNbackVariations)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
   runCalcTests()
   runFlowTests()
   runVariationsTests()
      