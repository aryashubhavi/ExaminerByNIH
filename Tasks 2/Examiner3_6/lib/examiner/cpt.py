#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Class library that provides extensions to the base LavaTask computer based task classes for the continuous performance task (CPT)

:Classes:
    CPTTask - extends Task class to implement block configuration and control of flow for the (CPT)
    CPTBlock - extends TrialBlock class to implement CPT specific trial block functionality.
    CPTResponses - extends TaskResponses class to implement CPT specific summary scoring.
    CPTResponse - extends TrialResponse class to implement CPT specific trial configuration in output files.

:Author:
    Joe Hesse, jhesse@memory.ucsf.edu

"""

# Part of the Examiner Computer Based Task Library
# Copyright (C) 2011, Regents of the University of California
# All Rights Reserved
#
# Distributed under the terms of the BSD 2-Clause License
# (http://www.opensource.org/licenses/BSD-2-Clause)

import os
from psychopy import core, data, event, visual, gui, logging
from random import randint
import lavatask.base



class CPTTask(lavatask.base.Task):
    """Extends Task class to implement block configuration and control of flow for the CPT.

    """
    def __init__(self,configuration,environment=None,sessionConfig=None):
        lavatask.base.Task.__init__(self,configuration,environment,sessionConfig)
        self.name='CPT'
        self.version='3.2.0.1'
        self.versionDate='12/30/2011'
        self.responses = CPTResponses(self)
        self.resourcePath = os.path.join(self.resourcePath,'examiner','cpt')

    def doBeforeTask(self):
        """Configure task blocks based on ageCohort and language of the task."""
        self.setupTask()
        #log error and quit if no configuration found for the ageCohort and language settings
        if(self.getBlockByName('testingBlock')==None):
            logging.error("CPT not configured.  AgeCohort=" + self.ageCohort +", Language=" + self.language + ".")
            core.quit();

    def doAfterBlock(self,block):
        """Perform task specific control of flow logic.

        If the subject gets 16 out of 20 trials correct in a practice trial then skip ahead to
        the real testing trial.  If the subject fails to get 16 out of 20 in 3 practice blocks then
        end the task.
        """
        if(block.name=="firstPracticeBlock" or block.name=="secondPracticeBlock"):
            #check whether we can skip the remaining practice blocks
            if(block.totalCorrect >= 16):
                self.setNextBlock("testingInstruct")
        if(block.name == "thirdPracticeBlock"):
            #check whether we should abort the task
            if(block.totalCorrect < 16):
                self.setNextBlock("completeInstruct")


    def setupTask(self):
        """Configure task blocks."""

        target = lavatask.base.Resource('target.bmp',self)


        firstPracticeInstruct = lavatask.base.InstructionBlock(self,"firstPracticeInstruct",['space',],"White","Black")
        firstPracticeInstruct.text = lavatask.base.UnicodeResource("practice.txt",self).getCenteredText()
        firstPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=target.getResourceLocation(),pos=[0,0],size=3.5,units='cm'))

        self.addBlock(firstPracticeInstruct)

        firstPracticeBlock = CPTBlock(self,'firstPracticeBlock',numTargets=15)
        firstPracticeBlock.initializeTrialData(1)
        self.addBlock(firstPracticeBlock)

        secondPracticeInstruct = lavatask.base.InstructionBlock(self,"secondPracticeInstruct",['space',],"White","Black")
        secondPracticeInstruct.text = lavatask.base.UnicodeResource("additional_practice.txt",self).getCenteredText()
        secondPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=target.getResourceLocation(),pos=[0,-1.8],size=3.5,units='cm'))



        self.addBlock(secondPracticeInstruct)

        secondPracticeBlock = CPTBlock(self,'secondPracticeBlock',numTargets=15)
        secondPracticeBlock.initializeTrialData(1)
        self.addBlock(secondPracticeBlock)


        thirdPracticeInstruct = lavatask.base.InstructionBlock(self,"thirdPracticeInstruct",['space',],"White","Black")
        thirdPracticeInstruct.text = lavatask.base.UnicodeResource("additional_practice.txt",self).getCenteredText()
        thirdPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=target.getResourceLocation(),pos=[0,-1.8],size=3.5,units='cm'))

        self.addBlock(thirdPracticeInstruct)

        thirdPracticeBlock = CPTBlock(self,'thirdPracticeBlock',numTargets=15)
        thirdPracticeBlock.initializeTrialData(1)
        self.addBlock(thirdPracticeBlock)
#
        testingInstruct = lavatask.base.InstructionBlock(self,"testingInstruct",['space',],"White","Black")
        testingInstruct.text = lavatask.base.UnicodeResource("testing.txt",self).getCenteredText()
        self.addBlock(testingInstruct)

        testingBlock = CPTBlock(self,'testingBlock')
        testingBlock.initializeTrialData(4)
        self.addBlock(testingBlock)

        completeInstruct = lavatask.base.InstructionBlock(self,"completeInstruct",['space'],"White","Black")
        completeInstruct.text = lavatask.base.UnicodeResource("complete.txt",self).getCenteredText()
        self.addBlock(completeInstruct)




class CPTBlock(lavatask.base.TrialResponseBlock):
    """Extends TrialBlock class to implement fixation points and other CPT specific trial block functionality.

    The CPT block runs a set number of trials (randomly ordered) and each trial has the following structure:
        1) Stimulus Display: 750 milliseconds
        2) Interstimulus Interval: 1500 milliseconds

    All responses are recorded after the display of the stimulus.  The first response after the display of the stimulus is recorded
    in terms of the response time.   Any additional responses prior to the next stimulus display are recorded and result in an "incorrect"
    response score for the trial.

    """
    def __init__(self,task,name,keys=["left"],numTargets=20,trialData=None):
        lavatask.base.TrialResponseBlock.__init__(self,task,name,keys,trialData)
        self.beforeBlockDelay = 1.0 # one second delay before block
        self.stimuli = {}
        self.lastTrialCorrect = None  #the last trial result (correct = True, incorrect = False)
        self.totalCorrect=0 #count of the number of correct responses
        self.stimulusDisplayDuration=.750 #length of time to display the stimulus
        self.responseTimeLimit=2.0 #duration from beginning of trial where responses are recorded
        self.interStimulusDelay=1.500 #length of each trial after the stimulus is erased from the screen and before the first stimulus is displayed
        self.trialTimeout = self.stimulusDisplayDuration + self.interStimulusDelay
        self.numTargets=numTargets #the number of targets to display during the block.  Default is 20, practice trials display 15.
        self.background="Black"

        self.defaultTrialDataTemplate = [  \
            {'stimulus': 'nontarget1'},
            {'stimulus': 'nontarget2'},
            {'stimulus': 'nontarget3'},
            {'stimulus': 'nontarget4'},
            {'stimulus': 'nontarget5'},
            ]
        for i in range(numTargets):
            self.defaultTrialDataTemplate.append({'stimulus':'target'})



    def initializeTrialData(self,reps,trialData=None):

        """Configures trialhandler with cpt trials.

        The cpt trials are handled to ensure that there are no sequences of tragets longer than 10
        and no sequences of nontargets longer than 2.

        """


        cptTrials = None
        cptSequenceCheckPassed = False

        while not(cptSequenceCheckPassed):
            cptTrials = self.getTrialsFromTrialHandler(data.TrialHandler(self.defaultTrialDataTemplate,reps))
            cptSequenceCheckPassed = self.cptSequenceCheck(cptTrials)


        self.trialHandler = data.TrialHandler(cptTrials,1,method="sequential")

    def cptSequenceCheck(self,trials):
        """utility method to validate the sequence ordering

        The cpt trials are handled to ensure that there are no sequences of targets longer than 10
        and no sequences of nontargets longer than 2.

        """
        targetSequence = 0
        nontargetSequence = 0

        for trial in trials:
            if(trial['stimulus']=='target'):
                targetSequence+=1
                nontargetSequence=0
                if(targetSequence > 10):
                    return False
            else:
                nontargetSequence+=1
                targetSequence=0
                if(nontargetSequence>2):
                    return False

        return True

    def doBeforeTrialBlock(self):
        """Sets up common stimuli for the block."""


        target = lavatask.base.Resource('target.bmp',self.task)
        nt1 = lavatask.base.Resource('nt1.bmp',self.task)
        nt2 = lavatask.base.Resource('nt2.bmp',self.task)
        nt3 = lavatask.base.Resource('nt3.bmp',self.task)
        nt4 = lavatask.base.Resource('nt4.bmp',self.task)
        nt5 = lavatask.base.Resource('nt5.bmp',self.task)

        self.stimuli['target'] = visual.ImageStim(win=self.task.window, image=target.getResourceLocation(),size=3.5,units='cm')
        self.stimuli['nontarget1'] = visual.ImageStim(win=self.task.window, image=nt1.getResourceLocation(),size=3.5,units='cm')
        self.stimuli['nontarget2'] = visual.ImageStim(win=self.task.window, image=nt2.getResourceLocation(),size=3.5,units='cm')
        self.stimuli['nontarget3'] = visual.ImageStim(win=self.task.window, image=nt3.getResourceLocation(),size=3.5,units='cm')
        self.stimuli['nontarget4'] = visual.ImageStim(win=self.task.window, image=nt4.getResourceLocation(),size=3.5,units='cm')
        self.stimuli['nontarget5'] = visual.ImageStim(win=self.task.window, image=nt5.getResourceLocation(),size=3.5,units='cm')

        #clear the instructions screen
        self.drawBackground(self.background)
        self.task.refreshWindow()
        self.disableResponse()

        # wait before display of initial trial in the block.

        self.wait(self.interStimulusDelay)

    def doBeforeTrial(self):
        """Configures the next trial or ends block if no more trials."""
        try:
            # get next trial data
            self.currentTrial = self.trialHandler.next()
        except StopIteration:  #no more trials
            self.setContinueTrial(False)
            self.setContinue(False)
            return
        #increment the trial counter
        self.currentTrialNum += 1
        #reset the trial "draw stage" variable
        self.trialDrawStage = 0

        #reset current response object with default values
        self.currentResponse = CPTResponse()
        self.currentResponse.block=self
        self.currentResponse.trialData = self.currentTrial
        self.currentResponse.trialNum=self.currentTrialNum
        self.currentResponse.responseDevice='none'
        self.currentResponse.taskTime=self.task.getTime()
        self.currentResponse.key='none'
        self.currentResponse.rt = 0

        #pre-set correct value for a non response
        if(self.currentResponse.trialData['stimulus']=='target'):
            self.currentResponse.corr = 0
        else:
            self.currentResponse.corr = 1

        self.lastResponse = None
        self.lastResponseTime = None
        self.lastResponseDevice = None
        self.resetClock()


    def doTrialTimeout(self):
         """Ends trial and determines if response was correct."""
         self.task.responses.addResponse(self.currentResponse)
         #increment total correct counter
         self.totalCorrect += self.currentResponse.corr


    def doBeforeTrialResponse(self):
        """Draws stimuli for stimuli display period"""
        if(self.trialDrawStage == 0):
            self.drawBackground(self.background)
            self.stimuli[self.currentTrial['stimulus']].draw()
            self.trialDrawStage = 1
            self.task.refreshWindow()
            self.enableResponse()
        if(self.trialDrawStage == 1 and self.getTime()>=self.stimulusDisplayDuration):
            self.drawBackground(self.background)
            self.trialDrawStage = 2
            self.task.refreshWindow()
        if(self.getTime()>=self.responseTimeLimit):
            self.disableResponse()


    def doAfterTrialResponse(self):
         """Records response."""

         #if this is the first response for the trial and it is a target trial then mark as correct
         if(self.currentResponse.rt==0):
             if(self.currentResponse.trialData['stimulus']=='target'):
                 self.currentResponse.corr=1
             else:
                 self.currentResponse.corr=0
         else:
            #not the first response, therefore incorrect trial
            self.currentResponse.corr=0

         #update response object with information about this latest response
         self.currentResponse.rt=self.lastResponseTime
         self.currentResponse.responses.append(self.lastResponseTime)
         self.currentResponse.taskTime=self.task.getTime()
         self.currentResponse.responseDevice = self.lastResponseDevice
         self.currentResponse.key=self.lastResponse

         #clear response data and continue trial
         self.lastResponse = None
         self.lastResponseDevice = None
         self.lastResponseTime = None
         self.setContinueTrial(True)





class CPTResponses(lavatask.base.TaskResponses):
    """Extends TaskResponses class to implement CPT specific summary scoring.

    Summary scoring for CPT is
        1) Count of correct responses
        2) Count of correct target trials
        3) Count of correct nontarget trials
        2) Mean of reaction times to correct target trials
        3) Median reaction time to correct target trials
        4) Stdev of reaction times to correct target trials
        5) performance_errors
        6) intrusion_errors
        7) ommission_errors


    There is also a total trials attempted score that helps identify incomplete testing sessions.)

    """
    def __init__(self,task):
        lavatask.base.TaskResponses.__init__(self,task)

    def getSummaryStatsColumns(self):
        """Return column names for the summary statistics."""
        columns = lavatask.base.TaskResponses.getSummaryStatsColumns(self)
        for column in ['response_device','total_trials','total_corr','total_errors','target_corr','target_errors',
        'target_mean','target_median','target_stdev',
        'nontarget_corr','nontarget_errors','performance_errors',
        ]:
            columns.append(column)
        return columns

    def getSummaryStatsFields(self):
        """Calculate the summary stats and return the data as a dictionary."""
        fields = lavatask.base.TaskResponses.getSummaryStatsFields(self)
        response_device=None

        target = []
        totalCorr = 0
        targetCorr = 0
        nontargetCorr = 0
        totalErrors = 0
        performanceErrors = 0
        nontargetErrors = 0
        targetErrors = 0
        testingTrialsAttempted=0

        #compile correct response data into groups for summary stats
        for response in self.data:
            if(response['block_name']=='testingBlock'):

                #update device type info
                if(response['response_device']!='none'):
                    if(response_device == None):
                        response_device = response['response_device']
                    elif (response_device != 'multiple' and response_device != response['response_device']): #changed <>
                        response_device = 'multiple'

                #update trials attempted
                testingTrialsAttempted+=1

                #handle incorrect trials
                if(response['resp_corr']==0):
                    totalErrors +=1
                    if(response['trial_extra_responses']!='none'):
                        performanceErrors+=1
                    else:
                        if(response['trial_stimulus']=='target'):
                            targetErrors+=1
                        else:
                            nontargetErrors+=1

                else:  #handle correct trials
                    totalCorr += 1
                    if(response['trial_stimulus']=='target'):
                        rt = response['resp_rt']
                        target.append(rt)
                        targetCorr+=1
                    else:
                        nontargetCorr+=1

        #do summary stats on each summary group and add to fields collection
        fields.update({'response_device':response_device})
        fields.update({'total_trials':testingTrialsAttempted})
        fields.update({'total_corr':totalCorr,'total_errors':totalErrors})
        fields.update({'target_corr':self.calcCorrect(target),'target_errors':targetErrors,'target_mean':self.calcMean(target),'target_median':self.calcMedian(target),'target_stdev':self.calcStDev(target)})
        fields.update({'nontarget_corr':nontargetCorr,'nontarget_errors':nontargetErrors,'performance_errors':performanceErrors})

        return fields



class CPTResponse(lavatask.base.TrialResponse):
    """Extends TrialResponse class to implement Flanker specific trial configuration in output files.

    """
    def __init__(self):
        lavatask.base.TrialResponse.__init__(self)
        self.responses=[] #custom field to record all key press times.
        self.extraResponses='none'
    def getTrialConfigurationFields(self):
        if(len(self.responses)>1):
            self.extraResponses = str(self.responses)
        """Returns the flanker specific trial configuration data as a dictionary."""
        return {'trial_stimulus':self.trialData.stimulus,'trial_extra_responses':self.extraResponses,}

    def getTrialConfigurationColumns(self):
        """Returns the flanker specific trial configuration column names."""
        return ['trial_stimulus','trial_extra_responses',]
