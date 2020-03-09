#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Class library that provides extensions to the base LavaTask computer based task classes for the set shifting task

:Classes:
    SetShiftingTask - extends Task class to implement block configuration and control of flow for the set shifting task
    SetShiftingBlock - extends TrialBlock class to implement set shifting specific trial block functionality.
    SetShiftingResponses - extends TaskResponses class to implement set shifting specific summary scoring.
    SetShiftingResponse - extends TrialResponse class to implement set shifting specific trial configuration in output files.
    SetShiftingInstructionBlock - extends base InstructionBlock to support playing audio stimuli in response to keypress

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
from random import randint, choice
from math import log10
import lavatask.base



class SetShiftingTask(lavatask.base.Task):
    """Extends Task class to implement block configuration and control of flow for the Set Shifting Task.

    """
    def __init__(self,configuration,environment=None,sessionConfig=None):
        lavatask.base.Task.__init__(self,configuration,environment,sessionConfig)
        self.name='SetShifting'
        self.version='3.2.0.1'
        self.versionDate='12/30/2011'
        self.responses = SetShiftingResponses(self)
        self.resourcePath = os.path.join(self.resourcePath,'examiner','setshifting')
        self.colorFirst = None #Whether to start with color or shape first, if None, it is randomly determined
        self.graphicPositions = None

    def doBeforeTask(self):
        """Configure task blocks based on ageCohort and language of the task."""
        if(self.ageCohort=='Adult'):
            self.setupAdultTask()
        elif(self.ageCohort=='Child'):
            self.setupChildTask()
        #log error and quit if no configuration found for the ageCohort and language settings
        if(self.getBlockByName('testingBlock')==None):
            logging.error("Set Shifting not configured.  AgeCohort=" + self.ageCohort +", Language=" + self.language + ".")
            core.quit();

    def doAfterBlock(self,block):
        """Perform task specific control of flow logic.

        If the subject gets 12 out of 16 trials correct in a practice trial then skip ahead to
        the real testing trial.  If the subject fails to get 12 out of 16 in 3 practice blocks then
        end the task.
        """
        if(block.name=="firstPracticeBlock" or block.name=="secondPracticeBlock"):
            #check whether we can skip the remaining practice blocks
            if(block.totalCorrect >= 12):
                self.setNextBlock("testingInstruct")
        if(block.name == "thirdPracticeBlock"):
            #check whether we should abort the task
            if(block.totalCorrect < 12):
                self.setNextBlock("completeInstruct")


    def setupAdultTask(self):
        """Configure task blocks for Adult stimuli and instructions."""

        #randomly determining starting condition if not specified
        if(self.colorFirst == None):
            self.colorFirst = choice([True,False])


        tri_red = lavatask.base.Resource('tri_red.bmp',self)
        rect_blue = lavatask.base.Resource('rect_blue.bmp',self)
        rect_red = lavatask.base.Resource('rect_red.bmp',self)
        shape_cue = lavatask.base.UnicodeResource('shape_cue.txt',self)

        firstPracticeInstruct = lavatask.base.InstructionBlock(self,"firstPracticeInstruct",['space',],"White","Black")
        firstPracticeInstruct.text = lavatask.base.UnicodeResource("practice.txt",self).getCenteredText()
        firstPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=tri_red.getResourceLocation(),pos=[-7,-7],size=3.5,units='cm'))
        firstPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=rect_blue.getResourceLocation(),pos=[7,-7],size=3.5,units='cm'))
        firstPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=rect_red.getResourceLocation(),pos=[0,0],size=3.5,units='cm'))
        firstPracticeInstruct.addStim(visual.TextStim(win=self.window, ori=0,text=shape_cue.getText(),pos=[0, -7],\
            alignHoriz = 'center',alignVert='center',height=1, units="cm",color=firstPracticeInstruct.foreground))
        self.addBlock(firstPracticeInstruct)



        firstPracticeInstruct2 = lavatask.base.InstructionBlock(self,"firstPracticeInstruct2",['space',],"White","Black")
        firstPracticeInstruct2.text = lavatask.base.UnicodeResource("practice2.txt",self).getCenteredText()
        firstPracticeInstruct2.addStim(visual.ImageStim(win=self.window, image=tri_red.getResourceLocation(),pos=[-7,-7],size=3.5,units='cm'))
        firstPracticeInstruct2.addStim(visual.ImageStim(win=self.window, image=rect_blue.getResourceLocation(),pos=[7,-7],size=3.5,units='cm'))
        firstPracticeInstruct2.addStim(visual.ImageStim(win=self.window, image=rect_red.getResourceLocation(),pos=[0,0],size=3.5,units='cm'))
        firstPracticeInstruct2.addStim(visual.TextStim(win=self.window, ori=0,text=shape_cue.getText(),pos=[0,-7],\
            alignHoriz = 'center',alignVert='center',height=1, units="cm",color=firstPracticeInstruct.foreground))
        self.addBlock(firstPracticeInstruct2)




        firstPracticeBlock = SetShiftingBlock(self,'firstPracticeBlock')
        firstPracticeBlock.initializeTrialData(self.colorFirst,4,4,None)
        firstPracticeBlock.displayFeedback = True
        self.addBlock(firstPracticeBlock)


        secondPracticeInstruct = lavatask.base.InstructionBlock(self,"secondPracticeInstruct",['space',],"White","Black")
        secondPracticeInstruct.text = lavatask.base.UnicodeResource("additional_practice.txt",self).getCenteredText()
        secondPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=tri_red.getResourceLocation(),pos=[-7,-7],size=3.5,units='cm'))
        secondPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=rect_blue.getResourceLocation(),pos=[7,-7],size=3.5,units='cm'))
        secondPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=rect_red.getResourceLocation(),pos=[0,0],size=3.5,units='cm'))
        secondPracticeInstruct.addStim(visual.TextStim(win=self.window, ori=0,text=shape_cue.getText(),pos=[0, -7],\
            alignHoriz = 'center',alignVert='center',height=1, units="cm",color=firstPracticeInstruct.foreground))
        self.addBlock(secondPracticeInstruct)

        secondPracticeBlock = SetShiftingBlock(self,'secondPracticeBlock')
        secondPracticeBlock.initializeTrialData(self.colorFirst,4,4,None)
        secondPracticeBlock.displayFeedback = True
        self.addBlock(secondPracticeBlock)


        thirdPracticeInstruct = lavatask.base.InstructionBlock(self,"thirdPracticeInstruct",['space',],"White","Black")
        thirdPracticeInstruct.text = lavatask.base.UnicodeResource("additional_practice.txt",self).getCenteredText()
        thirdPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=tri_red.getResourceLocation(),pos=[-7,-7],size=3.5,units='cm'))
        thirdPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=rect_blue.getResourceLocation(),pos=[7,-7],size=3.5,units='cm'))
        thirdPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=rect_red.getResourceLocation(),pos=[0,0],size=3.5,units='cm'))
        thirdPracticeInstruct.addStim(visual.TextStim(win=self.window, ori=0,text=shape_cue.getText(),pos=[0,-7],\
            alignHoriz = 'center',alignVert='center',height=1, units="cm",color=firstPracticeInstruct.foreground))
        self.addBlock(thirdPracticeInstruct)

        thirdPracticeBlock = SetShiftingBlock(self,'thirdPracticeBlock')
        thirdPracticeBlock.initializeTrialData(self.colorFirst,4,4,None)
        thirdPracticeBlock.displayFeedback = True
        self.addBlock(thirdPracticeBlock)


        testingInstruct = lavatask.base.InstructionBlock(self,"testingInstruct",['space',],"White","Black")
        testingInstruct.text = lavatask.base.UnicodeResource("testing.txt",self).getCenteredText()
        testingInstruct.addStim(visual.ImageStim(win=self.window, image=tri_red.getResourceLocation(),pos=[-7,-7],size=3.5,units='cm'))
        testingInstruct.addStim(visual.ImageStim(win=self.window, image=rect_blue.getResourceLocation(),pos=[7,-7],size=3.5,units='cm'))
        testingInstruct.addStim(visual.ImageStim(win=self.window, image=rect_red.getResourceLocation(),pos=[0,0],size=3.5,units='cm'))
        testingInstruct.addStim(visual.TextStim(win=self.window, ori=0,text=shape_cue.getText(),pos=[0, -7],\
            alignHoriz = 'center',alignVert='center',height=1, units="cm",color=firstPracticeInstruct.foreground))
        self.addBlock(testingInstruct)

        throwawayBlock = SetShiftingBlock(self,'throwawayBlock')
        if(self.colorFirst):
            throwawayBlock.initializeTrialData(self.colorFirst,1,None,None)
        else:
            throwawayBlock.initializeTrialData(self.colorFirst,None,1,None)

        self.addBlock(throwawayBlock)

        testingBlock = SetShiftingBlock(self,'testingBlock')
        testingBlock.initializeTrialData(self.colorFirst,10,10,16)
        testingBlock.beforeBlockDelay = None #skip delay because of throwaway block preceding this one.
        self.addBlock(testingBlock)

        completeInstruct = lavatask.base.InstructionBlock(self,"completeInstruct",['space'],"White","Black")
        completeInstruct.text = lavatask.base.UnicodeResource("complete.txt",self).getCenteredText()
        self.addBlock(completeInstruct)


    def getGraphicPosition(self,block,graphic):
        """utility method to handle location of graphics on different platforms / languages"""


        if(self.graphicPositions == None):
            pos = {}
            pos['osx']={}
            pos['osx']['English']={}
            pos['osx']['English']['firstPracticeInstruct2']={}
            pos['osx']['English']['firstPracticeInstruct2']['tri_red']=[-6.6,5.6]
            pos['osx']['English']['firstPracticeInstruct2']['rect_blue']=[-6.6,4.3]
            pos['osx']['English']['firstPracticeInstruct2']['left_button']=[12,5.5]
            pos['osx']['English']['firstPracticeInstruct2']['right_button']=[12,4.3]
            pos['osx']['English']['secondPracticeInstruct']={}
            pos['osx']['English']['secondPracticeInstruct']['tri_red']=[-6.6,5.35]
            pos['osx']['English']['secondPracticeInstruct']['rect_blue']=[-6.6,4]
            pos['osx']['English']['secondPracticeInstruct']['left_button']=[11.75,5.30]
            pos['osx']['English']['secondPracticeInstruct']['right_button']=[11.75,4]
            pos['osx']['English']['thirdPracticeInstruct']=pos['osx']['English']['secondPracticeInstruct']
            pos['osx']['English']['testingInstruct']={}
            pos['osx']['English']['testingInstruct']['tri_red']=[-6.6,-1.70]
            pos['osx']['English']['testingInstruct']['rect_blue']=[-6.6,-2.9]
            pos['osx']['English']['testingInstruct']['left_button']=[12,-1.80]
            pos['osx']['English']['testingInstruct']['right_button']=[12,-2.95]
            pos['osx']['Spanish']={}
            pos['osx']['Spanish']['firstPracticeInstruct2']={}
            pos['osx']['Spanish']['firstPracticeInstruct2']['tri_red']=[-4.9,5.6]
            pos['osx']['Spanish']['firstPracticeInstruct2']['rect_blue']=[-4.9,4.3]
            pos['osx']['Spanish']['firstPracticeInstruct2']['left_button']=[12,5.5]
            pos['osx']['Spanish']['firstPracticeInstruct2']['right_button']=[12,4.3]
            pos['osx']['Spanish']['secondPracticeInstruct']={}
            pos['osx']['Spanish']['secondPracticeInstruct']['tri_red']=[-5.1,5.35]
            pos['osx']['Spanish']['secondPracticeInstruct']['rect_blue']=[-5.1,4]
            pos['osx']['Spanish']['secondPracticeInstruct']['left_button']=[11.75,5.30]
            pos['osx']['Spanish']['secondPracticeInstruct']['right_button']=[11.75,4]
            pos['osx']['Spanish']['thirdPracticeInstruct']=pos['osx']['Spanish']['secondPracticeInstruct']
            pos['osx']['Spanish']['testingInstruct']={}
            pos['osx']['Spanish']['testingInstruct']['tri_red']=[-5.3,-1.70]
            pos['osx']['Spanish']['testingInstruct']['rect_blue']=[-5.3,-2.9]
            pos['osx']['Spanish']['testingInstruct']['left_button']=[12,-1.80]
            pos['osx']['Spanish']['testingInstruct']['right_button']=[12,-2.95]
            pos['osx']['Hebrew']={}
            pos['osx']['Hebrew']['firstPracticeInstruct2']={}
            pos['osx']['Hebrew']['firstPracticeInstruct2']['tri_red']=[4.1,5.6]
            pos['osx']['Hebrew']['firstPracticeInstruct2']['rect_blue']=[4.1,4.3]
            pos['osx']['Hebrew']['firstPracticeInstruct2']['left_button']=[-8.1,5.5]
            pos['osx']['Hebrew']['firstPracticeInstruct2']['right_button']=[-8.1,4.3]
            pos['osx']['Hebrew']['secondPracticeInstruct']={}
            pos['osx']['Hebrew']['secondPracticeInstruct']['tri_red']=[3.9,5.35]
            pos['osx']['Hebrew']['secondPracticeInstruct']['rect_blue']=[3.9,4]
            pos['osx']['Hebrew']['secondPracticeInstruct']['left_button']=[-8.1,5.30]
            pos['osx']['Hebrew']['secondPracticeInstruct']['right_button']=[-8.1,4]
            pos['osx']['Hebrew']['thirdPracticeInstruct']=pos['osx']['Hebrew']['secondPracticeInstruct']
            pos['osx']['Hebrew']['testingInstruct']={}
            pos['osx']['Hebrew']['testingInstruct']['tri_red']=[3.9,-1.60]
            pos['osx']['Hebrew']['testingInstruct']['rect_blue']=[3.9,-2.8]
            pos['osx']['Hebrew']['testingInstruct']['left_button']=[-8.1,-1.70]
            pos['osx']['Hebrew']['testingInstruct']['right_button']=[-8.1,-2.85]

            pos['windows']={}
            pos['windows']['English']={}
            pos['windows']['English']['firstPracticeInstruct2']={}
            pos['windows']['English']['firstPracticeInstruct2']['tri_red']=[-6.7,6.1]
            pos['windows']['English']['firstPracticeInstruct2']['rect_blue']=[-6.7,4.8]
            pos['windows']['English']['firstPracticeInstruct2']['left_button']=[12,6.1]
            pos['windows']['English']['firstPracticeInstruct2']['right_button']=[12,4.8]
            pos['windows']['English']['secondPracticeInstruct']={}
            pos['windows']['English']['secondPracticeInstruct']['tri_red']=[-6.7,5.85]
            pos['windows']['English']['secondPracticeInstruct']['rect_blue']=[-6.7,4.5]
            pos['windows']['English']['secondPracticeInstruct']['left_button']=[11.75,5.80]
            pos['windows']['English']['secondPracticeInstruct']['right_button']=[11.75,4.5]
            pos['windows']['English']['thirdPracticeInstruct']=pos['windows']['English']['secondPracticeInstruct']
            pos['windows']['English']['testingInstruct']={}
            pos['windows']['English']['testingInstruct']['tri_red']=[-6.7,-2.00]
            pos['windows']['English']['testingInstruct']['rect_blue']=[-6.7,-3.2]
            pos['windows']['English']['testingInstruct']['left_button']=[12,-2.05]
            pos['windows']['English']['testingInstruct']['right_button']=[12,-3.25]
            pos['windows']['Spanish']={}
            pos['windows']['Spanish']['firstPracticeInstruct2']={}
            pos['windows']['Spanish']['firstPracticeInstruct2']['tri_red']=[-4.9,6.1]
            pos['windows']['Spanish']['firstPracticeInstruct2']['rect_blue']=[-4.9,4.8]
            pos['windows']['Spanish']['firstPracticeInstruct2']['left_button']=[11.6,6.1]
            pos['windows']['Spanish']['firstPracticeInstruct2']['right_button']=[11.6,4.8]
            pos['windows']['Spanish']['secondPracticeInstruct']={}
            pos['windows']['Spanish']['secondPracticeInstruct']['tri_red']=[-5.1,5.85]
            pos['windows']['Spanish']['secondPracticeInstruct']['rect_blue']=[-5.1,4.5]
            pos['windows']['Spanish']['secondPracticeInstruct']['left_button']=[11.6,5.80]
            pos['windows']['Spanish']['secondPracticeInstruct']['right_button']=[11.6,4.5]
            pos['windows']['Spanish']['thirdPracticeInstruct']=pos['windows']['Spanish']['secondPracticeInstruct']
            pos['windows']['Spanish']['testingInstruct']={}
            pos['windows']['Spanish']['testingInstruct']['tri_red']=[-5.3,-1.9]
            pos['windows']['Spanish']['testingInstruct']['rect_blue']=[-5.3,-3.2]
            pos['windows']['Spanish']['testingInstruct']['left_button']=[11.4,-1.9]
            pos['windows']['Spanish']['testingInstruct']['right_button']=[11.4,-3.2]
            pos['windows']['Hebrew']={}
            pos['windows']['Hebrew']['firstPracticeInstruct2']={}
            pos['windows']['Hebrew']['firstPracticeInstruct2']['tri_red']=[4.1,6.1]
            pos['windows']['Hebrew']['firstPracticeInstruct2']['rect_blue']=[4.1,4.8]
            pos['windows']['Hebrew']['firstPracticeInstruct2']['left_button']=[-8.1,6.1]
            pos['windows']['Hebrew']['firstPracticeInstruct2']['right_button']=[-8.1,4.8]
            pos['windows']['Hebrew']['secondPracticeInstruct']={}
            pos['windows']['Hebrew']['secondPracticeInstruct']['tri_red']=[3.9,5.85]
            pos['windows']['Hebrew']['secondPracticeInstruct']['rect_blue']=[3.9,4.5]
            pos['windows']['Hebrew']['secondPracticeInstruct']['left_button']=[-8.1,5.80]
            pos['windows']['Hebrew']['secondPracticeInstruct']['right_button']=[-8.1,4.5]
            pos['windows']['Hebrew']['thirdPracticeInstruct']=pos['windows']['Hebrew']['secondPracticeInstruct']
            pos['windows']['Hebrew']['testingInstruct']={}
            pos['windows']['Hebrew']['testingInstruct']['tri_red']=[3.7,-2.00]
            pos['windows']['Hebrew']['testingInstruct']['rect_blue']=[3.7,-3.2]
            pos['windows']['Hebrew']['testingInstruct']['left_button']=[-8.3,-2.05]
            pos['windows']['Hebrew']['testingInstruct']['right_button']=[-8.3,-3.25]

            pos['linux']={}
            pos['linux']['English']={}
            pos['linux']['English']['firstPracticeInstruct2']={}
            pos['linux']['English']['firstPracticeInstruct2']['tri_red']=[-6.7,6.5]
            pos['linux']['English']['firstPracticeInstruct2']['rect_blue']=[-6.7,5.2]
            pos['linux']['English']['firstPracticeInstruct2']['left_button']=[12,6.5]
            pos['linux']['English']['firstPracticeInstruct2']['right_button']=[12,5.2]
            pos['linux']['English']['secondPracticeInstruct']={}
            pos['linux']['English']['secondPracticeInstruct']['tri_red']=[-6.7,6.35]
            pos['linux']['English']['secondPracticeInstruct']['rect_blue']=[-6.7,4.9]
            pos['linux']['English']['secondPracticeInstruct']['left_button']=[11.75,6.30]
            pos['linux']['English']['secondPracticeInstruct']['right_button']=[11.75,4.9]
            pos['linux']['English']['thirdPracticeInstruct']=pos['linux']['English']['secondPracticeInstruct']
            pos['linux']['English']['testingInstruct']={}
            pos['linux']['English']['testingInstruct']['tri_red']=[-6.7,-2.00]
            pos['linux']['English']['testingInstruct']['rect_blue']=[-6.7,-3.4]
            pos['linux']['English']['testingInstruct']['left_button']=[12,-2.05]
            pos['linux']['English']['testingInstruct']['right_button']=[12,-3.45]
            pos['linux']['Spanish']={}
            pos['linux']['Spanish']['firstPracticeInstruct2']={}
            pos['linux']['Spanish']['firstPracticeInstruct2']['tri_red']=[-4.9,6.5]
            pos['linux']['Spanish']['firstPracticeInstruct2']['rect_blue']=[-4.9,5.2]
            pos['linux']['Spanish']['firstPracticeInstruct2']['left_button']=[11.6,6.5]
            pos['linux']['Spanish']['firstPracticeInstruct2']['right_button']=[11.6,5.2]
            pos['linux']['Spanish']['secondPracticeInstruct']={}
            pos['linux']['Spanish']['secondPracticeInstruct']['tri_red']=[-5.1,6.25]
            pos['linux']['Spanish']['secondPracticeInstruct']['rect_blue']=[-5.1,4.9]
            pos['linux']['Spanish']['secondPracticeInstruct']['left_button']=[11.6,6.20]
            pos['linux']['Spanish']['secondPracticeInstruct']['right_button']=[11.6,4.9]
            pos['linux']['Spanish']['thirdPracticeInstruct']=pos['linux']['Spanish']['secondPracticeInstruct']
            pos['linux']['Spanish']['testingInstruct']={}
            pos['linux']['Spanish']['testingInstruct']['tri_red']=[-5.3,-2.1]
            pos['linux']['Spanish']['testingInstruct']['rect_blue']=[-5.3,-3.5]
            pos['linux']['Spanish']['testingInstruct']['left_button']=[11.4,-2.1]
            pos['linux']['Spanish']['testingInstruct']['right_button']=[11.4,-3.5]
            pos['linux']['Hebrew']={}
            pos['linux']['Hebrew']['firstPracticeInstruct2']={}
            pos['linux']['Hebrew']['firstPracticeInstruct2']['tri_red']=[4.1,6.5]
            pos['linux']['Hebrew']['firstPracticeInstruct2']['rect_blue']=[4.1,5.2]
            pos['linux']['Hebrew']['firstPracticeInstruct2']['left_button']=[-8.1,6.5]
            pos['linux']['Hebrew']['firstPracticeInstruct2']['right_button']=[-8.1,5.2]
            pos['linux']['Hebrew']['secondPracticeInstruct']={}
            pos['linux']['Hebrew']['secondPracticeInstruct']['tri_red']=[3.9,6.35]
            pos['linux']['Hebrew']['secondPracticeInstruct']['rect_blue']=[3.9,4.9]
            pos['linux']['Hebrew']['secondPracticeInstruct']['left_button']=[-8.1,6.30]
            pos['linux']['Hebrew']['secondPracticeInstruct']['right_button']=[-8.1,4.9]
            pos['linux']['Hebrew']['thirdPracticeInstruct']=pos['linux']['Hebrew']['secondPracticeInstruct']
            pos['linux']['Hebrew']['testingInstruct']={}
            pos['linux']['Hebrew']['testingInstruct']['tri_red']=[3.7,-2.00]
            pos['linux']['Hebrew']['testingInstruct']['rect_blue']=[3.7,-3.4]
            pos['linux']['Hebrew']['testingInstruct']['left_button']=[-8.3,-2.05]
            pos['linux']['Hebrew']['testingInstruct']['right_button']=[-8.3,-3.45]

            pos['undetermined']=pos['windows']
            self.graphicPositions = pos


        return self.graphicPositions[self.OS][self.language][block.name][graphic]




    def setupChildTask(self):
        """Configure task blocks for Child stimuli and instructions."""

        #randomly determining starting condition if not specified
        if(self.colorFirst == None):
            self.colorFirst = choice([True,False])


        tri_red = lavatask.base.Resource('tri_red.bmp',self)
        rect_blue = lavatask.base.Resource('rect_blue.bmp',self)
        rect_red = lavatask.base.Resource('rect_red.bmp',self)
        shape_cue = lavatask.base.UnicodeResource('shape_cue.txt',self)
        left_button = lavatask.base.Resource('l_button.bmp',self)
        right_button = lavatask.base.Resource('r_button.bmp',self)


        firstPracticeInstruct = SetShiftingInstructionBlock(self,"firstPracticeInstruct","White","Black")
        firstPracticeInstruct.text = lavatask.base.UnicodeResource("practice.txt",self).getCenteredText()
        firstPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=tri_red.getResourceLocation(),pos=[-7,-7],size=3.5,units='cm'))
        firstPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=rect_blue.getResourceLocation(),pos=[7,-7],size=3.5,units='cm'))
        firstPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=rect_red.getResourceLocation(),pos=[0,0],size=3.5,units='cm'))
        firstPracticeInstruct.addStim(visual.TextStim(win=self.window, ori=0,text=shape_cue.getText(),pos=[0, -7],\
            alignHoriz = 'center',alignVert='center',height=1, units="cm",color=firstPracticeInstruct.foreground))
        self.addBlock(firstPracticeInstruct)


        firstPracticeInstruct2 = SetShiftingInstructionBlock(self,"firstPracticeInstruct2","White","Black")
        firstPracticeInstruct2.text = lavatask.base.UnicodeResource("practice2.txt",self).getCenteredText()
        firstPracticeInstruct2.addStim(visual.ImageStim(win=self.window, image=tri_red.getResourceLocation(),pos=[-7,-7],size=3.5,units='cm'))
        firstPracticeInstruct2.addStim(visual.ImageStim(win=self.window, image=rect_blue.getResourceLocation(),pos=[7,-7],size=3.5,units='cm'))
        firstPracticeInstruct2.addStim(visual.ImageStim(win=self.window, image=rect_red.getResourceLocation(),pos=[0,0],size=3.5,units='cm'))
        firstPracticeInstruct2.addStim(visual.ImageStim(win=self.window, image=left_button.getResourceLocation(),pos=self.getGraphicPosition(firstPracticeInstruct2,'left_button'),size=1,units='cm'))
        firstPracticeInstruct2.addStim(visual.ImageStim(win=self.window, image=right_button.getResourceLocation(),pos=self.getGraphicPosition(firstPracticeInstruct2,'right_button'),size=1,units='cm'))
        firstPracticeInstruct2.addStim(visual.ImageStim(win=self.window, image=tri_red.getResourceLocation(),pos=self.getGraphicPosition(firstPracticeInstruct2,'tri_red'),size=1.5,units='cm'))
        firstPracticeInstruct2.addStim(visual.ImageStim(win=self.window, tex=rect_blue.getResourceLocation(),pos=self.getGraphicPosition(firstPracticeInstruct2,'rect_blue'),size=1.5,units='cm'))
        firstPracticeInstruct2.addStim(visual.TextStim(win=self.window, ori=0,text=shape_cue.getText(),pos=[0,-7],\
            alignHoriz = 'center',alignVert='center',height=1, units="cm",color=firstPracticeInstruct.foreground))
        self.addBlock(firstPracticeInstruct2)


        firstPracticeBlock = SetShiftingBlock(self,'firstPracticeBlock')
        firstPracticeBlock.initializeTrialData(self.colorFirst,4,4,None)
        firstPracticeBlock.displayFeedback = True
        self.addBlock(firstPracticeBlock)


        secondPracticeInstruct = SetShiftingInstructionBlock(self,"secondPracticeInstruct","White","Black")
        secondPracticeInstruct.text = lavatask.base.UnicodeResource("additional_practice.txt",self).getCenteredText()
        secondPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=tri_red.getResourceLocation(),pos=[-7,-7],size=3.5,units='cm'))
        secondPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=rect_blue.getResourceLocation(),pos=[7,-7],size=3.5,units='cm'))
        secondPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=rect_red.getResourceLocation(),pos=[0,0],size=3.5,units='cm'))
        secondPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=left_button.getResourceLocation(),pos=self.getGraphicPosition(secondPracticeInstruct,'left_button'),size=1,units='cm'))
        secondPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=right_button.getResourceLocation(),pos=self.getGraphicPosition(secondPracticeInstruct,'right_button'),size=1,units='cm'))
        secondPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=tri_red.getResourceLocation(),pos=self.getGraphicPosition(secondPracticeInstruct,'tri_red'),size=1.5,units='cm'))
        secondPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=rect_blue.getResourceLocation(),pos=self.getGraphicPosition(secondPracticeInstruct,'rect_blue'),size=1.5,units='cm'))
        secondPracticeInstruct.addStim(visual.TextStim(win=self.window, ori=0,text=shape_cue.getText(),pos=[0, -7],\
            alignHoriz = 'center',alignVert='center',height=1, units="cm",color=firstPracticeInstruct.foreground))
        self.addBlock(secondPracticeInstruct)

        secondPracticeBlock = SetShiftingBlock(self,'secondPracticeBlock')
        secondPracticeBlock.initializeTrialData(self.colorFirst,4,4,None)
        secondPracticeBlock.displayFeedback = True
        self.addBlock(secondPracticeBlock)


        thirdPracticeInstruct = SetShiftingInstructionBlock(self,"thirdPracticeInstruct","White","Black")
        thirdPracticeInstruct.text = lavatask.base.UnicodeResource("additional_practice.txt",self).getCenteredText()
        thirdPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=tri_red.getResourceLocation(),pos=[-7,-7],size=3.5,units='cm'))
        thirdPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=rect_blue.getResourceLocation(),pos=[7,-7],size=3.5,units='cm'))
        thirdPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=rect_red.getResourceLocation(),pos=[0,0],size=3.5,units='cm'))
        thirdPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=left_button.getResourceLocation(),pos=self.getGraphicPosition(thirdPracticeInstruct,'left_button'),size=1,units='cm'))
        thirdPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=right_button.getResourceLocation(),pos=self.getGraphicPosition(thirdPracticeInstruct,'right_button'),size=1,units='cm'))
        thirdPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=tri_red.getResourceLocation(),pos=self.getGraphicPosition(thirdPracticeInstruct,'tri_red'),size=1.5,units='cm'))
        thirdPracticeInstruct.addStim(visual.ImageStim(win=self.window, image=rect_blue.getResourceLocation(),pos=self.getGraphicPosition(thirdPracticeInstruct,'rect_blue'),size=1.5,units='cm'))
        thirdPracticeInstruct.addStim(visual.TextStim(win=self.window, ori=0,text=shape_cue.getText(),pos=[0,-7],\
            alignHoriz = 'center',alignVert='center',height=1, units="cm",color=firstPracticeInstruct.foreground))
        self.addBlock(thirdPracticeInstruct)

        thirdPracticeBlock = SetShiftingBlock(self,'thirdPracticeBlock')
        thirdPracticeBlock.initializeTrialData(self.colorFirst,4,4,None)
        thirdPracticeBlock.displayFeedback = True
        self.addBlock(thirdPracticeBlock)


        testingInstruct = SetShiftingInstructionBlock(self,"testingInstruct","White","Black")
        testingInstruct.text = lavatask.base.UnicodeResource("testing.txt",self).getCenteredText()
        testingInstruct.addStim(visual.ImageStim(win=self.window, image=tri_red.getResourceLocation(),pos=[-7,-7],size=3.5,units='cm'))
        testingInstruct.addStim(visual.ImageStim(win=self.window, image=rect_blue.getResourceLocation(),pos=[7,-7],size=3.5,units='cm'))
        testingInstruct.addStim(visual.ImageStim(win=self.window, image=rect_red.getResourceLocation(),pos=[0,0],size=3.5,units='cm'))
        testingInstruct.addStim(visual.ImageStim(win=self.window, image=left_button.getResourceLocation(),pos=self.getGraphicPosition(testingInstruct,'left_button'),size=1,units='cm'))
        testingInstruct.addStim(visual.ImageStim(win=self.window, image=right_button.getResourceLocation(),pos=self.getGraphicPosition(testingInstruct,'right_button'),size=1,units='cm'))
        testingInstruct.addStim(visual.ImageStim(win=self.window, image=tri_red.getResourceLocation(),pos=self.getGraphicPosition(testingInstruct,'tri_red'),size=1.5,units='cm'))
        testingInstruct.addStim(visual.ImageStim(win=self.window, image=rect_blue.getResourceLocation(),pos=self.getGraphicPosition(testingInstruct,'rect_blue'),size=1.5,units='cm'))
        testingInstruct.addStim(visual.TextStim(win=self.window, ori=0,text=shape_cue.getText(),pos=[0, -7],\
            alignHoriz = 'center',alignVert='center',height=1, units="cm",color=firstPracticeInstruct.foreground))
        self.addBlock(testingInstruct)

        throwawayBlock = SetShiftingBlock(self,'throwawayBlock')
        if(self.colorFirst):
            throwawayBlock.initializeTrialData(self.colorFirst,1,None,None)
        else:
            throwawayBlock.initializeTrialData(self.colorFirst,None,1,None)

        self.addBlock(throwawayBlock)

        testingBlock = SetShiftingBlock(self,'testingBlock')
        testingBlock.initializeTrialData(self.colorFirst,10,10,16)
        testingBlock.beforeBlockDelay = None #skip delay because of throwaway block preceding this one.
        self.addBlock(testingBlock)

        completeInstruct = lavatask.base.InstructionBlock(self,"completeInstruct",['space'],"White","Black")
        completeInstruct.text = lavatask.base.UnicodeResource("complete.txt",self).getCenteredText()
        self.addBlock(completeInstruct)





class SetShiftingBlock(lavatask.base.TrialResponseBlock):
    """Extends TrialBlock class to implement Set Shifting specific trial block functionality.

    The Set Shifting block runs a set number of trials (randomly ordered) and each trial has the following structure:
        1) Delay: 800 ms
        2) Condition Cue: 800 ms
        3) fixation Cue: 200 ms
        4) target image: 5 seconds (or until response)
        5) feedback during practice: 2 seconds

    """
    def __init__(self,task,name,keys=["left","right"],trialData=None):
        lavatask.base.TrialResponseBlock.__init__(self,task,name,keys,trialData)
        self.beforeBlockDelay = 1.0 # one second delay before block
        self.stimuli = {}
        self.lastTrialCorrect = None  #the last trial result (correct = True, incorrect = False)
        self.totalCorrect=0 #count of the number of correct responses
        self.initialDelay=.800 #length of delay at beginning of trial
        self.cueDuration=.800 #length of time the condition cue is displayed before fixation
        self.fixationDuration=.200 #length of time to display the fixation cue
        self.targetDuration=.800 #length of time to display the target
        self.targetDisplayTime=self.initialDelay+self.cueDuration+self.fixationDuration
        self.trialTimeout = self.targetDisplayTime + 5.0  #trial times out 5 seconds after target display
        self.displayFeedback = False # whether to display correct/incorrect feedback stimuli after each trial
        self.feedbackDuration = 2.0
        self.background="Black"
        self.lastCue=None # used to track the condition cue in switching blocks to identify switch conditions
        self.colorDataTemplate = [ \
        {'condition':'color','cue': 'color', 'corr_resp': 'left'},
        {'condition':'color','cue': 'color', 'corr_resp': 'right'},]

        self.shapeDataTemplate = [ \
        {'condition':'shape','cue': 'shape', 'corr_resp': 'left'},
        {'condition':'shape','cue': 'shape', 'corr_resp': 'right'},]

        self.shiftDataTemplate = [ \
        {'condition':'shift','cue': 'color', 'corr_resp': 'left'},
        {'condition':'shift','cue': 'color', 'corr_resp': 'right'},
        {'condition':'shift','cue': 'shape', 'corr_resp': 'left'},
        {'condition':'shift','cue': 'shape', 'corr_resp': 'right'},]



    def initializeTrialData(self,colorFirst,colorReps,shapeReps,shiftReps):
        """Configures trialhandler with set shifting trials.

        Whereas normally the different conditions would be coded as separate blocks, there
        are reasons to consider them as sets of trials within one 'block'
        (e.g. number correct across color / shape trials during practice to proceed to test block).

        The shift trials are handled to ensure that there are between 45% and 55% shifted trials

        :parameters:
            colorFirst - whether to begin the block with color trials or shape trials
            colorReps - the number of times to repeat the color trials in the block.
            shapeReps - the number of times to repeat the shape trials in the block.
            shiftReps - the number of times to repeat the shift trials in the block.

        """



        colorTrials = []
        colorCheckPassed = False
        shapeTrials = []
        shapeCheckPassed = False
        shiftTrials = []
        shiftCheckPassed = False

        if(colorReps!=None):
            for i in range(colorReps):
                colorTrials.extend(self.colorDataTemplate)

            while not(colorCheckPassed):
                colorTrials = self.getTrialsFromTrialHandler(data.TrialHandler(colorTrials,1))
                colorCheckPassed = self.colorAndShapeCheck(colorTrials)

        if(shapeReps!=None):
            for i in range(shapeReps):
                shapeTrials.extend(self.shapeDataTemplate)

            while not(shapeCheckPassed):
                shapeTrials = self.getTrialsFromTrialHandler(data.TrialHandler(shapeTrials,1))
                shapeCheckPassed = self.colorAndShapeCheck(colorTrials)

        if(shiftReps!=None):
            for i in range(shiftReps):
                shiftTrials.extend(self.shiftDataTemplate)

            while(not shiftCheckPassed):
                shiftTrials = self.getTrialsFromTrialHandler(data.TrialHandler(shiftTrials,1))
                shiftCheckPassed = self.shiftCheck(shiftTrials)

        #combine trials into a final array to pass to handler for sequential execution...
        finalTrials = []
        if(colorFirst):
            finalTrials.extend(colorTrials)
            finalTrials.extend(shapeTrials)
        else:
            finalTrials.extend(shapeTrials)
            finalTrials.extend(colorTrials)
        if(shiftReps!=None):
            finalTrials.extend(shiftTrials)

        self.trialHandler = data.TrialHandler(finalTrials,1,method="sequential")





    def colorAndShapeCheck(self,trials):
        """utility method to validate the random ordering of color and shape trials"""

        #check to make sure the correct response is not the same direction more than 4 times in a row.
        corrRespCount = 1
        lastCorrResp = None

        for trial in trials:
            if(lastCorrResp!=None):
                if(lastCorrResp != trial['corr_resp']):
                    corrRespCount = 1
                else:
                    corrRespCount +=1

            if(corrRespCount > 4):
                return False;
            lastCorrResp = trial['corr_resp']

        return True


    def shiftCheck(self,trials):
        """utility method to check that the number of cue shifted trials is between 40% and 60% and there are no runs of cues > 4"""
        shiftCount = 0.000
        lastCue = None
        cueCount = 1
        for trial in trials:
            if(lastCue!=None):
                if(lastCue != trial['cue']):
                    shiftCount +=1.000
                    cueCount = 1
                else:
                    cueCount +=1
            if(cueCount > 4):
                return False;
            lastCue = trial['cue']
        shiftPercentage = (shiftCount / (len(trials) * 1.000))
        return (shiftPercentage >= .450 and shiftPercentage <= .550)



    def doBeforeTrialBlock(self):
        """Sets up common stimuli for the block."""


        tri_red = lavatask.base.Resource('tri_red.bmp',self.task)
        rect_blue = lavatask.base.Resource('rect_blue.bmp',self.task)
        rect_red = lavatask.base.Resource('rect_red.bmp',self.task)
        tri_blue = lavatask.base.Resource('tri_blue.bmp',self.task)
        shape_cue = lavatask.base.UnicodeResource('shape_cue.txt',self.task)
        color_cue = lavatask.base.UnicodeResource('color_cue.txt',self.task)
        feedback_correct = lavatask.base.UnicodeResource('feedback_correct.txt',self.task)
        feedback_incorrect = lavatask.base.UnicodeResource('feedback_incorrect.txt',self.task)
        feedback_noresponse = lavatask.base.UnicodeResource('feedback_no_response.txt',self.task)


        self.stimuli['comp_left'] = visual.ImageStim(win=self.task.window, image=tri_red.getResourceLocation(),size=3.5, pos=[-7,-7], units='cm')
        self.stimuli['comp_right'] = visual.ImageStim(win=self.task.window, image=rect_blue.getResourceLocation(),size=3.5, pos=[7,-7], units='cm')
        self.stimuli['color_left'] = visual.ImageStim(win=self.task.window, image=rect_red.getResourceLocation(),size=3.5,pos=[0,0],units='cm')
        self.stimuli['color_right'] = visual.ImageStim(win=self.task.window, image=tri_blue.getResourceLocation(),size=3.5,pos=[0,0],units='cm')
        self.stimuli['shape_left'] = visual.ImageStim(win=self.task.window, image=tri_blue.getResourceLocation(),size=3.5,pos=[0,0],units='cm')
        self.stimuli['shape_right'] = visual.ImageStim(win=self.task.window, image=rect_red.getResourceLocation(),size=3.5,pos=[0,0],units='cm')

        self.stimuli['shape'] = visual.TextStim(win=self.task.window, ori=0,text=shape_cue.getText(),pos=[0,-7],\
            alignHoriz = 'center',alignVert='center',height=1, units="cm",color="white")

        self.stimuli['color'] = visual.TextStim(win=self.task.window, ori=0,text=color_cue.getText(),pos=[0,-7],\
            alignHoriz = 'center',alignVert='center',height=1, units="cm",color="white")

        self.stimuli['correct'] = visual.TextStim(win=self.task.window, ori=0,text=feedback_correct.getText(),pos=[0,0],\
            alignHoriz = 'center',alignVert='center',height=1, units="cm",color="white")
        self.stimuli['incorrect'] = visual.TextStim(win=self.task.window, ori=0,text=feedback_incorrect.getText(),pos=[0,0],\
            alignHoriz = 'center',alignVert='center',height=1, units="cm",color="white")
        self.stimuli['noresponse'] = visual.TextStim(win=self.task.window, ori=0,text=feedback_noresponse.getText(),pos=[0,0],\
            alignHoriz = 'center',alignVert='center',height=1, units="cm",color="white")


        self.stimuli['fixation'] = visual.TextStim(win=self.task.window, ori=0,text="x",pos=[0, 0],\
            alignHoriz = 'center',alignVert='center',height=.5, units="cm",color="white")


        if(self.task.ageCohort == 'Child'):
            shape_sound = lavatask.base.Resource('shape.wav',self.task)
            color_sound = lavatask.base.Resource('color.wav',self.task)
            self.stimuli['shape_sound']=sound.Sound(shape_sound.getResourceLocation())
            self.stimuli['color_sound']=sound.Sound(color_sound.getResourceLocation())


        #clear the instructions screen
        self.drawBackground(self.background)
        self.task.refreshWindow()


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
        self.currentResponse = SetShiftingResponse()
        self.currentResponse.block=self
        self.currentResponse.trialData = self.currentTrial
        self.currentResponse.trialNum=self.currentTrialNum
        self.currentResponse.responseDevice='none'
        self.currentResponse.taskTime=self.task.getTime()
        self.currentResponse.key='none'
        self.currentResponse.rt = 0
        self.lastResponse = None
        self.lastResponseTime = None
        self.lastResponseDevice = None
        #variable to track cue switching
        if(self.currentTrial['condition']=='shift'):
            if(self.lastCue==None or self.lastCue==self.currentTrial['cue']):
                self.currentResponse.shift=0
            else:
                self.currentResponse.shift=1
        else:
            self.currentResponse.shift=0

        self.lastCue = self.currentTrial['cue']
        self.resetClock()




    def doBeforeTrialResponse(self):
        """Draws stimuli for stimuli display period"""
        if(self.trialDrawStage == 0):
            self.drawBackground(self.background)
            self.stimuli['comp_left'].draw()
            self.stimuli['comp_right'].draw()
            self.trialDrawStage = 1
            self.task.refreshWindow()
        if(self.trialDrawStage == 1 and self.getTime()>=self.initialDelay):
            self.drawBackground(self.background)
            self.stimuli['comp_left'].draw()
            self.stimuli['comp_right'].draw()
            self.stimuli[self.currentTrial['cue']].draw()
            if(self.task.ageCohort == 'Child'):
                self.stimuli[self.currentTrial['cue']+'_sound'].play()
            self.trialDrawStage = 2
            self.task.refreshWindow()
        if(self.trialDrawStage == 2 and self.getTime()>=self.initialDelay+self.cueDuration):
            self.drawBackground(self.background)
            self.stimuli['comp_left'].draw()
            self.stimuli['comp_right'].draw()
            self.stimuli[self.currentTrial['cue']].draw()
            self.stimuli['fixation'].draw()
            self.trialDrawStage = 3
            self.task.refreshWindow()
        if(self.trialDrawStage == 3 and self.getTime() >= self.targetDisplayTime):
            self.drawBackground(self.background)
            self.stimuli['comp_left'].draw()
            self.stimuli['comp_right'].draw()
            self.stimuli[self.currentTrial['cue']].draw()
            self.stimuli[self.currentTrial['cue'] +"_"+ self.currentTrial['corr_resp']].draw()
            self.trialDrawStage = 4
            self.task.refreshWindow()
            self.enableResponse()


    def doAfterTrialResponse(self):
         """Records response."""

         self.currentResponse.key=self.lastResponse
         self.currentResponse.responseDevice = self.lastResponseDevice
         self.currentResponse.rt=(self.lastResponseTime-self.targetDisplayTime)
         self.currentResponse.taskTime=self.task.getTime()
         if(self.currentResponse.key == self.currentResponse.trialData['corr_resp']):
            self.currentResponse.corr=1
            self.totalCorrect += 1
         else:
            self.currentResponse.corr=0
         self.lastTrialCorrect=self.currentResponse.corr
         self.task.responses.addResponse(self.currentResponse)
         self.disableResponse()
    def doTrialTimeout(self):
         """Ends trial and determines if response was correct."""

         self.currentResponse.corr=0
         self.lastTrialCorrect = None
         self.task.responses.addResponse(self.currentResponse)
         self.disableResponse()

    def doAfterTrial(self):
        """Draws response feedback if enabled for block."""
        if(self.displayFeedback):
            feedbackTimeout = self.getTime() + self.feedbackDuration
            self.drawBackground("Black")
            if(self.lastTrialCorrect == True):
                self.stimuli['correct'].draw()
            elif(self.lastTrialCorrect == False):
                self.stimuli['incorrect'].draw()
            else:
                self.stimuli['noresponse'].draw()
            self.stimuli['comp_left'].draw()
            self.stimuli['comp_right'].draw()
            self.task.refreshWindow()
            self.wait(self.feedbackDuration)


class SetShiftingResponses(lavatask.base.TaskResponses):
    """Extends TaskResponses class to implement Set Shifting specific summary scoring.

    Summary scoring for Set Shifting is
        1) For the color, shape, and shift Conditions
            a) correct
            b) errors
            c) mean, median, stdev
        2) FOr the shift and nonshifted trials in the shift block
            a) correct
            b) errors
            c) mean, median, stdev


        3) There is also a total trials attempted score that helps identify incomplete testing sessions.)
        4) There is a shift_score and a shift_error_diff that are used for generating a composite score and scales
    """
    def __init__(self,task):
        lavatask.base.TaskResponses.__init__(self,task)

    def getSummaryStatsColumns(self):
        """Return column names for the summary statistics."""
        columns = lavatask.base.TaskResponses.getSummaryStatsColumns(self)
        for column in ['response_device','total_trials','shift_score','shift_error_diff',
                'color_corr','color_errors','color_mean','color_median','color_stdev',
                'shape_corr','shape_errors','shape_mean','shape_median','shape_stdev',
                'shift_corr','shift_errors','shift_mean','shift_median','shift_stdev',
                'shifted_corr','shifted_errors','shifted_mean','shifted_median','shifted_stdev',
                'nonshifted_corr','nonshifted_errors','nonshifted_mean','nonshifted_median','nonshifted_stdev',
        ]:
            columns.append(column)
        return columns

    def getSummaryStatsFields(self):
        """Calculate the summary stats and return the data as a dictionary."""
        fields = lavatask.base.TaskResponses.getSummaryStatsFields(self)
        response_device=None

        color = []
        shape = []
        shift = []
        shifted = []
        nonshifted = []

        colorErrors = 0
        shapeErrors = 0
        shiftErrors = 0
        shiftedErrors = 0
        nonshiftedErrors = 0
        testingTrialsAttempted=0

        #compile correct response data into groups for summary stats
        for response in self.data:
            if(response['block_name']=='testingBlock'):

                #update device type info
                if(response['response_device']!='none'):
                    if(response_device == None):
                        response_device = response['response_device']
                    elif (response_device != 'multiple' and response_device != response['response_device']): #changed <> to !=
                        response_device = 'multiple'

                #update trials attempted
                testingTrialsAttempted+=1

                #handle color block
                if(response['trial_condition']=='color'):
                    if(response['resp_corr']==0):
                        colorErrors +=1
                    else:
                        rt = response['resp_rt']
                        color.append(rt)
                elif(response['trial_condition']=='shape'):
                    if(response['resp_corr']==0):
                        shapeErrors +=1
                    else:
                        rt = response['resp_rt']
                        shape.append(rt)
                elif(response['trial_condition']=='shift'):
                    if(response['trial_shift']==1):
                        if(response['resp_corr']==0):
                            shiftErrors +=1
                            shiftedErrors+=1
                        else:
                           rt = response['resp_rt']
                           shift.append(rt)
                           shifted.append(rt)
                    else: #nonshifted
                        if(response['resp_corr']==0):
                            shiftErrors +=1
                            nonshiftedErrors+=1
                        else:
                           rt = response['resp_rt']
                           shift.append(rt)
                           nonshifted.append(rt)

        #do summary stats on each summary group and add to fields collection
        fields.update({'response_device':response_device})
        fields.update({'total_trials':testingTrialsAttempted})
        fields.update({'color_corr':self.calcCorrect(color),'color_errors':colorErrors,'color_mean':self.calcMean(color),'color_median':self.calcMedian(color),'color_stdev':self.calcStDev(color)})
        fields.update({'shape_corr':self.calcCorrect(shape),'shape_errors':shapeErrors,'shape_mean':self.calcMean(shape),'shape_median':self.calcMedian(shape),'shape_stdev':self.calcStDev(shape)})
        fields.update({'shift_corr':self.calcCorrect(shift),'shift_errors':shiftErrors,'shift_mean':self.calcMean(shift),'shift_median':self.calcMedian(shift),'shift_stdev':self.calcStDev(shift)})
        fields.update({'shifted_corr':self.calcCorrect(shifted),'shifted_errors':shiftedErrors,'shifted_mean':self.calcMean(shifted),'shifted_median':self.calcMedian(shifted),'shifted_stdev':self.calcStDev(shifted)})
        fields.update({'nonshifted_corr':self.calcCorrect(nonshifted),'nonshifted_errors':nonshiftedErrors,'nonshifted_mean':self.calcMean(nonshifted),'nonshifted_median':self.calcMedian(nonshifted),'nonshifted_stdev':self.calcStDev(nonshifted)})


        shift_score = self.calcShiftScore(fields)
        shift_error_diff = self.calcErrorDiff(fields)
        fields.update({'shift_score':shift_score,'shift_error_diff':shift_error_diff})
        return fields

    def calcShiftScore(self,fields,noCalcValue=-5):
        """Calculate the Shift score."""
        shift_corr = fields['shift_corr']
        shift_errors = fields['shift_errors']

        shift_median = fields['shift_median']

        if(fields['total_trials']!=104 or shift_corr == noCalcValue or shift_median == noCalcValue or shift_errors == noCalcValue): #changed<> before 104
            return noCalcValue;

        # the * 1.0 makes sure we get a decimal result... is there a better way to do this?
        accuracy_score = (shift_corr * 1.0 / (shift_corr + shift_errors) * 1.0) * 5.0

        if(shift_median < 0.400):
            #performance ceiling is 400 milliseconds
            shift_median = 0.400
        if(shift_median > 2.800):
            #performance floor is 2.8 seconds
            shift_median = 2.800

        shift_median_adjusted = (log10(shift_median)-log10(0.400))/(log10(2.800)-log10(0.400))
        reaction_time_score = 5 - (5 * shift_median_adjusted)
        return round(accuracy_score + reaction_time_score,3)

    def calcErrorDiff(self,fields,noCalcValue=-5):
        """Calculate difference in errors from shift condition to the color and shape conditions."""
        shift_errors = fields['shift_errors']
        color_errors = fields['color_errors']
        shape_errors = fields['shape_errors']

        if(fields['total_trials']!=104 or shift_errors == noCalcValue or color_errors == noCalcValue or shape_errors == noCalcValue):# changed <>before 104
            return noCalcValue;
        return ((shift_errors) - (color_errors + shape_errors))




class SetShiftingResponse(lavatask.base.TrialResponse):
    """Extends TrialResponse class to implement Flanker specific trial configuration in output files.

    """
    def __init__(self):
        lavatask.base.TrialResponse.__init__(self)
        self.shift=0 #variable to track cue shifted trials

    def getTrialConfigurationFields(self):
        """Returns the flanker specific trial configuration data as a dictionary."""
        return {'trial_condition':self.trialData.condition,'trial_cue':self.trialData.cue,'trial_corr_resp':self.trialData.corr_resp,'trial_shift':self.shift,}

    def getTrialConfigurationColumns(self):
        """Returns the flanker specific trial configuration column names."""
        return ['trial_condition','trial_cue','trial_corr_resp','trial_shift']


class SetShiftingInstructionBlock(lavatask.base.InstructionBlock):
    """Extends base InstructionBlock to support playing audio stimuli in response to keypress.

    """
    def __init__(self,task,name,foreground="Black",background="White",keys=['space','c','s','f'],):
        lavatask.base.InstructionBlock.__init__(self,task,name,keys,foreground,background)
        self.audio = {}

    def doBeforeBlock(self):
        lavatask.base.InstructionBlock.doBeforeBlock(self)
        shape_sound = lavatask.base.Resource('shape.wav',self.task)
        color_sound = lavatask.base.Resource('color.wav',self.task)
        self.audio['s']=sound.Sound(shape_sound.getResourceLocation())
        self.audio['c']=sound.Sound(color_sound.getResourceLocation())
        self.audio['f']=self.audio['s'] #in spanish version the shape cue is 'forma'

    def doTimeout(self):
        """Abort the task when an instruction block times out."""
        self.task.abort()

    def doBeforeResponse(self):
        """Displays instructions."""
        if(self.drawStage == 0):
            self.drawBackground(self.background)
            for stim in self.stims:
                stim.draw()
            self.instructions.draw()
            self.task.refreshWindow()
            self.captureScreenShot()
            self.drawStage = 1
            self.enableResponse()

    def doAfterResponse(self):
        """draw blank background"""

        if(self.lastResponse in self.audio.keys()):
            logging.error("Set Shifting self.audio self.lastResponse=" + self.lastResponse)
            self.audio[self.lastResponse].play()
            self.setContinue(True);
            return

        if(self.clearForegroundOnResponse == True):
            self.drawBackground(self.background)
            self.task.refreshWindow()

    def createDefaultInstructionStimuli(self):
        """Creates a default Instruction Stimuli using the text property."""
        return visual.TextStim(win=self.task.window, ori=0,text=self.text,pos=[0, 0],\
            alignHoriz = 'center',alignVert='center',font=self.task.fontName,height=self.task.fontSize,color=self.foreground,wrapWidth=50)

    def addStim(self,stim):
        self.stims.append(stim)
