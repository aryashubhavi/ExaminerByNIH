#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Class library that provides extensions to the base LavaTask computer based task classes for the Saccades task

:Classes:
    SaccadesTask - extends Task class to implement block configuration and control of flow for the Saccades task
    SaccadesBlock - extends TrialBlock class to implement Saccades specific trial block functionality.

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
from psychopy import core, sound, data, event, visual, gui, logging
from random import randint
import lavatask.base



class SaccadesTask(lavatask.base.Task):
    """Extends Task class to implement block configuration and control of flow for the Saccades Task.

    """
    def __init__(self,configuration,environment=None,sessionConfig=None):
        lavatask.base.Task.__init__(self,configuration,environment,sessionConfig)
        self.name='Saccades'
        self.version='3.2.0.1'
        self.versionDate='12/30/2011'
        self.resourcePath = os.path.join(self.resourcePath,'examiner','saccades')


    def doBeforeTask(self):
        """Configure task blocks based on ageCohort and language of the task."""
        self.setupTask()
        #log error and quit if no configuration found for the ageCohort and language settings
        if(self.getBlockByName('prosaccades')==None):
            logging.error("Saccades not configured.  AgeCohort=" + self.ageCohort +", Language=" + self.language + ".")
            core.quit();


    def setupTask(self):
        """Configure task blocks for Adult stimuli and instructions."""

        #Setup administrator audio cues
        #refactor this location finding into the resource base code
        audioResourcePath = os.path.normpath(os.path.join(self.resourcePath,"audio"))
        self.audioCues = [ \
        0,
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"one.wav"))),
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"two.wav"))),
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"three.wav"))),
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"four.wav"))),
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"five.wav"))),
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"six.wav"))),
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"seven.wav"))),
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"eight.wav"))),
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"nine.wav"))),
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"ten.wav"))),
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"eleven.wav"))),
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"twelve.wav"))),
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"thirteen.wav"))),
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"fourteen.wav"))),
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"fifteen.wav"))),
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"sixteen.wav"))),
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"seventeen.wav"))),
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"eighteen.wav"))),
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"nineteen.wav"))),
        sound.Sound(os.path.normpath(os.path.join(audioResourcePath,"twenty.wav"))),
        ]


        prosaccadesInstr = lavatask.base.InstructionBlock(self,"prosaccadesInstr",['space',],"White","Black")
        prosaccadesInstr.text = lavatask.base.UnicodeResource("prosaccades.txt",self).getCenteredText()
        self.addBlock(prosaccadesInstr)

        prosaccadesBlock = SaccadesBlock(self,'prosaccades')
        prosaccadesBlock.initializeTrialData()
        self.addBlock(prosaccadesBlock)

        antipracticeInstr = lavatask.base.InstructionBlock(self,"antipracticeInstr",['space',],"White","Black")
        antipracticeInstr.text = lavatask.base.UnicodeResource("antipractice.txt",self).getCenteredText()
        self.addBlock(antipracticeInstr)

        antipracticeBlock = SaccadesBlock(self,'antipractice')
        antipracticeBlock.initializeTrialData()
        self.addBlock(antipracticeBlock)

        antisaccades1Instr = lavatask.base.InstructionBlock(self,"antisaccades1Instr",['space',],"White","Black")
        antisaccades1Instr.text = lavatask.base.UnicodeResource("antisaccades1.txt",self).getCenteredText()
        self.addBlock(antisaccades1Instr)

        antisaccades1Block = SaccadesBlock(self,'antisaccades1')
        antisaccades1Block.initializeTrialData()
        self.addBlock(antisaccades1Block)

        antisaccades2Instr = lavatask.base.InstructionBlock(self,"antisaccades2Instr",['space',],"White","Black")
        antisaccades2Instr.text = lavatask.base.UnicodeResource("antisaccades2.txt",self).getCenteredText()
        self.addBlock(antisaccades2Instr)

        antisaccades2Block = SaccadesBlock(self,'antisaccades2')
        antisaccades2Block.initializeTrialData()
        self.addBlock(antisaccades2Block)

        completeInstruct = lavatask.base.InstructionBlock(self,"completeInstr",['space'],"White","Black")
        completeInstruct.text = lavatask.base.UnicodeResource("complete.txt",self).getCenteredText()
        self.addBlock(completeInstruct)



class SaccadesBlock(lavatask.base.TrialResponseBlock):
    """Extends TrialBlock class to implement  Saccades specific trial block functionality.


    """
    def __init__(self,task,name,keys=["left"],numTargets=20,trialData=None):
        lavatask.base.TrialResponseBlock.__init__(self,task,name,keys,trialData)
        self.beforeBlockDelay = 1.0 # one second delay before block
        self.background="Black"
        self.centerTargetDuration = 1.0
        self.beforeSaccadeTargetDelay = 0.200
        self.prosaccadeDuration = 0.900
        self.antisaccadeDuration = 1.000
        self.dataTemplates = {}

        self.dataTemplates['prosaccades_a'] = [ \
        {'trial_number':1,'trial_direction':'left'},
        {'trial_number':2,'trial_direction':'right'},
        {'trial_number':3,'trial_direction':'right'},
        {'trial_number':4,'trial_direction':'right'},
        {'trial_number':5,'trial_direction':'left'},
        {'trial_number':6,'trial_direction':'left'},
        {'trial_number':7,'trial_direction':'right'},
        {'trial_number':8,'trial_direction':'left'},
        {'trial_number':9,'trial_direction':'left'},
        {'trial_number':10,'trial_direction':'right'},
        ]

        self.dataTemplates['antipractice_a'] = [ \
        {'trial_number':1,'trial_direction':'left'},
        {'trial_number':2,'trial_direction':'right'},
        {'trial_number':3,'trial_direction':'left'},
        ]

        self.dataTemplates['antisaccades1_a'] = [ \
        {'trial_number':1,'trial_direction':'right'},
        {'trial_number':2,'trial_direction':'left'},
        {'trial_number':3,'trial_direction':'left'},
        {'trial_number':4,'trial_direction':'right'},
        {'trial_number':5,'trial_direction':'right'},
        {'trial_number':6,'trial_direction':'right'},
        {'trial_number':7,'trial_direction':'left'},
        {'trial_number':8,'trial_direction':'left'},
        {'trial_number':9,'trial_direction':'right'},
        {'trial_number':10,'trial_direction':'left'},
        {'trial_number':11,'trial_direction':'right'},
        {'trial_number':12,'trial_direction':'right'},
        {'trial_number':13,'trial_direction':'right'},
        {'trial_number':14,'trial_direction':'left'},
        {'trial_number':15,'trial_direction':'left'},
        {'trial_number':16,'trial_direction':'right'},
        {'trial_number':17,'trial_direction':'left'},
        {'trial_number':18,'trial_direction':'left'},
        {'trial_number':19,'trial_direction':'right'},
        {'trial_number':20,'trial_direction':'right'},
        ]

        self.dataTemplates['antisaccades2_a'] = [ \
        {'trial_number':1,'trial_direction':'right'},
        {'trial_number':2,'trial_direction':'right'},
        {'trial_number':3,'trial_direction':'right'},
        {'trial_number':4,'trial_direction':'left'},
        {'trial_number':5,'trial_direction':'left'},
        {'trial_number':6,'trial_direction':'right'},
        {'trial_number':7,'trial_direction':'left'},
        {'trial_number':8,'trial_direction':'left'},
        {'trial_number':9,'trial_direction':'right'},
        {'trial_number':10,'trial_direction':'right'},
        {'trial_number':11,'trial_direction':'right'},
        {'trial_number':12,'trial_direction':'left'},
        {'trial_number':13,'trial_direction':'right'},
        {'trial_number':14,'trial_direction':'left'},
        {'trial_number':15,'trial_direction':'left'},
        {'trial_number':16,'trial_direction':'right'},
        {'trial_number':17,'trial_direction':'right'},
        {'trial_number':18,'trial_direction':'left'},
        {'trial_number':19,'trial_direction':'left'},
        {'trial_number':20,'trial_direction':'left'},
        ]

        self.dataTemplates['prosaccades_b'] = [ \
        {'trial_number':1,'trial_direction':'left'},
        {'trial_number':2,'trial_direction':'left'},
        {'trial_number':3,'trial_direction':'right'},
        {'trial_number':4,'trial_direction':'left'},
        {'trial_number':5,'trial_direction':'right'},
        {'trial_number':6,'trial_direction':'left'},
        {'trial_number':7,'trial_direction':'right'},
        {'trial_number':8,'trial_direction':'right'},
        {'trial_number':9,'trial_direction':'right'},
        {'trial_number':10,'trial_direction':'left'},
        ]

        self.dataTemplates['antipractice_b'] = [ \
        {'trial_number':1,'trial_direction':'left'},
        {'trial_number':2,'trial_direction':'right'},
        {'trial_number':3,'trial_direction':'left'},
        ]

        self.dataTemplates['antisaccades1_b'] = [ \
        {'trial_number':1,'trial_direction':'left'},
        {'trial_number':2,'trial_direction':'right'},
        {'trial_number':3,'trial_direction':'left'},
        {'trial_number':4,'trial_direction':'left'},
        {'trial_number':5,'trial_direction':'right'},
        {'trial_number':6,'trial_direction':'left'},
        {'trial_number':7,'trial_direction':'left'},
        {'trial_number':8,'trial_direction':'right'},
        {'trial_number':9,'trial_direction':'left'},
        {'trial_number':10,'trial_direction':'right'},
        {'trial_number':11,'trial_direction':'right'},
        {'trial_number':12,'trial_direction':'left'},
        {'trial_number':13,'trial_direction':'right'},
        {'trial_number':14,'trial_direction':'left'},
        {'trial_number':15,'trial_direction':'left'},
        {'trial_number':16,'trial_direction':'right'},
        {'trial_number':17,'trial_direction':'right'},
        {'trial_number':18,'trial_direction':'right'},
        {'trial_number':19,'trial_direction':'left'},
        {'trial_number':20,'trial_direction':'right'},
        ]

        self.dataTemplates['antisaccades2_b'] = [ \
        {'trial_number':1,'trial_direction':'right'},
        {'trial_number':2,'trial_direction':'left'},
        {'trial_number':3,'trial_direction':'left'},
        {'trial_number':4,'trial_direction':'right'},
        {'trial_number':5,'trial_direction':'left'},
        {'trial_number':6,'trial_direction':'right'},
        {'trial_number':7,'trial_direction':'right'},
        {'trial_number':8,'trial_direction':'left'},
        {'trial_number':9,'trial_direction':'right'},
        {'trial_number':10,'trial_direction':'left'},
        {'trial_number':11,'trial_direction':'right'},
        {'trial_number':12,'trial_direction':'left'},
        {'trial_number':13,'trial_direction':'left'},
        {'trial_number':14,'trial_direction':'right'},
        {'trial_number':15,'trial_direction':'left'},
        {'trial_number':16,'trial_direction':'left'},
        {'trial_number':17,'trial_direction':'right'},
        {'trial_number':18,'trial_direction':'right'},
        {'trial_number':19,'trial_direction':'right'},
        {'trial_number':20,'trial_direction':'left'},
        ]

        self.dataTemplates['prosaccades_c'] = [ \
        {'trial_number':1,'trial_direction':'right'},
        {'trial_number':2,'trial_direction':'left'},
        {'trial_number':3,'trial_direction':'left'},
        {'trial_number':4,'trial_direction':'right'},
        {'trial_number':5,'trial_direction':'right'},
        {'trial_number':6,'trial_direction':'left'},
        {'trial_number':7,'trial_direction':'right'},
        {'trial_number':8,'trial_direction':'left'},
        {'trial_number':9,'trial_direction':'right'},
        {'trial_number':10,'trial_direction':'left'},
        ]

        self.dataTemplates['antipractice_c'] = [ \
        {'trial_number':1,'trial_direction':'left'},
        {'trial_number':2,'trial_direction':'right'},
        {'trial_number':3,'trial_direction':'left'},
        ]

        self.dataTemplates['antisaccades1_c'] = [ \
        {'trial_number':1,'trial_direction':'right'},
        {'trial_number':2,'trial_direction':'right'},
        {'trial_number':3,'trial_direction':'left'},
        {'trial_number':4,'trial_direction':'right'},
        {'trial_number':5,'trial_direction':'right'},
        {'trial_number':6,'trial_direction':'left'},
        {'trial_number':7,'trial_direction':'right'},
        {'trial_number':8,'trial_direction':'left'},
        {'trial_number':9,'trial_direction':'left'},
        {'trial_number':10,'trial_direction':'left'},
        {'trial_number':11,'trial_direction':'right'},
        {'trial_number':12,'trial_direction':'left'},
        {'trial_number':13,'trial_direction':'right'},
        {'trial_number':14,'trial_direction':'left'},
        {'trial_number':15,'trial_direction':'left'},
        {'trial_number':16,'trial_direction':'right'},
        {'trial_number':17,'trial_direction':'left'},
        {'trial_number':18,'trial_direction':'right'},
        {'trial_number':19,'trial_direction':'left'},
        {'trial_number':20,'trial_direction':'right'},
        ]

        self.dataTemplates['antisaccades2_c'] = [ \
        {'trial_number':1,'trial_direction':'right'},
        {'trial_number':2,'trial_direction':'left'},
        {'trial_number':3,'trial_direction':'left'},
        {'trial_number':4,'trial_direction':'right'},
        {'trial_number':5,'trial_direction':'left'},
        {'trial_number':6,'trial_direction':'left'},
        {'trial_number':7,'trial_direction':'right'},
        {'trial_number':8,'trial_direction':'left'},
        {'trial_number':9,'trial_direction':'right'},
        {'trial_number':10,'trial_direction':'left'},
        {'trial_number':11,'trial_direction':'right'},
        {'trial_number':12,'trial_direction':'right'},
        {'trial_number':13,'trial_direction':'right'},
        {'trial_number':14,'trial_direction':'left'},
        {'trial_number':15,'trial_direction':'right'},
        {'trial_number':16,'trial_direction':'right'},
        {'trial_number':17,'trial_direction':'left'},
        {'trial_number':18,'trial_direction':'right'},
        {'trial_number':19,'trial_direction':'right'},
        {'trial_number':20,'trial_direction':'left'},
        ]


    def initializeTrialData(self):
        """Configures the trialData handler using data template for the form and blockname

        """
        form = self.task.form
        if(form==None):
            form = 'a'

        dataTemplate = self.dataTemplates[self.name + '_' + form.lower()]
        if(dataTemplate != None):
            self.trialHandler = data.TrialHandler(dataTemplate,1,method="sequential")
        else:
            logging.error("Error configuring saccades block for Form = " + form + " and block=" + self.name + ".")
            core.quit();

    def doBeforeTrialBlock(self):
        """Sets up common stimuli for the block."""


        target = lavatask.base.Resource('target.bmp',self.task)

        self.centerTarget = visual.ImageStim(win=self.task.window, image=target.getResourceLocation(),pos=[0,0],size=.3,units='cm')
        self.leftTarget = visual.ImageStim(win=self.task.window, image=target.getResourceLocation(),pos=[-12,0],size=.3,units='cm')
        self.rightTarget = visual.ImageStim(win=self.task.window, image=target.getResourceLocation(),pos=[12,0],size=.3,units='cm')

        #clear the instructions screen
        self.drawBackground(self.background)
        self.task.refreshWindow()
        self.disableResponse()

        # self.wait(self.interStimulusDelay)

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

        if(self.name == 'prosaccades'):
            self.saccadeDuration = self.prosaccadeDuration
        else:
            self.saccadeDuration = self.antisaccadeDuration


        #generate a random inter trial delay value
        randomDelayMs = randint(0,500) / (1000.000)
        if(self.currentTrial.trial_number % 2 == 0):
            # if the trial number is even, use 1.0 second as the base delay
            randomDelayMs += 1.000
        else:
            #if trial number is add , use 1.5 sec as the base delay
            randomDelayMs = 1.500


        # set timeout
        self.trialTimeout = self.centerTargetDuration + self.beforeSaccadeTargetDelay + self.saccadeDuration + randomDelayMs

        #set utility timing values
        self.timeToSaccadeDisplay = self.centerTargetDuration+self.beforeSaccadeTargetDelay
        self.timeToSaccadeCompletion = self.timeToSaccadeDisplay + self.saccadeDuration

        self.resetClock()

    def doTrialTimeout(self):
         """Ends trial and determines if response was correct."""
         #self.task.responses.addResponse(self.currentResponse)


    def doBeforeTrialResponse(self):
        """Draws stimuli for stimuli display period"""
        if(self.trialDrawStage == 0):
            self.drawBackground(self.background)
            self.centerTarget.draw()
            self.trialDrawStage = 1
            self.task.refreshWindow()
            self.task.audioCues[self.currentTrial.trial_number].play()
            #self.enableResponse()
        if(self.trialDrawStage == 1 and self.getTime()>=self.centerTargetDuration):
            self.drawBackground(self.background)
            self.trialDrawStage = 2
            self.task.refreshWindow()
        if(self.trialDrawStage == 2 and self.getTime()>=self.timeToSaccadeDisplay):
            self.drawBackground(self.background)
            if(self.currentTrial.trial_direction=='left'):
                self.leftTarget.draw()
            else:
                self.rightTarget.draw()
            self.trialDrawStage = 3
            self.task.refreshWindow()
        if(self.trialDrawStage == 3 and self.getTime()>=self.timeToSaccadeCompletion):
            self.trialDrawStage = 4
            self.drawBackground(self.background)
            self.task.refreshWindow()
