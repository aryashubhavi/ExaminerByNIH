#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Class library that provides extensions to the base LavaTask computer based task classes for the flanker task

:Classes:
    FlankerTask - extends Task class to implement block configuration and control of flow for the Flanker task.
    FlankerBlock - extends TrialBlock class to implement fixation points and other Flanker specific trial block functionality.
    FlankerResponses - extends TaskResponses class to implement Flanker specific summary scoring.
    FlankerResponse - extends TrialResponse class to implement Flanker specific trial configuration in output files.

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
from math import log10
import lavatask.base



class FlankerTask(lavatask.base.Task):
    """Extends Task class to implement block configuration and control of flow for the Flanker task.

    """
    def __init__(self,configuration,environment=None,sessionConfig=None):
        lavatask.base.Task.__init__(self,configuration,environment,sessionConfig)
        self.name='Flanker'
        self.version='3.2.0.1'
        self.versionDate='12/30/2011'
        self.responses = FlankerResponses(self)
        self.resourcePath = os.path.join(self.resourcePath,'examiner','flanker')
        self.graphicPositions = None

    def doBeforeTask(self):
        """Configure task blocks based on ageCohort of the task."""
        if(self.ageCohort=='Adult'):
                self.setupAdultTask()
        elif(self.ageCohort=='Child'):
                self.setupChildTask()
        #log error and quit if no configuration found for the ageCohort and language settings
        if(self.getBlockByName('testingBlock')==None):
            logging.error("Flanker task not configured.  AgeCohort=" + self.ageCohort +", Language=" + self.language + ".")
            core.quit();

    def doAfterBlock(self,block):
        """Perform task specific control of flow logic.

        If the subject gets 6 out of 8 trials correct in a practice trial then skip ahead to
        the real testing trial.  If the subject fails to get 6 out of 8 in 3 practice blocks then
        end the task.
        """
        if(block.name=="firstPracticeBlock" or block.name=="secondPracticeBlock"):
            #check whether we can skip the remaining practice blocks
            if(block.totalCorrect >= 6):
                self.setNextBlock("testingInstruct")
        if(block.name == "thirdPracticeBlock"):
            #check whether we should abort the task
            if(block.totalCorrect < 6):
                self.setNextBlock("completeInstruct")


    def setupAdultTask(self):
        """Configure task blocks for Adult stimuli and instructions for all languages."""

        lllll = lavatask.base.Resource('lllll.bmp',self)
        llrll = lavatask.base.Resource('llrll.bmp',self)

        firstPracticeInstruct = lavatask.base.InstructionBlock(self,"firstPracticeInstruct",['space',])
        firstPracticeInstruct.text = lavatask.base.UnicodeResource("practice.txt",self).getCenteredText()
        firstPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=lllll.getResourceLocation(),pos=[0,3.75],size=3.1,units='cm'))
        firstPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=llrll.getResourceLocation(),pos=[0,1.25],size=3.1,units='cm'))


        self.addBlock(firstPracticeInstruct)

        firstPracticeBlock = FlankerBlock(self,'firstPracticeBlock')
        firstPracticeBlock.beforeTrialDelay=0.400 #longer delay during practice
        firstPracticeBlock.initializeTrialData(1)
        firstPracticeBlock.displayFeedback = True
        self.addBlock(firstPracticeBlock)

        secondPracticeInstruct = lavatask.base.InstructionBlock(self,"secondPracticeInstruct",['space',])
        secondPracticeInstruct.text = lavatask.base.UnicodeResource("additional_practice.txt",self).getCenteredText()
        secondPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=lllll.getResourceLocation(),pos=[0,2.75],size=3.1,units='cm'))
        secondPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=llrll.getResourceLocation(),pos=[0,.25],size=3.1,units='cm'))

        self.addBlock(secondPracticeInstruct)

        secondPracticeBlock = FlankerBlock(self,'secondPracticeBlock')
        secondPracticeBlock.beforeTrialDelay=0.400 #longer delay during practice
        secondPracticeBlock.initializeTrialData(1)
        secondPracticeBlock.displayFeedback = True
        self.addBlock(secondPracticeBlock)


        thirdPracticeInstruct = lavatask.base.InstructionBlock(self,"thirdPracticeInstruct",['space',])
        thirdPracticeInstruct.text = secondPracticeInstruct.text #reuse text from first practice
        thirdPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=lllll.getResourceLocation(),pos=[0,2.75],size=3.1,units='cm'))
        thirdPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=llrll.getResourceLocation(),pos=[0,.25],size=3.1,units='cm'))
        self.addBlock(thirdPracticeInstruct)

        thirdPracticeBlock = FlankerBlock(self,'thirdPracticeBlock')
        thirdPracticeBlock.beforeTrialDelay=0.400 #longer delay during practice
        thirdPracticeBlock.initializeTrialData(1)
        thirdPracticeBlock.displayFeedback = True
        self.addBlock(thirdPracticeBlock)

        testingInstruct = lavatask.base.InstructionBlock(self,"testingInstruct",['space',])
        testingInstruct.text =  lavatask.base.UnicodeResource("testing.txt",self).getCenteredText()

        self.addBlock(testingInstruct)

        throwawayBlock = FlankerBlock(self,'throwawayBlock')
        throwawayBlock.initializeTrialData(1, [{'congruent': 0, 'arrows': 'llrll', 'upDown':'up','corrAns': 'right'},{'congruent': 1, 'arrows': 'lllll', 'upDown':'down','corrAns': 'left'},])
        self.addBlock(throwawayBlock)

        testingBlock = FlankerBlock(self,'testingBlock')
        testingBlock.initializeTrialData(6)
        self.addBlock(testingBlock)

        completeInstruct = lavatask.base.InstructionBlock(self,"completeInstruct")
        completeInstruct.text = lavatask.base.UnicodeResource("complete.txt",self).getCenteredText()
        self.addBlock(completeInstruct)



    def getGraphicPosition(self,block,graphic):
        """utility method to handle location of graphics on different platforms / languages"""



        if(self.graphicPositions == None):
            pos = {}
            pos['osx']={}
            pos['osx']['English']={}
            pos['osx']['English']['firstPracticeInstruct']={}
            pos['osx']['English']['firstPracticeInstruct']['r']=[-1.85,-.30]
            pos['osx']['English']['firstPracticeInstruct']['l']=[-1.85,-2.10]
            pos['osx']['English']['firstPracticeInstruct']['l_button']=[13,-2.10]
            pos['osx']['English']['firstPracticeInstruct']['r_button']=[13,-.30]
            pos['osx']['English']['secondPracticeInstruct']=pos['osx']['English']['firstPracticeInstruct']
            pos['osx']['English']['thirdPracticeInstruct']=pos['osx']['English']['firstPracticeInstruct']
            pos['osx']['English']['testingInstruct']={}
            pos['osx']['English']['testingInstruct']['r']=[-1.85,-.30]
            pos['osx']['English']['testingInstruct']['l']=[-1.85,-2.10]
            pos['osx']['English']['testingInstruct']['l_button']=[13,-2.10]
            pos['osx']['English']['testingInstruct']['r_button']=[13,-.30]
            pos['osx']['Spanish']={}
            pos['osx']['Spanish']['firstPracticeInstruct']={}
            pos['osx']['Spanish']['firstPracticeInstruct']['r']=[.3,-.30]
            pos['osx']['Spanish']['firstPracticeInstruct']['l']=[.3,-2.10]
            pos['osx']['Spanish']['firstPracticeInstruct']['l_button']=[13,-2.10]
            pos['osx']['Spanish']['firstPracticeInstruct']['r_button']=[13,-.30]
            pos['osx']['Spanish']['secondPracticeInstruct']=pos['osx']['Spanish']['firstPracticeInstruct']
            pos['osx']['Spanish']['thirdPracticeInstruct']=pos['osx']['Spanish']['firstPracticeInstruct']
            pos['osx']['Spanish']['testingInstruct']={}
            pos['osx']['Spanish']['testingInstruct']['r']=[.3,-.30]
            pos['osx']['Spanish']['testingInstruct']['l']=[.3,-2.10]
            pos['osx']['Spanish']['testingInstruct']['l_button']=[13,-2.10]
            pos['osx']['Spanish']['testingInstruct']['r_button']=[13,-.30]
            pos['osx']['Hebrew']={}
            pos['osx']['Hebrew']['firstPracticeInstruct']={}
            pos['osx']['Hebrew']['firstPracticeInstruct']['r']=[0.3,-.10]
            pos['osx']['Hebrew']['firstPracticeInstruct']['l']=[0.3,-1.90]
            pos['osx']['Hebrew']['firstPracticeInstruct']['l_button']=[-9.5,-1.90]
            pos['osx']['Hebrew']['firstPracticeInstruct']['r_button']=[-9.5,-.10]
            pos['osx']['Hebrew']['secondPracticeInstruct']=pos['osx']['Hebrew']['firstPracticeInstruct']
            pos['osx']['Hebrew']['thirdPracticeInstruct']=pos['osx']['Hebrew']['firstPracticeInstruct']
            pos['osx']['Hebrew']['testingInstruct']={}
            pos['osx']['Hebrew']['testingInstruct']['r']=[0.3,-.10]
            pos['osx']['Hebrew']['testingInstruct']['l']=[0.3,-1.90]
            pos['osx']['Hebrew']['testingInstruct']['l_button']=[-9.5,-1.90]
            pos['osx']['Hebrew']['testingInstruct']['r_button']=[-9.5,-.10]

            pos['windows']={}
            pos['windows']['English']={}
            pos['windows']['English']['firstPracticeInstruct']={}
            pos['windows']['English']['firstPracticeInstruct']['r']=[-1.85,-.30]
            pos['windows']['English']['firstPracticeInstruct']['l']=[-1.85,-2.30]
            pos['windows']['English']['firstPracticeInstruct']['l_button']=[13,-2.30]
            pos['windows']['English']['firstPracticeInstruct']['r_button']=[13,-.30]
            pos['windows']['English']['secondPracticeInstruct']=pos['windows']['English']['firstPracticeInstruct']
            pos['windows']['English']['thirdPracticeInstruct']=pos['windows']['English']['firstPracticeInstruct']
            pos['windows']['English']['testingInstruct']={}
            pos['windows']['English']['testingInstruct']['r']=[-1.85,-.30]
            pos['windows']['English']['testingInstruct']['l']=[-1.85,-2.30]
            pos['windows']['English']['testingInstruct']['l_button']=[13,-2.30]
            pos['windows']['English']['testingInstruct']['r_button']=[13,-.30]
            pos['windows']['Spanish']={}
            pos['windows']['Spanish']['firstPracticeInstruct']={}
            pos['windows']['Spanish']['firstPracticeInstruct']['r']=[.3,-.30]
            pos['windows']['Spanish']['firstPracticeInstruct']['l']=[.3,-2.30]
            pos['windows']['Spanish']['firstPracticeInstruct']['l_button']=[13,-2.30]
            pos['windows']['Spanish']['firstPracticeInstruct']['r_button']=[13,-.30]
            pos['windows']['Spanish']['secondPracticeInstruct']=pos['windows']['Spanish']['firstPracticeInstruct']
            pos['windows']['Spanish']['thirdPracticeInstruct']=pos['windows']['Spanish']['firstPracticeInstruct']
            pos['windows']['Spanish']['testingInstruct']={}
            pos['windows']['Spanish']['testingInstruct']['r']=[.3,-.30]
            pos['windows']['Spanish']['testingInstruct']['l']=[.3,-2.30]
            pos['windows']['Spanish']['testingInstruct']['l_button']=[13,-2.30]
            pos['windows']['Spanish']['testingInstruct']['r_button']=[13,-.30]
            pos['windows']['Hebrew']={}
            pos['windows']['Hebrew']['firstPracticeInstruct']={}
            pos['windows']['Hebrew']['firstPracticeInstruct']['r']=[-0.4,-.30]
            pos['windows']['Hebrew']['firstPracticeInstruct']['l']=[-0.4,-2.30]
            pos['windows']['Hebrew']['firstPracticeInstruct']['l_button']=[-10,-2.30]
            pos['windows']['Hebrew']['firstPracticeInstruct']['r_button']=[-10,-.30]
            pos['windows']['Hebrew']['secondPracticeInstruct']=pos['windows']['Hebrew']['firstPracticeInstruct']
            pos['windows']['Hebrew']['thirdPracticeInstruct']=pos['windows']['Hebrew']['firstPracticeInstruct']
            pos['windows']['Hebrew']['testingInstruct']={}
            pos['windows']['Hebrew']['testingInstruct']['r']=[-0.4,-.30]
            pos['windows']['Hebrew']['testingInstruct']['l']=[-0.4,-2.30]
            pos['windows']['Hebrew']['testingInstruct']['l_button']=[-10,-2.30]
            pos['windows']['Hebrew']['testingInstruct']['r_button']=[-10,-.30]

            pos['linux']={}
            pos['linux']['English']={}
            pos['linux']['English']['firstPracticeInstruct']={}
            pos['linux']['English']['firstPracticeInstruct']['r']=[-1.85,-.30]
            pos['linux']['English']['firstPracticeInstruct']['l']=[-1.85,-2.40]
            pos['linux']['English']['firstPracticeInstruct']['l_button']=[13,-2.40]
            pos['linux']['English']['firstPracticeInstruct']['r_button']=[13,-.30]
            pos['linux']['English']['secondPracticeInstruct']=pos['linux']['English']['firstPracticeInstruct']
            pos['linux']['English']['thirdPracticeInstruct']=pos['linux']['English']['firstPracticeInstruct']
            pos['linux']['English']['testingInstruct']={}
            pos['linux']['English']['testingInstruct']['r']=[-1.85,-.30]
            pos['linux']['English']['testingInstruct']['l']=[-1.85,-2.40]
            pos['linux']['English']['testingInstruct']['l_button']=[13,-2.40]
            pos['linux']['English']['testingInstruct']['r_button']=[13,-.30]
            pos['linux']['Spanish']={}
            pos['linux']['Spanish']['firstPracticeInstruct']={}
            pos['linux']['Spanish']['firstPracticeInstruct']['r']=[.3,-.30]
            pos['linux']['Spanish']['firstPracticeInstruct']['l']=[.3,-2.40]
            pos['linux']['Spanish']['firstPracticeInstruct']['l_button']=[13,-2.40]
            pos['linux']['Spanish']['firstPracticeInstruct']['r_button']=[13,-.30]
            pos['linux']['Spanish']['secondPracticeInstruct']=pos['linux']['Spanish']['firstPracticeInstruct']
            pos['linux']['Spanish']['thirdPracticeInstruct']=pos['linux']['Spanish']['firstPracticeInstruct']
            pos['linux']['Spanish']['testingInstruct']={}
            pos['linux']['Spanish']['testingInstruct']['r']=[.3,-.30]
            pos['linux']['Spanish']['testingInstruct']['l']=[.3,-2.40]
            pos['linux']['Spanish']['testingInstruct']['l_button']=[13,-2.40]
            pos['linux']['Spanish']['testingInstruct']['r_button']=[13,-.30]
            pos['linux']['Hebrew']={}
            pos['linux']['Hebrew']['firstPracticeInstruct']={}
            pos['linux']['Hebrew']['firstPracticeInstruct']['r']=[-0.4,-.30]
            pos['linux']['Hebrew']['firstPracticeInstruct']['l']=[-0.4,-2.40]
            pos['linux']['Hebrew']['firstPracticeInstruct']['l_button']=[-10,-2.40]
            pos['linux']['Hebrew']['firstPracticeInstruct']['r_button']=[-10,-.30]
            pos['linux']['Hebrew']['secondPracticeInstruct']=pos['linux']['Hebrew']['firstPracticeInstruct']
            pos['linux']['Hebrew']['thirdPracticeInstruct']=pos['linux']['Hebrew']['firstPracticeInstruct']
            pos['linux']['Hebrew']['testingInstruct']={}
            pos['linux']['Hebrew']['testingInstruct']['r']=[-0.4,-.30]
            pos['linux']['Hebrew']['testingInstruct']['l']=[-0.4,-2.40]
            pos['linux']['Hebrew']['testingInstruct']['l_button']=[-10,-2.40]
            pos['linux']['Hebrew']['testingInstruct']['r_button']=[-10,-.30]

            pos['undetermined']=pos['windows']
            self.graphicPositions = pos


        return self.graphicPositions[self.OS][self.language][block.name][graphic]




    def setupChildTask(self):
        """Configure task blocks for Child stimuli and instructions."""

        llrll = lavatask.base.Resource('llrll.bmp',self)
        fixation=lavatask.base.Resource('fixation.bmp',self)
        r = lavatask.base.Resource('r.bmp',self)
        r_button = lavatask.base.Resource('r_button.bmp',self)
        l = lavatask.base.Resource('l.bmp',self)
        l_button = lavatask.base.Resource('l_button.bmp',self)
        pracInstr = lavatask.base.UnicodeResource("practice.txt",self)


        firstPracticeInstruct = lavatask.base.InstructionBlock(self,"firstPracticeInstruct",['space',])
        firstPracticeInstruct.text  =  pracInstr.getCenteredText()
        firstPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=llrll.getResourceLocation(),pos=[-1,2.2],size=15,units='cm'))
        firstPracticeInstruct.addStim(visual.GratingStim(win=self.window, tex=fixation.getResourceLocation(),pos=[-1,1.1],size=.6,units='cm'))
        firstPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=r.getResourceLocation(),pos=self.getGraphicPosition(firstPracticeInstruct,'r'),size=1.5,units='cm'))
        firstPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=r_button.getResourceLocation(),pos=self.getGraphicPosition(firstPracticeInstruct,'r_button'),size=1,units='cm'))
        firstPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=l.getResourceLocation(),pos=self.getGraphicPosition(firstPracticeInstruct,'l'),size=1.5,units='cm'))
        firstPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=l_button.getResourceLocation(),pos=self.getGraphicPosition(firstPracticeInstruct,'l_button'),size=1,units='cm'))


        self.addBlock(firstPracticeInstruct)

        firstPracticeBlock = FlankerBlock(self,'firstPracticeBlock')
        firstPracticeBlock.beforeTrialDelay=0.400 #longer delay during practice
        firstPracticeBlock.initializeTrialData(1)
        firstPracticeBlock.displayFeedback = True
        self.addBlock(firstPracticeBlock)

        secondPracticeInstruct = lavatask.base.InstructionBlock(self,"secondPracticeInstruct",['space',])
        secondPracticeInstruct.text  =  pracInstr.getCenteredText()
        secondPracticeInstruct.addStim(visual.ImageStim(win=self.window, tex=llrll.getResourceLocation(),pos=[-1,2.2],size=15,units='cm'))
        secondPracticeInstruct.addStim(visual.GratingStim(win=self.window, tex=fixation.getResourceLocation(),pos=[-1,1.1],size=.6,units='cm'))
        secondPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=r.getResourceLocation(),pos=self.getGraphicPosition(secondPracticeInstruct,'r'),size=1.5,units='cm'))
        secondPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=r_button.getResourceLocation(),pos=self.getGraphicPosition(secondPracticeInstruct,'r_button'),size=1,units='cm'))
        secondPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=l.getResourceLocation(),pos=self.getGraphicPosition(secondPracticeInstruct,'l'),size=1.5,units='cm'))
        secondPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=l_button.getResourceLocation(),pos=self.getGraphicPosition(secondPracticeInstruct,'l_button'),size=1,units='cm'))

        self.addBlock(secondPracticeInstruct)

        secondPracticeBlock = FlankerBlock(self,'secondPracticeBlock')
        secondPracticeBlock.beforeTrialDelay=0.400 #longer delay during practice
        secondPracticeBlock.initializeTrialData(1)
        secondPracticeBlock.displayFeedback = True
        self.addBlock(secondPracticeBlock)


        thirdPracticeInstruct = lavatask.base.InstructionBlock(self,"thirdPracticeInstruct",['space',])
        thirdPracticeInstruct.text  =  pracInstr.getCenteredText()
        thirdPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=llrll.getResourceLocation(),pos=[-1,2.2],size=15,units='cm'))
        thirdPracticeInstruct.addStim(visual.GratingStim(win=self.window, tex=fixation.getResourceLocation(),pos=[-1,1.1],size=.6,units='cm'))
        thirdPracticeInstruct.addStim(visual.ImageStim(win=self.window, tex=r.getResourceLocation(),pos=self.getGraphicPosition(thirdPracticeInstruct,'r'),size=1.5,units='cm'))
        thirdPracticeInstruct.addStim(visual.ImageStim(win=self.window, tex=r_button.getResourceLocation(),pos=self.getGraphicPosition(thirdPracticeInstruct,'r_button'),size=1,units='cm'))
        thirdPracticeInstruct.addStim(visual.ImageStim(win=self.window, tex=l.getResourceLocation(),pos=self.getGraphicPosition(thirdPracticeInstruct,'l'),size=1.5,units='cm'))
        thirdPracticeInstruct.addStim(visual.ImageStim(win=self.window, tex=l_button.getResourceLocation(),pos=self.getGraphicPosition(thirdPracticeInstruct,'l_button'),size=1,units='cm'))
        self.addBlock(thirdPracticeInstruct)

        thirdPracticeBlock = FlankerBlock(self,'thirdPracticeBlock')
        thirdPracticeBlock.beforeTrialDelay=0.400 #longer delay during practice
        thirdPracticeBlock.initializeTrialData(1)
        thirdPracticeBlock.displayFeedback = True
        self.addBlock(thirdPracticeBlock)


        rpos = [-1.85,-.30]
        lpos = [-1.85,-2.10]
        rbpos = [13,-.30]
        lbpos = [13,-2.10]
        if(self.language == 'Spanish'):
            rpos = [.3,-.30]
            lpos = [.3,-2.10]
            rbpos = [13,-.30]
            lbpos = [13,-2.10]


        testingInstruct = lavatask.base.InstructionBlock(self,"testingInstruct",['space',])
        testingInstruct.text  =  lavatask.base.UnicodeResource("testing.txt",self).getCenteredText()
        testingInstruct.addStim(visual.ImageStim(win=self.window, image=llrll.getResourceLocation(),pos=[-1,2.2],size=15,units='cm'))
        testingInstruct.addStim(visual.GratingStim(win=self.window, tex=fixation.getResourceLocation(),pos=[-1,1.1],size=.6,units='cm'))
        testingInstruct.addStim(visual.ImageStim(win=self.window, image=r.getResourceLocation(),pos=self.getGraphicPosition(testingInstruct,'r'),size=1.5,units='cm'))
        testingInstruct.addStim(visual.ImageStim(win=self.window, image=r_button.getResourceLocation(),pos=self.getGraphicPosition(testingInstruct,'r_button'),size=1,units='cm'))
        testingInstruct.addStim(visual.ImageStim(win=self.window, image=l.getResourceLocation(),pos=self.getGraphicPosition(testingInstruct,'l'),size=1.5,units='cm'))
        testingInstruct.addStim(visual.ImageStim(win=self.window, image=l_button.getResourceLocation(),pos=self.getGraphicPosition(testingInstruct,'l_button'),size=1,units='cm'))
        self.addBlock(testingInstruct)

        throwawayBlock = FlankerBlock(self,'throwawayBlock')
        throwawayBlock.initializeTrialData(1, [{'congruent': 0, 'arrows': 'llrll', 'upDown':'up','corrAns': 'right'},{'congruent': 1, 'arrows': 'lllll', 'upDown':'down','corrAns': 'left'},])
        self.addBlock(throwawayBlock)

        testingBlock = FlankerBlock(self,'testingBlock')
        testingBlock.initializeTrialData(6)
        self.addBlock(testingBlock)

        completeInstruct = lavatask.base.InstructionBlock(self,"completeInstruct")
        completeInstruct.text = lavatask.base.UnicodeResource("complete.txt",self).getCenteredText()
        self.addBlock(completeInstruct)




class FlankerBlock(lavatask.base.TrialResponseBlock):
    """Extends TrialBlock class to implement fixation points and other Flanker specific trial block functionality.

    The flanker block runs a set number of trials (randomly ordered) and each trial has the following structure:
        1) Pre Trial Delay: 0.2 seconds in the real testing and 0.4 seconds in the practice blocks
        2) Fixation Period: displays fixation stimuli for at least 1 second and no more than 3 seconds (random)
        3) Stimuli Display: displays the trial stimuli for 4 seconds or until the subject provides a keyboard response
        4) Feedback Display: in practice trials, displays feedback to the subject about their response for 2 seconds
        5) Records response
    """
    def __init__(self,task,name,keys=["left","right"],trialData=None):
        lavatask.base.TrialResponseBlock.__init__(self,task,name,keys,trialData)
        self.beforeTrialDelay = 0.200 #default time between response and next fixation (this is set to 0.400 in practice trials)
        self.arrowsStimuli = None
        self.fixationStimuli = None
        self.correctStimuli = None
        self.incorrectStimuli = None
        self.noresponseStimuli = None
        self.displayFeedback = False # whether to display correct/incorrect feedback stimuli after each trial
        self.lastTrialCorrect = None  #the last trial result (correct = True, incorrect = False, None = No Response)
        self.displayFeedbackDuration = 2.0 #how long to display feedback
        self.upDownPositionOffset=1.0 #the number of cm to shift the stimuli up or down
        self.fixationBaseDuration=1.0 #standard amount of fixation time
        self.fixationVariationMaxMiliseconds=2000 # random portion of fixation duration
        self.currentTrialFixation=None
        self.totalCorrect=0 #count of the number of correct responses
        self.maxResponseTime=4.0 #default response time after arrows are displayed
        self.defaultTrialDataTemplate = [ \
        {'congruent': 0, 'arrows': 'llrll', 'upDown':'up','corrAns': 'right'},
        {'congruent': 1, 'arrows': 'lllll', 'upDown':'down','corrAns': 'left'},
        {'congruent': 0, 'arrows': 'rrlrr', 'upDown':'up','corrAns': 'left'},
        {'congruent': 1, 'arrows': 'rrrrr', 'upDown':'down','corrAns': 'right'},
        {'congruent': 0, 'arrows': 'llrll', 'upDown':'down','corrAns': 'right'},
        {'congruent': 1, 'arrows': 'lllll', 'upDown':'up','corrAns': 'left'},
        {'congruent': 0, 'arrows': 'rrlrr', 'upDown':'down','corrAns': 'left'},
        {'congruent': 1, 'arrows': 'rrrrr', 'upDown':'up','corrAns': 'right'},
        ]

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
        self.arrowsStimuli=visual.ImageStim(win=self.task.window, image=lavatask.base.Resource('rrrrr.bmp',self.task).getResourceLocation(),size=3.1,units='cm')
        self.fixationStimuli=visual.GratingStim(win=self.task.window, tex=lavatask.base.Resource('fixation.bmp',self.task).getResourceLocation(),size=.4,units='cm')
        if(self.task.ageCohort=='Child'):
           #child stimuli are larger
            self.arrowsStimuli=visual.ImageStim(win=self.task.window, image=lavatask.base.Resource('rrrrr.bmp',self.task).getResourceLocation(),size=15,units='cm')
            self.fixationStimuli=visual.GratingStim(win=self.task.window, tex=lavatask.base.Resource('fixation.bmp',self.task).getResourceLocation(),size=.6,units='cm')
            self.upDownPositionOffset=1.25  #increase offset to accomodate the larger stimuli.

        self.correctStimuli=visual.TextStim(win=self.task.window, ori=0,text=lavatask.base.UnicodeResource("feedback_correct.txt",self.task).getText(),pos=[0, 0], height=1, color=[-1,-1,1])
        self.incorrectStimuli=visual.TextStim(win=self.task.window, ori=0,text=lavatask.base.UnicodeResource("feedback_incorrect.txt",self.task).getText(),pos=[0, 0], height=1, color=[1,-1,-1])
        self.noresponseStimuli=visual.TextStim(win=self.task.window, ori=0,text=lavatask.base.UnicodeResource("feedback_no_response.txt",self.task).getText(),pos=[0, 0], height=1, color=[1,-1,-1])

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
        #setup the arrows stimuli for the trialData#setup stimuli
        self.arrowsStimuli.setImage(lavatask.base.Resource(self.currentTrial.arrows+'.bmp',self.task).getResourceLocation())
        if(self.currentTrial.upDown == 'down'):
           self.arrowsStimuli.setPos([0,(-1*self.upDownPositionOffset)])# removed ,units='cm'
        else:
           self.arrowsStimuli.setPos([0,self.upDownPositionOffset])

        #determine how long the fixation display will last
        randomFixationValue = randint(0,self.fixationVariationMaxMiliseconds)
        self.currentTrialFixation=self.fixationBaseDuration+ (randomFixationValue/1000.0000)

        #set trial timeout and reset clock
        self.trialTimeout = self.currentTrialFixation + self.maxResponseTime

        self.lastResponse = None
        self.lastResponseTime = None
        self.lastResponseDevice = None
        self.resetClock()

        #turn off response checking (until fixation period is over)
        self.disableResponse()


    def doTrialTimeout(self):
         """Handles timed out trial by recording a "none" response."""
         response = FlankerResponse()
         response.block=self
         response.trialData = self.currentTrial
         response.fixation = self.currentTrialFixation
         response.key='none'
         response.responseDevice = 'none'
         response.rt=0
         response.taskTime=self.task.getTime()
         response.trialNum=self.currentTrialNum
         response.corr=0
         self.task.responses.addResponse(response)
         self.lastTrialCorrect = None

    def doBeforeTrialResponse(self):
        """Draws fixation stimuli and once fixation period is over enables responses and draws stimuli."""
        if(self.trialDrawStage == 0):
            self.drawBackground("White")
            self.fixationStimuli.draw()
            self.trialDrawStage = 1
            self.task.refreshWindow()
        if(self.trialDrawStage == 1 and self.getTime()>=self.currentTrialFixation):
            self.drawBackground("White")
            self.arrowsStimuli.draw()
            self.fixationStimuli.draw()
            self.trialDrawStage = 2
            self.enableResponse()
            self.task.refreshWindow()

    def doAfterTrialResponse(self):
         """Checks correctness of response and records response data."""
         response = FlankerResponse()
         response.block=self
         response.trialData = self.currentTrial
         response.fixation = self.currentTrialFixation
         response.key=self.lastResponse
         response.responseDevice = self.lastResponseDevice
         response.rt=(self.lastResponseTime-self.currentTrialFixation)
         response.taskTime=self.task.getTime()
         response.trialNum=self.currentTrialNum
         if(response.key == response.trialData.corrAns):
            response.corr=1
            self.totalCorrect += 1
         else:
            response.corr=0
         self.lastTrialCorrect=response.corr
         self.task.responses.addResponse(response)


    def doAfterTrial(self):
        """Draws response feedback if enabled for block."""
        if(self.displayFeedback):
            self.drawBackground("White")
            if(self.lastTrialCorrect == True):
                self.correctStimuli.draw()
            elif(self.lastTrialCorrect == False):
                self.incorrectStimuli.draw()
            else:
                self.noresponseStimuli.draw()
            self.task.refreshWindow()
            self.wait(self.displayFeedbackDuration)




class FlankerResponses(lavatask.base.TaskResponses):
    """Extends TaskResponses class to implement Flanker specific summary scoring.

    Summary scoring for Flanker is
        1) Count of correct responses
        2) Mean of reaction times to correct responses
        3) Median reaction time to correct responses
        4) Stdev of reaction times to correct responses

    These scoring values are calculated for:
        1) Overall Total (all trials)
        2) Congruent Trials
        3) Incongruent Trials
        4) Left Trials
        5) Right Trials
        6) Up Trials
        7) Down Trials

    There is also a total trials attempted score that helps identify incomplete testing sessions.  (for the purposes of the
    scoring a "none" response trial is considered to be "attempted")

    flanker_score and flanker_error_diff are calculated values used for scale and composite score generation.

    """
    def __init__(self,task):
        lavatask.base.TaskResponses.__init__(self,task)

    def getSummaryStatsColumns(self):
        """Return column names for the summary statistics."""
        columns = lavatask.base.TaskResponses.getSummaryStatsColumns(self)
        for column in ['response_device','total_trials','flanker_score','flanker_error_diff','total_corr','total_mean','total_median','total_stdev',
        'congr_corr','congr_mean','congr_median','congr_stdev',
        'incongr_corr','incongr_mean','incongr_median','incongr_stdev',
        'left_corr','left_mean','left_median','left_stdev',
        'right_corr','right_mean','right_median','right_stdev',
        'up_corr','up_mean','up_median','up_stdev',
        'down_corr','down_mean','down_median','down_stdev',
        ]:
            columns.append(column)
        return columns

    def getSummaryStatsFields(self):
        """Calculate the summary stats and return the data as a dictionary."""
        fields = lavatask.base.TaskResponses.getSummaryStatsFields(self)
        response_device=None
        total = []
        congruent=[]
        incongruent=[]
        up=[]
        down=[]
        left=[]
        right=[]
        testingTrialsAttempted=0
        #compile correct response data into groups for summary stats
        for response in self.data:
            if(response['block_name']=='testingBlock'):
                if(response['response_device']!='none'):
                    if(response_device == None):
                        response_device = response['response_device']
                    elif (response_device == 'multiple' and response_device == response['response_device']):
                        response_device = 'multiple'
                testingTrialsAttempted+=1
                if(response['resp_corr']==1):
                    rt = response['resp_rt']
                    total.append(rt)
                    if(response['trial_corrResp']=='left'):left.append(rt)
                    if(response['trial_corrResp']=='right'):right.append(rt)
                    if(response['trial_upDown']=='up'):up.append(rt)
                    if(response['trial_upDown']=='down'):down.append(rt)
                    if(response['trial_congruent']==0):incongruent.append(rt)
                    if(response['trial_congruent']==1):congruent.append(rt)

        #do summary stats on each summary group and add to fields collection
        fields.update({'response_device':response_device})
        fields.update({'total_trials':testingTrialsAttempted})
        fields.update({'total_corr':self.calcCorrect(total),'total_mean':self.calcMean(total),'total_median':self.calcMedian(total),'total_stdev':self.calcStDev(total)})
        fields.update({'congr_corr':self.calcCorrect(congruent),'congr_mean':self.calcMean(congruent),'congr_median':self.calcMedian(congruent),'congr_stdev':self.calcStDev(congruent)})
        fields.update({'incongr_corr':self.calcCorrect(incongruent),'incongr_mean':self.calcMean(incongruent),'incongr_median':self.calcMedian(incongruent),'incongr_stdev':self.calcStDev(incongruent)})
        fields.update({'left_corr':self.calcCorrect(left),'left_mean':self.calcMean(left),'left_median':self.calcMedian(left),'left_stdev':self.calcStDev(left)})
        fields.update({'right_corr':self.calcCorrect(right),'right_mean':self.calcMean(right),'right_median':self.calcMedian(right),'right_stdev':self.calcStDev(right)})
        fields.update({'up_corr':self.calcCorrect(up),'up_mean':self.calcMean(up),'up_median':self.calcMedian(up),'up_stdev':self.calcStDev(up)})
        fields.update({'down_corr':self.calcCorrect(down),'down_mean':self.calcMean(down),'down_median':self.calcMedian(down),'down_stdev':self.calcStDev(down)})

        flanker_score = self.calcFlankerScore(fields)
        flanker_error_diff = self.calcErrorDiff(fields)
        fields.update({'flanker_score':flanker_score,'flanker_error_diff':flanker_error_diff})
        return fields

    def calcFlankerScore(self,fields,noCalcValue=-5):
        """Calculate the Flanker score."""
        incongr_corr = fields['incongr_corr']
        incongr_median = fields['incongr_median']

        if(fields['total_trials']!=48 or incongr_corr == noCalcValue or incongr_median == noCalcValue): #changed <> before 48
            return noCalcValue;

        accuracy_score = (incongr_corr / 24.0) * 5.0

        if(incongr_median < 0.500):
            #performance ceiling is 500 milliseconds
            incongr_median = 0.500
        if(incongr_median > 3.000):
            #performance floor is 3 seconds
            incongr_median = 3.000
        incongr_median_adjusted = (log10(incongr_median)-log10(0.500))/(log10(3.000)-log10(0.500))
        reaction_time_score = 5 - (5 * incongr_median_adjusted)
        return round(accuracy_score + reaction_time_score,3)

    def calcErrorDiff(self,fields,noCalcValue=-5):
        """Calculate difference in errors from incongrument condition to congruent conditions."""
        incongr_corr = fields['incongr_corr']
        congr_corr = fields['congr_corr']
        if(fields['total_trials']!=48 or incongr_corr == noCalcValue or congr_corr == noCalcValue): #changed<> before 48
            return noCalcValue;
        return ((24-incongr_corr) - (24-congr_corr))





class FlankerResponse(lavatask.base.TrialResponse):
    """Extends TrialResponse class to implement Flanker specific trial configuration in output files.

    """
    def __init__(self):
        lavatask.base.TrialResponse.__init__(self)
        # this data field is used to record the random fixation period of
        # each trial (output to allow validation of randomness if needed)
        self.fixation = None

    def getTrialConfigurationFields(self):
        """Returns the flanker specific trial configuration data as a dictionary."""
        return {'trial_congruent':self.trialData.congruent,'trial_arrows':self.trialData.arrows,'trial_upDown':self.trialData.upDown,'trial_corrResp':self.trialData.corrAns,'trial_fixation':self.fixation,}

    def getTrialConfigurationColumns(self):
        """Returns the flanker specific trial configuration column names."""
        return ['trial_congruent','trial_arrows','trial_upDown','trial_corrResp','trial_fixation',]


#CHANGES
#1. PatchStim (deprecated) to ImageStim
#2. removed units from setPos
