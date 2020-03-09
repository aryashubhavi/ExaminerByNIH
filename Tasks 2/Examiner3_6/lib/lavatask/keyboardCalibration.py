#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Class library that provides extensions to the LavaTask classes for the keyboard calibration task

:Classes:
    keyboardCalibrationTask - extends Task class to implement block configuration and control of flow for the keyboardCalibration task.
    keyboardCalibrationBlock - extends TrialBlock class to implement fixation points and other keyboardCalibration specific trial block functionality.
    keyboardCalibrationResponses - extends TaskResponses class to implement keyboardCalibration specific summary scoring.
    keyboardCalibrationResponse - extends TrialResponse class to implement keyboardCalibration specific trial configuration in output files.
 
:Author:
    Joe Hesse, jhesse@memory.ucsf.edu

"""

# Part of the LavaTask Library
# Copyright (C) 2011, Regents of the University of California
# All Rights Reserved
#
# Distributed under the terms of the BSD 2-Clause License 
# (http://www.opensource.org/licenses/BSD-2-Clause)

import os
from psychopy import core, data, event, visual, gui, logging
from random import randint
from numpy import *
import lavatask.base
import lavatask.arduino



class KeyboardCalibrationTask(lavatask.base.Task):
    """Extends Task class to implement block configuration and control of flow for the KeyboardCalibration task.
    
    """
    def __init__(self,configuration):
        lavatask.base.Task.__init__(self,configuration)
        self.name='KeyboardCalibration'
        self.version='1.0.0.0'
        self.versionDate='12/08/2010'
        self.arduinoPort=configuration.get("arduino","port","None")
        self.responses = KeyboardCalibrationResponses(self)
        self.arduino = lavatask.arduino.Arduino(self.arduinoPort)
    
    def doBeforeTask(self):
        """Configure task blocks 
        """
        self.clock.wait(2)
        block = KeyboardCalibrationBlock(self,'calibration')
        block.initializeTrialData(20)
        self.addBlock(block)
    


class KeyboardCalibrationBlock(lavatask.base.TrialResponseBlock):
    """Extends TrialBlock class to implement fixation points and other KeyboardCalibration specific trial block functionality.
    
    The KeyboardCalibration block runs a set number of trials to check the keyboard response latency times against and external
    measure of the keypress (arduino based pressure sensor). 
    """
    def __init__(self,task,name,keys=["left","right"],trialData=None):
        lavatask.base.TrialResponseBlock.__init__(self,task,name,keys,trialData)
        self.beforeTrialDelay = 1 #default time between response and next trial
        self.leftStimuli = None 
        self.rightStimuli = None
        self.currentTrialNum = 0
        self.maxResponseTime=4.0 #default response time after stimuli is displayed
        self.defaultTrialDataTemplate = [{'direction': 'left'},{'direction': 'right'},]
    def initializeTrialData(self,reps,trialData=None):
        """Configures an underlying trialData handler using default template or trialData param if supplied.
        
        :parameters:
            reps - the number of times to repeat the trial configuration.
            trialData - trial configuration data (optional : uses default template if not supplied)
        """
        if(trialData!=None):
            self.trialData=trialData
        if(self.trialData == None):
            self.trialData=self.defaultTrialDataTemplate
        self.trialHandler = data.TrialHandler(self.trialData,reps)
        
    def doBeforeTrialBlock(self):
        """Sets up common stimuli for the block."""
        self.leftStimuli=visual.TextStim(win=self.task.window, ori=0,text='<< Left',pos=[0, 0], height=0.1, color='#0000FF')
        self.rightStimuli=visual.TextStim(win=self.task.window, ori=0,text='Right >>',pos=[0, 0], height=0.1, color='#0000FF')
    
    def doBeforeTrial(self):
        """Configures the next trial or ends block if no more trials."""
        try:
            # get next trial data
            self.currentTrial = self.trialHandler.next()
        except StopIteration:  #no more trials
            self.setContinueTrial(False)
            self.setContinue(False)
            return
        #reset the trial "draw stage" variable
        self.trialDrawStage = 0
        
        self.currentTrialNum += 1
        #set trial timeout and reset clock  
        self.trialTimeout = self.maxResponseTime
        
        self.lastResponse = None
        self.lastResponseTime = None
        self.lastResponseDevice = None
        
        #turn off response checking (until stimulus is displayed)
        self.disableResponse()
        
        
    def doTrialTimeout(self):
         """Handles timed out trial by recording a "none" response."""
         response = KeyboardCalibrationResponse()
         response.block=self
         response.trialData = self.currentTrial
         response.key='none'
         response.responseDevice = 'none'
         response.rt=0
         response.taskTime=self.task.getTime()
         response.trialNum=self.currentTrialNum
         response.calbrationSensor=0
         response.calibrationSensorTime=0
         self.task.responses.addResponse(response)
         
    def doBeforeTrialResponse(self):
        """Draws stimuli and configures devices."""
        if(self.trialDrawStage == 0):
            if(self.currentTrial['direction'] == 'left'):
                self.leftStimuli.draw()
            else:
                self.rightStimuli.draw()
            self.trialDrawStage = 1
            self.task.arduino.clearEvents()
            self.task.arduino.resetTimer()
            self.resetClock()
            self.enableResponse()
            self.task.refreshWindow()
        
    def doAfterTrialResponse(self):
         """Checks response and records response data."""
         response = KeyboardCalibrationResponse()
         response.block=self
         response.trialData = self.currentTrial
         response.key=self.lastResponse
         response.responseDevice = self.lastResponseDevice
         response.rt=self.lastResponseTime
         response.taskTime=self.task.getTime()
         response.trialNum=self.currentTrialNum
         self.wait(0.05)
         events = self.task.arduino.getSensorEvents(allowedEvents=[1])
         if(events):
            response.calibrationSensor= events[0].sensor
            response.calibrationSensorTime=events[0].time/1000.0000
         else:
            response.calibrationSensor=0
            response.calibrationSensorTime=0
         
         self.task.responses.addResponse(response)
         self.task.refreshWindow()
        
    

class KeyboardCalibrationResponses(lavatask.base.TaskResponses):
    """Extends TaskResponses class to implement KeyboardCalibration specific summary scoring.
    
    Summary scoring for Keyboard Calibration is 
        1) Mean of keyboard response
        2) Median of keyboard response
        3) Stdev of keyboard response
        4) Mean of calibration sensor response
        5) Median of calibration sensor response
        6) Stdev of calibration sensor response
    
    These scoring values are calculated for:
        1) Overall 
        2) Left
        3) Right
    
    """
    def __init__(self,task):
        lavatask.base.TaskResponses.__init__(self,task)
    
    def getSummaryStatsColumns(self):
        """Return column names for the summary statistics."""
        columns = lavatask.base.TaskResponses.getSummaryStatsColumns(self)
        for column in ['response_device','total_trials',
        'total_diff_mean','total_diff_median','total_diff_stdev',
        'left_diff_mean','left_diff_median','left_diff_stdev',
        'right_diff_mean','right_diff_median','right_diff_stdev',
        'total_resp_mean','total_resp_median','total_resp_stdev',
        'right_resp_mean','right_resp_median','right_resp_stdev',
        'left_resp_mean','left_resp_median','left_resp_stdev',
        'total_sensor_mean','total_sensor_median','total_sensor_stdev',
        'left_sensor_mean','left_sensor_median','left_sensor_stdev',
        'right_sensor_mean','right_sensor_median','right_sensor_stdev',
        ]:
            columns.append(column)
        return columns
    
    def getSummaryStatsFields(self):
        """Calculate the summary stats and return the data as a dictionary."""
        fields = lavatask.base.TaskResponses.getSummaryStatsFields(self)
        response_device=None
        left_kb = []
        left_sensor=[]
        left_diff = []
        right_kb=[]
        right_sensor=[]
        right_diff=[]
        kb=[]
        sensor=[]
        diff=[]
        testingTrialsAttempted=0
        #compile response data into groups for summary stats
        for response in self.data:
            if(response['resp_value']!='None'):
                if(response_device == None):
                    response_device = response['response_device']
                elif (response_device <> 'multiple' and response_device <> response['response_device']):
                    response_device = 'multiple'
                
                if(response['trial_direction']=='left' and response['resp_sensor']==1):
                    testingTrialsAttempted+=1
                    rt = response['resp_rt']
                    sensor_rt = response['resp_sensor_time']
                    kb.append(rt)
                    sensor.append(sensor_rt)
                    diff.append(rt-sensor_rt)
                    left_kb.append(rt)
                    left_sensor.append(sensor_rt)
                    left_diff.append(rt-sensor_rt)
                elif(response['trial_direction']=='right' and response['resp_sensor']==2):
                    testingTrialsAttempted+=1
                    rt = response['resp_rt']
                    sensor_rt = response['resp_sensor_time']
                    kb.append(rt)
                    sensor.append(sensor_rt)
                    diff.append(rt-sensor_rt)
                    right_kb.append(rt)
                    right_sensor.append(sensor_rt)
                    right_diff.append(rt-sensor_rt)
        #do summary stats on each summary group and add to fields collection
        fields.update({'response_device':response_device})
        fields.update({'total_trials':testingTrialsAttempted})
        fields.update({'total_diff_mean':self.calcMean(diff),'total_diff_median':self.calcMedian(diff),'total_diff_stdev':self.calcStDev(diff)})
        fields.update({'left_diff_mean':self.calcMean(left_diff),'left_diff_median':self.calcMedian(left_diff),'left_diff_stdev':self.calcStDev(left_diff)})
        fields.update({'right_diff_mean':self.calcMean(right_diff),'right_diff_median':self.calcMedian(right_diff),'right_diff_stdev':self.calcStDev(right_diff)})
        fields.update({'total_resp_mean':self.calcMean(kb),'total_resp_median':self.calcMedian(kb),'total_resp_stdev':self.calcStDev(kb)})
        fields.update({'left_resp_mean':self.calcMean(left_kb),'left_resp_median':self.calcMedian(left_kb),'left_resp_stdev':self.calcStDev(left_kb)})
        fields.update({'right_resp_mean':self.calcMean(right_kb),'right_resp_median':self.calcMedian(right_kb),'right_resp_stdev':self.calcStDev(right_kb)})
        fields.update({'total_sensor_mean':self.calcMean(sensor),'total_sensor_median':self.calcMedian(sensor),'total_sensor_stdev':self.calcStDev(sensor)})
        fields.update({'left_sensor_mean':self.calcMean(left_sensor),'left_sensor_median':self.calcMedian(left_sensor),'left_sensor_stdev':self.calcStDev(left_sensor)})
        fields.update({'right_sensor_mean':self.calcMean(right_sensor),'right_sensor_median':self.calcMedian(right_sensor),'right_sensor_stdev':self.calcStDev(right_sensor)})
        
        return fields
        
    def calcCorrect(self,values,noCalcValue=0):
        """Calculate the number of correct responses. """
        return len(values)
    
    def calcMean(self,values,noCalcValue=-5):
        """Calculate the mean of the values array passed to the method, returnng noCalcValue if Mean cannot be calculated."""
        if(len(values)==0):
            return noCalcValue
        return round(mean(values),4)
    
    def calcMedian(self,values,noCalcValue=-5):
        """Calculate the median of the values array passed to the method, returning noCalcValue if Median cannot be calculated."""
        if(len(values)==0):
           return noCalcValue
        return round(median(values),4)
    
    def calcStDev(self,values,noCalcValue=-5):
        """Calculate the standard deviation of the values array passed to the method, returning noCalcValue if StDev cannot be calculated."""
        if(len(values)==0):
           return noCalcValue
        return round(std(values),4)

class KeyboardCalibrationResponse(lavatask.base.TrialResponse):
    """Extends TrialResponse class to implement Keyboard Calibration specific trial configuration in output files.
    
    """
    def __init__(self):
        lavatask.base.TrialResponse.__init__(self)
        # this data field is used to record the random fixation period of 
        # each trial (output to allow validation of randomness if needed)
        self.calibrationSensor=None
        self.calibrationSensorTime=None
    
    def getTrialConfigurationFields(self):
        """Returns the flanker specific trial configuration data as a dictionary."""
        return {'trial_direction':self.trialData.direction,'resp_sensor':self.calibrationSensor,'resp_sensor_time':self.calibrationSensorTime}
    def getTrialConfigurationColumns(self):
        """Returns the flanker specific trial configuration column names."""
        return ['trial_direction','resp_sensor','resp_sensor_time']
     