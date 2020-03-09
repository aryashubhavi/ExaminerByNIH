#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Class library that provides extensions to the base LavaTask computer based task classes for the NBack task

:Classes:
    NBackTask - extends Task class to implement block configuration and control of flow for the NBack task.
    NBackBlock - extends TrialBlock class to implement NBack specific trial block functionality.
    NBackResponses - extends TaskResponses class to implement NBack specific summary scoring.
    NBackResponse - extends TrialResponse class to implement NBack specific trial configuration in output files.

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
from scipy.stats import norm




class NBackTask(lavatask.base.Task):
    """Extends Task class to implement block configuration and control of flow for the NBack task.

    """
    def __init__(self,configuration,environment=None,sessionConfig=None):
        lavatask.base.Task.__init__(self,configuration,environment,sessionConfig)
        self.name='NBack'
        self.version='3.2.0.2'
        self.versionDate='04/04/2012'
        self.responses = NBackResponses(self)
        self.resourcePath = os.path.join(self.resourcePath,'examiner','nback')
        self.skipTwoBack = False #variable used to skip the execution of the 2 back (either by protocol or because 1-Back was failed)
    def doBeforeTask(self):
        """Configure task blocks """
        if(self.ageCohort=="Child"):
            self.skipTwoBack=True
        self.setupTask()

        #log error and quit if no configuration found for the ageCohort and language settings
        if(self.getBlockByName('nb1TestingBlock')==None):
            logging.error("NBack task not configured. Form = " + self.form + ", Language=" + self.language + ".")
            core.quit();

    def doAfterBlock(self,block):
        """Perform task specific control of flow logic.

        If the subject gets 7 out of 10 trials correct in a practice trial then skip ahead to
        the real testing trial.  If the subject fails to get 7 out of 10 in 3 practice blocks then
        end the task.
        """
        if(block.name=="nb1PracticeBlock" ):
            #check whether we can skip the remaining practice blocks
            if(block.totalCorrect >= 7):
                self.setNextBlock("nb1TestingInstruct")
        if(block.name == "nb1Practice2Block"):
            #check whether we should abort the task
            if(block.totalCorrect < 7):
                self.skipTwoBack = True
                self.setNextBlock("nb1CompleteInstruct")
        if(block.name == "nb1CompleteInstruct"):
            #if the two back is not to be run, then abort the remaining blocks
            if(self.skipTwoBack == True):
                self.abort()


        if(block.name == "nb1TestingBlock" and self.skipTwoBack==False):
            #skip the nb1 complete block if the 2 back is being administered
            self.setNextBlock("nb2DemoInstruct")


        if(block.name=="nb2PracticeBlock" or block.name=="nb2Practice2Block"):
            #check whether we can skip the remaining practice blocks
            if(block.totalCorrect >= 7):
                self.setNextBlock("nb2TestingInstruct")
        if(block.name == "nb2Practice3Block"):
            #check whether we should abort the task
            if(block.totalCorrect < 7):
                self.setNextBlock("nb2CompleteInstruct")

    def setupTask(self):
        """Configure task blocks for stimuli and instructions for all languages."""

        nb1DemoInstruct = lavatask.base.InstructionBlock(self,"nb1DemoInstruct",['space',],"White","Black")
        nb1DemoInstruct.text = lavatask.base.UnicodeResource("demo.txt",self).getCenteredText()
        self.addBlock(nb1DemoInstruct)

        nb1DemoInstruct2 = lavatask.base.InstructionBlock(self,"nb1DemoInstruct2",['space',],"White","Black")
        nb1DemoInstruct2.text = lavatask.base.UnicodeResource("demo2.txt",self).getCenteredText()
        self.addBlock(nb1DemoInstruct2)

        nb1Demo = OneBackDemoBlock(self,'nb1DemoBlock')
        nb1Demo.initializeTrialData(self.form,"demo")
        self.addBlock(nb1Demo)

        nb1PracticeInstruct = lavatask.base.InstructionBlock(self,"nb1PracticeInstruct",['space',],"White","Black")
        nb1PracticeInstruct.text = lavatask.base.UnicodeResource("practice.txt",self).getCenteredText()
        self.addBlock(nb1PracticeInstruct)

        nb1PracticeBlock = OneBackBlock(self,'nb1PracticeBlock')
        nb1PracticeBlock.initializeTrialData(self.form,"practice1")
        self.addBlock(nb1PracticeBlock)

        nb1Practice2Instruct = lavatask.base.InstructionBlock(self,"nb1Practice2Instruct",['space',],"White","Black")
        nb1Practice2Instruct.text = lavatask.base.UnicodeResource("practice.txt",self).getCenteredText()
        self.addBlock(nb1Practice2Instruct)

        nb1Practice2Block = OneBackBlock(self,'nb1Practice2Block')
        nb1Practice2Block.initializeTrialData(self.form,"practice2")
        self.addBlock(nb1Practice2Block)


        nb1TestingInstruct = lavatask.base.InstructionBlock(self,"nb1TestingInstruct",['space',],"White","Black")
        nb1TestingInstruct.text =  lavatask.base.UnicodeResource("testing.txt",self).getCenteredText()
        self.addBlock(nb1TestingInstruct)

        nb1TestingBlock = OneBackBlock(self,'nb1TestingBlock')
        nb1TestingBlock.initializeTrialData(self.form,"testing")
        self.addBlock(nb1TestingBlock)

        nb1CompleteInstruct = lavatask.base.InstructionBlock(self,"nb1CompleteInstruct",['space',],"White","Black")
        nb1CompleteInstruct.text = lavatask.base.UnicodeResource("complete.txt",self).getCenteredText()
        self.addBlock(nb1CompleteInstruct)

        if(self.skipTwoBack == True):
            return

        nb2DemoInstruct = lavatask.base.InstructionBlock(self,"nb2DemoInstruct",['space',],"White","Black")
        nb2DemoInstruct.text = lavatask.base.UnicodeResource("2demo.txt",self).getCenteredText()
        self.addBlock(nb2DemoInstruct)

        nb2DemoInstruct2 = lavatask.base.InstructionBlock(self,"nb2DemoInstruct2",['space',],"White","Black")
        nb2DemoInstruct2.text = lavatask.base.UnicodeResource("2demo2.txt",self).getCenteredText()
        self.addBlock(nb2DemoInstruct2)

        nb2Demo = TwoBackDemoBlock(self,'nb2DemoBlock')
        nb2Demo.initializeTrialData(self.form,"demo")
        self.addBlock(nb2Demo)

        nb2PracticeInstruct = lavatask.base.InstructionBlock(self,"nb2PracticeInstruct",['space',],"White","Black")
        nb2PracticeInstruct.text = lavatask.base.UnicodeResource("2practice.txt",self).getCenteredText()
        self.addBlock(nb2PracticeInstruct)

        nb2PracticeBlock = TwoBackBlock(self,'nb2PracticeBlock')
        nb2PracticeBlock.initializeTrialData(self.form,"practice1")
        self.addBlock(nb2PracticeBlock)

        nb2Practice2Instruct = lavatask.base.InstructionBlock(self,"nb2Practice2Instruct",['space',],"White","Black")
        nb2Practice2Instruct.text = lavatask.base.UnicodeResource("2additional_practice.txt",self).getCenteredText()
        self.addBlock(nb2Practice2Instruct)

        nb2Practice2Block = TwoBackBlock(self,'nb2Practice2Block')
        nb2Practice2Block.initializeTrialData(self.form,"practice2")
        self.addBlock(nb2Practice2Block)

        nb2Practice3Instruct = lavatask.base.InstructionBlock(self,"nb2Practice3Instruct",['space',],"White","Black")
        nb2Practice3Instruct.text = lavatask.base.UnicodeResource("2additional_practice.txt",self).getCenteredText()
        self.addBlock(nb2Practice3Instruct)

        nb2Practice3Block = TwoBackBlock(self,'nb2Practice3Block')
        nb2Practice3Block.initializeTrialData(self.form,"practice3")
        self.addBlock(nb2Practice3Block)

        nb2TestingInstruct = lavatask.base.InstructionBlock(self,"nb2TestingInstruct",['space',],"White","Black")
        nb2TestingInstruct.text =  lavatask.base.UnicodeResource("2testing.txt",self).getCenteredText()
        self.addBlock(nb2TestingInstruct)

        nb2TestingBlock = TwoBackBlock(self,'nb2TestingBlock')
        nb2TestingBlock.initializeTrialData(self.form,"testing")
        self.addBlock(nb2TestingBlock)

        nb2CompleteInstruct = lavatask.base.InstructionBlock(self,"nb2CompleteInstruct",['space',],"White","Black")
        nb2CompleteInstruct.text = lavatask.base.UnicodeResource("2complete.txt",self).getCenteredText()
        self.addBlock(nb2CompleteInstruct)





class OneBackBlock(lavatask.base.TrialResponseBlock):
    """Extends TrialBlock class to implement One Back specific trial block functionality.

    The One Back block runs a set number of trials with the following structure
        Initial Trial:
        1) target: Displayed for 1 second
        2) 500 ms delay
        3) Fixation number: displays fixation number for 1 second
        4) 500 ms Delay with Yes/No Stimuli (once displayed on a block, they stay on)
        Remaining Trials
        1) Probe: displayed for 1 second
        2) User input: wait for user input (may be provided as soon as the probe is displayed)
        3) 500 ms delay
        4) Fixation number: displays fixation number for 1 second
        5) 500 ms Delay with Yes/No Stimuli (once displayed on a block, they stay on)

    """
    def __init__(self,task,name,keys=["left","right"],trialData=None):
        lavatask.base.TrialResponseBlock.__init__(self,task,name,keys,trialData)
        self.standardDelay = 0.500 # default delay period between phases of trials / trials
        self.beforeBlockDelay = 2.0
        self.beforeTrialDelay = 0.500 #default time between each trial
        self.totalCorrect=0 #count of the number of correct responses
        self.fixationDisplayDuration = 1.0 # The amount of time to display the fixation stimuli
        self.targetDisplayDuration = 1.0 # the length of time to display the target stimuli
        self.displayFeedbackDuration = 2.0 #length of time to display feedback
        self.responseTrial = False # flag indicating whether the trial requires a response to continue

        self.dataTemplates = {}
        self.dataTemplates['practice1_a']= [ \
        {'trial_number':0,'location':3,'similarity':None,'fixation_number':2,'corr_resp':'none'},
        {'trial_number':1,'location':6,'similarity':3,'fixation_number':5,'corr_resp':'right'},
        {'trial_number':2,'location':6,'similarity':0,'fixation_number':9,'corr_resp':'left'},
        {'trial_number':3,'location':4,'similarity':2,'fixation_number':1,'corr_resp':'right'},
        {'trial_number':4,'location':1,'similarity':3,'fixation_number':6,'corr_resp':'right'},
        {'trial_number':5,'location':1,'similarity':0,'fixation_number':7,'corr_resp':'left'},
        {'trial_number':6,'location':12,'similarity':4,'fixation_number':3,'corr_resp':'right'},
        {'trial_number':7,'location':10,'similarity':2,'fixation_number':8,'corr_resp':'right'},
        {'trial_number':8,'location':10,'similarity':0,'fixation_number':2,'corr_resp':'left'},
        {'trial_number':9,'location':10,'similarity':0,'fixation_number':4,'corr_resp':'left'},
        {'trial_number':10,'location':6,'similarity':4,'fixation_number':None,'corr_resp':'right'},
        ]
        self.dataTemplates['practice1_b'] = self.dataTemplates['practice1_a']
        self.dataTemplates['practice1_c'] = self.dataTemplates['practice1_a']


        self.dataTemplates['practice2_a']= [ \
        {'trial_number':0,'location':10,'similarity':None,'fixation_number':8,'corr_resp':'none'},
        {'trial_number':1,'location':10,'similarity':0,'fixation_number':6,'corr_resp':'left'},
        {'trial_number':2,'location':13,'similarity':3,'fixation_number':1,'corr_resp':'right'},
        {'trial_number':3,'location':2,'similarity':4,'fixation_number':8,'corr_resp':'right'},
        {'trial_number':4,'location':2,'similarity':0,'fixation_number':3,'corr_resp':'left'},
        {'trial_number':5,'location':5,'similarity':3,'fixation_number':2,'corr_resp':'right'},
        {'trial_number':6,'location':7,'similarity':2,'fixation_number':9,'corr_resp':'right'},
        {'trial_number':7,'location':7,'similarity':0,'fixation_number':7,'corr_resp':'left'},
        {'trial_number':8,'location':4,'similarity':3,'fixation_number':5,'corr_resp':'right'},
        {'trial_number':9,'location':0,'similarity':4,'fixation_number':1,'corr_resp':'right'},
        {'trial_number':10,'location':0,'similarity':0,'fixation_number':None,'corr_resp':'left'},
        ]

        self.dataTemplates['practice2_b'] = self.dataTemplates['practice2_a']
        self.dataTemplates['practice2_c'] = self.dataTemplates['practice2_a']


        self.dataTemplates['testing_a']= [ \
        {'trial_number':0,'location':11,'similarity':None,'fixation_number':7,'corr_resp':'none','visual_hemifield':None},
        {'trial_number':1,'location':11,'similarity':0,'fixation_number':6,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':2,'location':7,'similarity':4,'fixation_number':1,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':3,'location':8,'similarity':1,'fixation_number':8,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':4,'location':12,'similarity':4,'fixation_number':5,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':5,'location':12,'similarity':0,'fixation_number':2,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':6,'location':0,'similarity':3,'fixation_number':7,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':7,'location':0,'similarity':0,'fixation_number':3,'corr_resp':'left','visual_hemifield':0},
        {'trial_number':8,'location':1,'similarity':1,'fixation_number':1,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':9,'location':3,'similarity':2,'fixation_number':4,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':10,'location':2,'similarity':1,'fixation_number':7,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':11,'location':6,'similarity':4,'fixation_number':2,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':12,'location':6,'similarity':0,'fixation_number':9,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':13,'location':6,'similarity':0,'fixation_number':5,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':14,'location':10,'similarity':4,'fixation_number':8,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':15,'location':8,'similarity':2,'fixation_number':2,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':16,'location':8,'similarity':0,'fixation_number':6,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':17,'location':6,'similarity':2,'fixation_number':7,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':18,'location':9,'similarity':3,'fixation_number':9,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':19,'location':9,'similarity':0,'fixation_number':1,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':20,'location':5,'similarity':4,'fixation_number':6,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':21,'location':4,'similarity':1,'fixation_number':8,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':22,'location':4,'similarity':0,'fixation_number':2,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':23,'location':2,'similarity':2,'fixation_number':7,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':24,'location':14,'similarity':3,'fixation_number':1,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':25,'location':11,'similarity':3,'fixation_number':9,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':26,'location':13,'similarity':2,'fixation_number':5,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':27,'location':13,'similarity':0,'fixation_number':7,'corr_resp':'left','visual_hemifield':0},
        {'trial_number':28,'location':14,'similarity':1,'fixation_number':2,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':29,'location':2,'similarity':3,'fixation_number':4,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':30,'location':2,'similarity':0,'fixation_number':None,'corr_resp':'left','visual_hemifield':1},
        ]

        self.dataTemplates['testing_b']= [ \
        {'trial_number':0,'location':14,'similarity':None,'fixation_number':7,'corr_resp':'none','visual_hemifield':None},
        {'trial_number':1,'location':14,'similarity':0,'fixation_number':4,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':2,'location':1,'similarity':2,'fixation_number':5,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':3,'location':1,'similarity':0,'fixation_number':1,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':4,'location':12,'similarity':4,'fixation_number':3,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':5,'location':0,'similarity':3,'fixation_number':8,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':6,'location':3,'similarity':3,'fixation_number':6,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':7,'location':3,'similarity':0,'fixation_number':9,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':8,'location':4,'similarity':1,'fixation_number':8,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':9,'location':5,'similarity':1,'fixation_number':7,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':10,'location':7,'similarity':2,'fixation_number':1,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':11,'location':7,'similarity':0,'fixation_number':3,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':12,'location':11,'similarity':4,'fixation_number':5,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':13,'location':12,'similarity':1,'fixation_number':2,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':14,'location':14,'similarity':2,'fixation_number':4,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':15,'location':13,'similarity':1,'fixation_number':7,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':16,'location':2,'similarity':4,'fixation_number':5,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':17,'location':2,'similarity':0,'fixation_number':4,'corr_resp':'left','visual_hemifield':0},
        {'trial_number':18,'location':2,'similarity':0,'fixation_number':9,'corr_resp':'left','visual_hemifield':0},
        {'trial_number':19,'location':13,'similarity':4,'fixation_number':8,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':20,'location':10,'similarity':3,'fixation_number':5,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':21,'location':10,'similarity':0,'fixation_number':7,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':22,'location':9,'similarity':1,'fixation_number':1,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':23,'location':9,'similarity':0,'fixation_number':7,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':24,'location':11,'similarity':2,'fixation_number':4,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':25,'location':0,'similarity':4,'fixation_number':6,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':26,'location':2,'similarity':2,'fixation_number':3,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':27,'location':5,'similarity':3,'fixation_number':5,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':28,'location':5,'similarity':0,'fixation_number':7,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':29,'location':8,'similarity':3,'fixation_number':8,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':30,'location':8,'similarity':0,'fixation_number':None,'corr_resp':'left','visual_hemifield':2},
        ]

        self.dataTemplates['testing_c']= [ \
        {'trial_number':0,'location':10,'similarity':None,'fixation_number':7,'corr_resp':'none','visual_hemifield':None},
        {'trial_number':1,'location':10,'similarity':0,'fixation_number':5,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':2,'location':12,'similarity':2,'fixation_number':1,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':3,'location':14,'similarity':2,'fixation_number':7,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':4,'location':14,'similarity':0,'fixation_number':2,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':5,'location':13,'similarity':1,'fixation_number':8,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':6,'location':2,'similarity':4,'fixation_number':9,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':7,'location':13,'similarity':4,'fixation_number':1,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':8,'location':14,'similarity':1,'fixation_number':5,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':9,'location':3,'similarity':4,'fixation_number':8,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':10,'location':6,'similarity':3,'fixation_number':3,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':11,'location':6,'similarity':0,'fixation_number':6,'corr_resp':'left','visual_hemifield':0},
        {'trial_number':12,'location':7,'similarity':1,'fixation_number':4,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':13,'location':7,'similarity':0,'fixation_number':1,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':14,'location':7,'similarity':0,'fixation_number':8,'corr_resp':'left','visual_hemifield':0},
        {'trial_number':15,'location':9,'similarity':2,'fixation_number':6,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':16,'location':8,'similarity':1,'fixation_number':5,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':17,'location':12,'similarity':4,'fixation_number':7,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':18,'location':12,'similarity':0,'fixation_number':3,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':19,'location':8,'similarity':4,'fixation_number':2,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':20,'location':5,'similarity':3,'fixation_number':4,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':21,'location':5,'similarity':0,'fixation_number':9,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':22,'location':4,'similarity':1,'fixation_number':8,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':23,'location':4,'similarity':0,'fixation_number':6,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':24,'location':1,'similarity':3,'fixation_number':5,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':25,'location':1,'similarity':0,'fixation_number':7,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':26,'location':3,'similarity':2,'fixation_number':8,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':27,'location':6,'similarity':3,'fixation_number':5,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':28,'location':9,'similarity':3,'fixation_number':1,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':29,'location':11,'similarity':2,'fixation_number':9,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':30,'location':11,'similarity':0,'fixation_number':None,'corr_resp':'left','visual_hemifield':2},
        ]

    def initializeTrialData(self,form,setName):
        """Configures the trialData handler using data template for the form and setName

        :parameters:
            form - the alternate form of the task.
            setName - the set name of the data template (e.g. 'practice1','testing')
        """
        if(form==None):
            form = 'a'
        if(setName==None):
            setName = 'testing'

        dataTemplate = self.dataTemplates[setName + '_' + form.lower()]
        if(dataTemplate != None):
            self.trialHandler = data.TrialHandler(dataTemplate,1,method="sequential")
        else:
            logging.error("Error configuring one back trial block for Form = " + form + " and Set=" + setName + ".")
            core.quit();

    def doBeforeTrialBlock(self):
        """Sets up common stimuli for the block."""
        self.target=visual.ImageStim(win=self.task.window, image=lavatask.base.Resource('whitesquare.bmp',self.task).getResourceLocation(),size=2.5,units='cm')
        self.fixation=visual.TextStim(win=self.task.window, ori=0,text="1",pos=[0,0], height=1, color=[1,1,-1],alignHoriz = 'center',alignVert='center', wrapWidth=26)

        self.yesStimuli=visual.TextStim(win=self.task.window, ori=0,text=lavatask.base.UnicodeResource("yes_prompt.txt",self.task).getText(),pos=[-10,-7.5], height=1, color=[1,1,-1], units='cm')
        self.noStimuli=visual.TextStim(win=self.task.window, ori=0,text=lavatask.base.UnicodeResource("no_prompt.txt",self.task).getText(),pos=[11,-7.5], height=1, color=[1,1,-1], units='cm')




    def doBeforeTrial(self):
        """Configures the next trial or ends block if no more trials."""
        try:
            # get next trial data
            self.currentTrial = self.trialHandler.next()
        except StopIteration:  #no more trials
            self.setContinueTrial(False)
            self.setContinue(False)
            return

        if(self.currentTrial.corr_resp == 'none'):
            #trials without responses need to timeout  ( in this case just the initial target)
            self.trialTimeout=self.targetDisplayDuration
            self.responseTrial=False
        else:
            self.trialTimeout=None
            self.responseTrial=True


        #reset the trial "draw stage" variable
        self.trialDrawStage = 0

        #setup the target stimuli location
        self.setTargetPosition(self.currentTrial.location)

        #setup the fixation number stimuli
        if(self.currentTrial.fixation_number != None):
            self.fixation.setText(str(self.currentTrial.fixation_number))


        self.lastResponse = None
        self.lastResponseTime = None
        self.lastResponseDevice = None
        self.lastTrialCorrect = None
        self.resetClock()

        #turn off response checking (until prompt is displayed)
        self.disableResponse()

    def setTargetPosition(self,location):
        """Set the location of the target stimuli on the screen"""
        if(location == 0):self.target.setPos([0,7.2])
        elif(location == 1):self.target.setPos([3.4,6.5])
        elif(location == 2):self.target.setPos([6.2,4.8])
        elif(location == 3):self.target.setPos([8.3,2.2])
        elif(location == 4):self.target.setPos([8.7,-0.8])
        elif(location == 5):self.target.setPos([7.5,-3.6])
        elif(location == 6):self.target.setPos([4.9,-6.0])
        elif(location == 7):self.target.setPos([1.7,-7.0])
        elif(location == 8):self.target.setPos([-1.7,-7.0])
        elif(location == 9):self.target.setPos([-4.9,-6.0])
        elif(location == 10):self.target.setPos([-7.5,-3.6])
        elif(location == 11):self.target.setPos([-8.7,-0.8])
        elif(location == 12):self.target.setPos([-8.3,2.2])
        elif(location == 13):self.target.setPos([-6.2,4.8])
        elif(location == 14):self.target.setPos([-3.4,6.5])



    def doTrialTimeout(self):
        """Trials without responses timeout"""
        response = NBackResponse()
        response.block=self
        response.trialData = self.currentTrial
        response.key='none'
        response.responseDevice = 'none'
        response.rt=0
        response.taskTime=self.task.getTime()
        response.corr=0
        self.lastTrialCorrect=response.corr
        self.task.responses.addResponse(response)



    def debugDrawTargets(self):
        """Utility function to draw all target positions for layout / spacing"""
        self.drawBackground("Black")
        for i in range(15):
           self.setTargetPosition(i)
           self.target.draw()
        self.yesStimuli.draw()
        self.noStimuli.draw()
        self.task.refreshWindow()
        self.wait(2)

    def doBeforeTrialResponse(self):

       # self.debugDrawTargets()
        if(self.trialDrawStage == 0):
                self.drawBackground("Black")
                self.target.draw()
                if(self.responseTrial == True):
                    self.enableResponse()
                    self.yesStimuli.draw()
                    self.noStimuli.draw()
                self.trialDrawStage = 1
                self.task.refreshWindow()

        elif(self.trialDrawStage == 1 and self.getTime()>= self.targetDisplayDuration):
                self.drawBackground("Black")
                if(self.responseTrial == True):
                    self.yesStimuli.draw()
                    self.noStimuli.draw()
                self.trialDrawStage = 2
                self.task.refreshWindow()

    def doAfterTrialResponse(self):
         """Checks correctness of response and records response data."""
         response = NBackResponse()
         response.block=self
         response.trialData = self.currentTrial
         response.key=self.lastResponse
         response.responseDevice = self.lastResponseDevice
         response.rt=(self.lastResponseTime)
         response.taskTime=self.task.getTime()
         if(response.key == response.trialData.corr_resp):
            response.corr=1
            self.totalCorrect += 1
         else:
            response.corr=0
         self.lastTrialCorrect=response.corr
         self.task.responses.addResponse(response)


    def doAfterTrial(self):
        """Draws intertarget fixation and the response feedback if response feedback is enabled for block."""
       #First need to wait for the full target display period to complete
        while(self.getTime() < self.targetDisplayDuration):
            self.wait(.010)

        #clear target and wait 500 milliseconds
        self.drawBackground("Black")
        if(self.responseTrial == True):
            self.yesStimuli.draw()
            self.noStimuli.draw()
        self.task.refreshWindow()
        self.wait(self.standardDelay)

        # display fixation number
        if(self.currentTrial.fixation_number != None):
            self.drawBackground("Black")
            self.fixation.draw()
            if(self.responseTrial == True):
                self.yesStimuli.draw()
                self.noStimuli.draw()
            self.task.refreshWindow()
            self.wait(self.fixationDisplayDuration)

            #now clear fixation number
            self.drawBackground("Black")
            if(self.responseTrial == True):
                self.yesStimuli.draw()
                self.noStimuli.draw()
            self.task.refreshWindow()




class OneBackDemoBlock(OneBackBlock):
    """Extends OneBackBlock class to implement Demo block specific trial functionality.

    The One Back Demoblock runs a set number of trials with the following structure
        Initial Trial:
        1) target: Displayed for 5 seconds with instructions
        2) 1 sec delay
        3) Fixation number: displays fixation number for 4 seconds (w/ instructions on first 3 response trials)
        4) 1 sec Delay with Yes/No Stimuli (once displayed on a block, they stay on)
        Remaining Trials
        1) Probe displayed with yes/no stimuli and instructions until they respond
        2) User input: wait for user input (may be provided as soon as the probe is displayed)
        3) 500 ms delay
        4) Feedback displayed for 2 seconds
        5) 500 ms delay
        4) Fixation number: displays fixation number for 4 seconds (w / instructions on first 3 response trials)
        5) 1 sec Delay with Yes/No Stimuli (once displayed on a block, they stay on)

    """
    def __init__(self,task,name,keys=["left","right"],trialData=None):
        OneBackBlock.__init__(self,task,name,keys,trialData)
        self.totalCorrect=0 #count of the number of correct responses
        self.dataTemplates = {}
        self.demoInitialTrialTimeout=5.0
        self.demoFixationDisplayDuration=4.0

        self.dataTemplates.clear()
        self.dataTemplates['demo_a'] = [ \
        {'trial_number':0,'location':0,'similarity':None,'fixation_number':3,'corr_resp':'none'},
        {'trial_number':1,'location':0,'similarity':None,'fixation_number':8,'corr_resp':'left'},
        {'trial_number':2,'location':11,'similarity':None,'fixation_number':3,'corr_resp':'right'},
        {'trial_number':3,'location':11,'similarity':None,'fixation_number':6,'corr_resp':'left'},
        {'trial_number':4,'location':13,'similarity':None,'fixation_number':2,'corr_resp':'right'},
        {'trial_number':5,'location':9,'similarity':None,'fixation_number':1,'corr_resp':'right'},
        {'trial_number':6,'location':9,'similarity':None,'fixation_number':8,'corr_resp':'left'},
        {'trial_number':7,'location':0,'similarity':None,'fixation_number':7,'corr_resp':'right'},
        {'trial_number':8,'location':14,'similarity':None,'fixation_number':5,'corr_resp':'right'},
        {'trial_number':9,'location':10,'similarity':None,'fixation_number':9,'corr_resp':'right'},
        {'trial_number':10,'location':10,'similarity':None,'fixation_number':None,'corr_resp':'left'},
        ]
        self.dataTemplates['demo_b'] = self.dataTemplates['demo_a']
        self.dataTemplates['demo_c'] = self.dataTemplates['demo_a']



    def doBeforeTrialBlock(self):
        """Sets up common stimuli for the block."""

        OneBackBlock.doBeforeTrialBlock(self)
        self.demoProbePrompt = visual.TextStim(win=self.task.window, ori=0,text=lavatask.base.UnicodeResource("demo_probe_prompt.txt",self.task).getCenteredText(),pos=[0,0], height=.8,color=[-1,1,1],wrapWidth=50)
        self.demoTargetPrompt = visual.TextStim(win=self.task.window, ori=0,text=lavatask.base.UnicodeResource("demo_target_prompt.txt",self.task).getCenteredText(),pos=[0, 0], height=.8, color=[-1,1,1],wrapWidth=50)
        self.demoFixationPrompt = visual.TextStim(win=self.task.window, ori=0,text=lavatask.base.UnicodeResource("demo_fixation_prompt.txt",self.task).getCenteredText(),pos=[0, -4], height=.8, color=[-1,1,1],wrapWidth=50)
        self.demoProbeYesNoPrompt = visual.TextStim(win=self.task.window, ori=0,text=lavatask.base.UnicodeResource("demo_yesno_prompt.txt",self.task).getCenteredText(),pos=[0,0], height=.8,color=[-1,1,1],wrapWidth=50)
        self.correctStimuli=visual.TextStim(win=self.task.window, ori=0,text=lavatask.base.UnicodeResource("feedback_correct.txt",self.task).getText(),pos=[0, 0], height=.8, color=[1,1,-1],wrapWidth=50)
        self.incorrectStimuli=visual.TextStim(win=self.task.window, ori=0,text=lavatask.base.UnicodeResource("feedback_incorrect.txt",self.task).getText(),pos=[0, 0], height=.8, color=[1,-1,-1], wrapWidth=50)




    def doBeforeTrial(self):
        """Configures the next trial or ends block if no more trials."""
        OneBackBlock.doBeforeTrial(self)

        #demo timeout is longer than standard timeout
        if(self.currentTrial.corr_resp == 'none'):
            self.trialTimeout=self.demoInitialTrialTimeout

    def doBeforeTrialResponse(self):

        if(self.trialDrawStage == 0):
            self.drawBackground("Black")
            self.target.draw()

            if(self.currentTrial.trial_number==0):
                self.demoTargetPrompt.draw()
            elif(self.currentTrial.trial_number <= 3):
                self.demoProbeYesNoPrompt.draw()
            else:
                self.demoProbePrompt.draw()
            if(self.responseTrial == True):
                self.enableResponse()
                self.yesStimuli.draw()
                self.noStimuli.draw()

            self.trialDrawStage = 1
            self.task.refreshWindow()



    def doAfterTrial(self):
        """Draws intertarget fixation and the response feedback if response feedback is enabled for block."""
       #First need to wait for the full target display period to complete
        while(self.getTime() < self.targetDisplayDuration):
            self.wait(.010)


        #clear target and wait 500 milliseconds
        self.drawBackground("Black")
        if(self.responseTrial == True):
            self.yesStimuli.draw()
            self.noStimuli.draw()
        self.task.refreshWindow()
        self.wait(self.standardDelay)

        #display feedback if this is a response trial
        if(self.responseTrial==True):
            self.drawBackground("Black")
            if(self.lastTrialCorrect == True):
                self.correctStimuli.draw()
            elif(self.lastTrialCorrect == False):
                self.incorrectStimuli.draw()

            if(self.responseTrial == True):
                self.yesStimuli.draw()
                self.noStimuli.draw()

            self.task.refreshWindow()
            self.wait(self.displayFeedbackDuration)

            #clear feedback and wait 500 milliseconds
            self.drawBackground("Black")
            if(self.responseTrial == True):
                self.yesStimuli.draw()
                self.noStimuli.draw()
            self.task.refreshWindow()
            self.wait(self.standardDelay)

        # display fixation number
        if(self.currentTrial.fixation_number != None):
            self.drawBackground("Black")
            self.fixation.draw()
            if(self.responseTrial == True):
                self.yesStimuli.draw()
                self.noStimuli.draw()
            if(self.currentTrial.trial_number <= 3):
                self.demoFixationPrompt.draw()
            self.task.refreshWindow()
            self.wait(self.demoFixationDisplayDuration)

            #now clear fixation number
            self.drawBackground("Black")
            if(self.responseTrial == True):
                self.yesStimuli.draw()
                self.noStimuli.draw()
            self.task.refreshWindow()



class TwoBackBlock(lavatask.base.TrialResponseBlock):
    """Extends TrialBlock class to implement Two Back specific trial block functionality.

    The Two Back block runs a set number of trials with the following structure
        There are two initial trials for which responses are not collected.  The remaining trials
        require a response to continue.

        Non response trials
        1) target: Displayed for 1 second
        2) 1 sec delay

        Response Trials
        1) Probe: displayed for 1 at least second
        2) User input: wait for user input (may be provided as soon as the probe is displayed)
        3) 500 ms delay after the probe display is finished or the response is provided (whichever is greater)
        note) Yes/No Stimuli: once displayed on a block, they stay on

    """
    def __init__(self,task,name,keys=["left","right"],trialData=None):
        lavatask.base.TrialResponseBlock.__init__(self,task,name,keys,trialData)
        self.standardDelay = 0.500 # default delay period between phases of trials / trials
        self.beforeBlockDelay = 2.0
        self.beforeTrialDelay = 0.500 #default time between each trial
        self.totalCorrect=0 #count of the number of correct responses
        self.targetDisplayDuration = 1.0 # the length of time to display the target stimuli
        self.nonResponseTrialTimeout = 2.0 # the length of time until a non-response trial times out
        self.displayFeedbackDuration = 2.0 #length of time to display feedback
        self.dataTemplates = {}


        self.dataTemplates['practice1_a']= [ \
        {'trial_number':0,'location':3,'similarity':None,'corr_resp':'none'},
        {'trial_number':1,'location':7,'similarity':None,'corr_resp':'none'},
        {'trial_number':2,'location':3,'similarity':0,'corr_resp':'left'},
        {'trial_number':3,'location':11,'similarity':4,'corr_resp':'right'},
        {'trial_number':4,'location':6,'similarity':3,'corr_resp':'right'},
        {'trial_number':5,'location':11,'similarity':0,'corr_resp':'left'},
        {'trial_number':6,'location':4,'similarity':2,'corr_resp':'right'},
        {'trial_number':7,'location':14,'similarity':3,'corr_resp':'right'},
        {'trial_number':8,'location':4,'similarity':0,'corr_resp':'left'},
        {'trial_number':9,'location':1,'similarity':2,'corr_resp':'right'},
        {'trial_number':10,'location':8,'similarity':4,'corr_resp':'right'},
        {'trial_number':11,'location':1,'similarity':0,'corr_resp':'left'},
        ]
        self.dataTemplates['practice1_b'] = self.dataTemplates['practice1_a']
        self.dataTemplates['practice1_c'] = self.dataTemplates['practice1_a']

        self.dataTemplates['practice2_a']= [ \
        {'trial_number':0,'location':10,'similarity':None,'corr_resp':'none'},
        {'trial_number':1,'location':6,'similarity':None,'corr_resp':'none'},
        {'trial_number':2,'location':10,'similarity':0,'corr_resp':'left'},
        {'trial_number':3,'location':2,'similarity':4,'corr_resp':'right'},
        {'trial_number':4,'location':12,'similarity':2,'corr_resp':'right'},
        {'trial_number':5,'location':2,'similarity':0,'corr_resp':'left'},
        {'trial_number':6,'location':8,'similarity':4,'corr_resp':'right'},
        {'trial_number':7,'location':5,'similarity':3,'corr_resp':'right'},
        {'trial_number':8,'location':8,'similarity':0,'corr_resp':'left'},
        {'trial_number':9,'location':5,'similarity':0,'corr_resp':'left'},
        {'trial_number':10,'location':11,'similarity':3,'corr_resp':'right'},
        {'trial_number':11,'location':3,'similarity':2,'corr_resp':'right'},
        ]
        self.dataTemplates['practice2_b'] = self.dataTemplates['practice2_a']
        self.dataTemplates['practice2_c'] = self.dataTemplates['practice2_a']

        self.dataTemplates['practice3_a']= [ \
        {'trial_number':0,'location':0,'similarity':None,'corr_resp':'none'},
        {'trial_number':1,'location':10,'similarity':None,'corr_resp':'none'},
        {'trial_number':2,'location':4,'similarity':4,'corr_resp':'right'},
        {'trial_number':3,'location':10,'similarity':0,'corr_resp':'left'},
        {'trial_number':4,'location':4,'similarity':0,'corr_resp':'left'},
        {'trial_number':5,'location':13,'similarity':3,'corr_resp':'right'},
        {'trial_number':6,'location':4,'similarity':0,'corr_resp':'left'},
        {'trial_number':7,'location':9,'similarity':4,'corr_resp':'right'},
        {'trial_number':8,'location':6,'similarity':2,'corr_resp':'right'},
        {'trial_number':9,'location':9,'similarity':0,'corr_resp':'left'},
        {'trial_number':10,'location':3,'similarity':3,'corr_resp':'right'},
        {'trial_number':11,'location':7,'similarity':2,'corr_resp':'right'},
        ]
        self.dataTemplates['practice3_b'] = self.dataTemplates['practice3_a']
        self.dataTemplates['practice3_c'] = self.dataTemplates['practice3_a']

        self.dataTemplates['testing_a']= [ \
        {'trial_number':0,'location':3,'similarity':None,'interference':None,'corr_resp':'none','visual_hemifield':None},
        {'trial_number':1,'location':12,'similarity':None,'interference':None,'corr_resp':'none','visual_hemifield':None},
        {'trial_number':2,'location':3,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':3,'location':9,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':4,'location':2,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':5,'location':9,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':6,'location':4,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':7,'location':10,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':8,'location':6,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':9,'location':6,'similarity':4,'interference':1,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':10,'location':7,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':11,'location':6,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':12,'location':5,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':13,'location':10,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':14,'location':2,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':15,'location':13,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':16,'location':3,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':17,'location':1,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':18,'location':3,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':19,'location':1,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':20,'location':4,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':21,'location':1,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':22,'location':4,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':23,'location':5,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':24,'location':0,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':25,'location':5,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':26,'location':3,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':27,'location':1,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':28,'location':1,'similarity':2,'interference':1,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':29,'location':12,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':30,'location':14,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':31,'location':11,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':32,'location':14,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':33,'location':14,'similarity':3,'interference':1,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':34,'location':12,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':35,'location':0,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':36,'location':8,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':37,'location':0,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':0},
        {'trial_number':38,'location':11,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':39,'location':13,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':40,'location':11,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':41,'location':11,'similarity':2,'interference':1,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':42,'location':11,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':43,'location':8,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':44,'location':9,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':45,'location':9,'similarity':1,'interference':1,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':46,'location':7,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':47,'location':9,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':48,'location':7,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':49,'location':8,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':50,'location':3,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':51,'location':8,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':52,'location':6,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':53,'location':10,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':54,'location':6,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':55,'location':10,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':56,'location':5,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':57,'location':10,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':58,'location':5,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':59,'location':7,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':60,'location':3,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':61,'location':10,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':62,'location':7,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':63,'location':14,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':64,'location':6,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':65,'location':14,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':66,'location':2,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':67,'location':13,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':68,'location':1,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':69,'location':0,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':70,'location':4,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':71,'location':4,'similarity':4,'interference':1,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':72,'location':8,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':73,'location':4,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':74,'location':8,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':75,'location':2,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':76,'location':5,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':77,'location':2,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':78,'location':2,'similarity':3,'interference':1,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':79,'location':13,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':80,'location':2,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':81,'location':13,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':82,'location':14,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':83,'location':13,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':84,'location':12,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':85,'location':12,'similarity':1,'interference':1,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':86,'location':1,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':87,'location':12,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':88,'location':0,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':89,'location':12,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':0},
        {'trial_number':90,'location':0,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':0},
        {'trial_number':91,'location':12,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':0},
        ]
        self.dataTemplates['testing_b']= [ \
        {'trial_number':0,'location':9,'similarity':None,'interference':None,'corr_resp':'none','visual_hemifield':None},
        {'trial_number':1,'location':0,'similarity':None,'interference':None,'corr_resp':'none','visual_hemifield':None},
        {'trial_number':2,'location':12,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':3,'location':0,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':0},
        {'trial_number':4,'location':12,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':0},
        {'trial_number':5,'location':0,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':0},
        {'trial_number':6,'location':12,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':7,'location':1,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':8,'location':12,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':9,'location':12,'similarity':4,'interference':1,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':10,'location':13,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':11,'location':14,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':12,'location':13,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':13,'location':2,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':14,'location':13,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':0},
        {'trial_number':15,'location':2,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':16,'location':2,'similarity':4,'interference':1,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':17,'location':5,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':18,'location':2,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':19,'location':8,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':20,'location':4,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':21,'location':8,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':22,'location':4,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':23,'location':4,'similarity':4,'interference':1,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':24,'location':0,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':25,'location':1,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':26,'location':13,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':27,'location':2,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':28,'location':14,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':29,'location':6,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':30,'location':14,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':31,'location':7,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':32,'location':10,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':33,'location':3,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':34,'location':7,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':35,'location':5,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':36,'location':10,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':37,'location':5,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':38,'location':10,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':39,'location':6,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':40,'location':10,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':41,'location':6,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':42,'location':8,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':43,'location':3,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':44,'location':8,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':45,'location':7,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':46,'location':9,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':47,'location':7,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':48,'location':9,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':49,'location':9,'similarity':2,'interference':1,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':50,'location':8,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':51,'location':11,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':52,'location':11,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':53,'location':11,'similarity':0,'interference':1,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':54,'location':13,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':55,'location':11,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':56,'location':0,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':57,'location':8,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':58,'location':0,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':0},
        {'trial_number':59,'location':12,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':60,'location':14,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':61,'location':14,'similarity':2,'interference':1,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':62,'location':11,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':63,'location':14,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':64,'location':12,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':65,'location':1,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':66,'location':1,'similarity':4,'interference':1,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':67,'location':3,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':68,'location':5,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':69,'location':0,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':70,'location':5,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':71,'location':4,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':72,'location':1,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':73,'location':4,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':74,'location':1,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':75,'location':3,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':76,'location':1,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':77,'location':3,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':78,'location':13,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':79,'location':2,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':80,'location':10,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':81,'location':5,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':82,'location':6,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':83,'location':7,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':84,'location':6,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':85,'location':6,'similarity':1,'interference':1,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':86,'location':10,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':87,'location':4,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':88,'location':9,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':89,'location':2,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':90,'location':9,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':0},
        {'trial_number':91,'location':3,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':0},
        ]
        self.dataTemplates['testing_c']= [ \
        {'trial_number':0,'location':10,'similarity':None,'interference':None,'corr_resp':'none','visual_hemifield':None},
        {'trial_number':1,'location':4,'similarity':None,'interference':None,'corr_resp':'none','visual_hemifield':None},
        {'trial_number':2,'location':10,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':3,'location':1,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':4,'location':9,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':5,'location':1,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':6,'location':11,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':7,'location':2,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':8,'location':13,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':9,'location':13,'similarity':4,'interference':1,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':10,'location':14,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':11,'location':13,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':12,'location':12,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':13,'location':2,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':14,'location':9,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':15,'location':5,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':16,'location':10,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':17,'location':8,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':18,'location':10,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':19,'location':8,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':20,'location':11,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':21,'location':8,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':22,'location':11,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':23,'location':12,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':24,'location':7,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':25,'location':12,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':26,'location':10,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':27,'location':8,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':28,'location':8,'similarity':2,'interference':1,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':29,'location':4,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':30,'location':6,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':31,'location':3,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':32,'location':6,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':33,'location':6,'similarity':3,'interference':1,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':34,'location':4,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':35,'location':7,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':36,'location':0,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':37,'location':7,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':38,'location':3,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':39,'location':5,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':40,'location':3,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':41,'location':3,'similarity':2,'interference':1,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':42,'location':3,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':43,'location':0,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':44,'location':1,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':45,'location':1,'similarity':1,'interference':1,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':46,'location':14,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':47,'location':1,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':48,'location':14,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':49,'location':0,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':50,'location':10,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':51,'location':0,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':0},
        {'trial_number':52,'location':13,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':53,'location':2,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':54,'location':13,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':55,'location':2,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':56,'location':12,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':57,'location':2,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':58,'location':12,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':59,'location':14,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':60,'location':10,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':61,'location':2,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':62,'location':14,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':63,'location':6,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':64,'location':13,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':65,'location':6,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':66,'location':9,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':67,'location':5,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':68,'location':8,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':69,'location':7,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':70,'location':11,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':71,'location':11,'similarity':4,'interference':1,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':72,'location':0,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':73,'location':11,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':74,'location':0,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':0},
        {'trial_number':75,'location':9,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':76,'location':12,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':77,'location':9,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':78,'location':9,'similarity':3,'interference':1,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':79,'location':5,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':80,'location':9,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':2},
        {'trial_number':81,'location':5,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':82,'location':6,'similarity':3,'interference':0,'corr_resp':'right','visual_hemifield':2},
        {'trial_number':83,'location':5,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':84,'location':4,'similarity':2,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':85,'location':4,'similarity':1,'interference':1,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':86,'location':8,'similarity':4,'interference':0,'corr_resp':'right','visual_hemifield':1},
        {'trial_number':87,'location':4,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':88,'location':7,'similarity':1,'interference':0,'corr_resp':'right','visual_hemifield':0},
        {'trial_number':89,'location':4,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':0},
        {'trial_number':90,'location':7,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':1},
        {'trial_number':91,'location':4,'similarity':0,'interference':0,'corr_resp':'left','visual_hemifield':0},
        ]

    def initializeTrialData(self,form,setName):
        """Configures the trialData handler using data template for the form and setName

        :parameters:
            form - the alternate form of the task.
            setName - the set name of the data template (e.g. 'practice1','testing')
        """
        if(form==None):
            form = 'a'
        if(setName==None):
            setName = 'testing'

        dataTemplate = self.dataTemplates[setName + '_' + form.lower()]
        if(dataTemplate != None):
            self.trialHandler = data.TrialHandler(dataTemplate,1,method="sequential")
        else:
            logging.error("Error configuring two back trial block for Form = " + form + " and Set=" + setName + ".")
            core.quit();

    def doBeforeTrialBlock(self):
        """Sets up common stimuli for the block."""
        self.target=visual.ImageStim(win=self.task.window, image=lavatask.base.Resource('whitesquare.bmp',self.task).getResourceLocation(),size=2.5,units='cm')

        self.yesStimuli=visual.TextStim(win=self.task.window, ori=0,text=lavatask.base.UnicodeResource("yes_prompt.txt",self.task).getText(),pos=[-10,-7.5], height=1, color=[1,1,-1], units='cm')
        self.noStimuli=visual.TextStim(win=self.task.window, ori=0,text=lavatask.base.UnicodeResource("no_prompt.txt",self.task).getText(),pos=[11,-7.5], height=1, color=[1,1,-1], units='cm')




    def doBeforeTrial(self):
        """Configures the next trial or ends block if no more trials."""
        try:
            # get next trial data
            self.currentTrial = self.trialHandler.next()
        except StopIteration:  #no more trials
            self.setContinueTrial(False)
            self.setContinue(False)
            return

        if(self.currentTrial.corr_resp == 'none'):
            #trials without responses need to timeout  ( in this case just the initial target)
            self.trialTimeout=self.nonResponseTrialTimeout
            self.responseTrial=False
        else:
            self.trialTimeout=None
            self.responseTrial=True


        #reset the trial "draw stage" variable
        self.trialDrawStage = 0

        #setup the target stimuli location
        self.setTargetPosition(self.currentTrial.location)


        self.lastResponse = None
        self.lastResponseTime = None
        self.lastResponseDevice = None
        self.lastTrialCorrect = None
        self.resetClock()

        #turn off response checking (until prompt is displayed)
        self.disableResponse()

    def setTargetPosition(self,location):
        """Set the location of the target stimuli on the screen"""
        if(location == 0):self.target.setPos([0,7.2])
        elif(location == 1):self.target.setPos([3.4,6.5])
        elif(location == 2):self.target.setPos([6.2,4.8])
        elif(location == 3):self.target.setPos([8.3,2.2])
        elif(location == 4):self.target.setPos([8.7,-0.8])
        elif(location == 5):self.target.setPos([7.5,-3.6])
        elif(location == 6):self.target.setPos([4.9,-6.0])
        elif(location == 7):self.target.setPos([1.7,-7.0])
        elif(location == 8):self.target.setPos([-1.7,-7.0])
        elif(location == 9):self.target.setPos([-4.9,-6.0])
        elif(location == 10):self.target.setPos([-7.5,-3.6])
        elif(location == 11):self.target.setPos([-8.7,-0.8])
        elif(location == 12):self.target.setPos([-8.3,2.2])
        elif(location == 13):self.target.setPos([-6.2,4.8])
        elif(location == 14):self.target.setPos([-3.4,6.5])



    def doTrialTimeout(self):
        """Trials without responses timeout"""
        response = NBackResponse()
        response.block=self
        response.trialData = self.currentTrial
        response.key='none'
        response.responseDevice = 'none'
        response.rt=0
        response.taskTime=self.task.getTime()
        response.corr=0
        self.lastTrialCorrect=response.corr
        self.task.responses.addResponse(response)

    def doBeforeTrialResponse(self):

       # self.debugDrawTargets()
        if(self.trialDrawStage == 0):
                self.drawBackground("Black")
                self.target.draw()
                if(self.responseTrial == True):
                    self.enableResponse()
                    self.yesStimuli.draw()
                    self.noStimuli.draw()
                self.trialDrawStage = 1
                self.task.refreshWindow()

        elif(self.trialDrawStage == 1 and self.getTime()>= self.targetDisplayDuration):
                self.drawBackground("Black")
                if(self.responseTrial == True):
                    self.yesStimuli.draw()
                    self.noStimuli.draw()
                self.trialDrawStage = 2
                self.task.refreshWindow()

    def doAfterTrialResponse(self):
         """Checks correctness of response and records response data."""
         response = NBackResponse()
         response.block=self
         response.trialData = self.currentTrial
         response.key=self.lastResponse
         response.responseDevice = self.lastResponseDevice
         response.rt=(self.lastResponseTime)
         response.taskTime=self.task.getTime()
         if(response.key == response.trialData.corr_resp):
            response.corr=1
            self.totalCorrect += 1
         else:
            response.corr=0
         self.lastTrialCorrect=response.corr
         self.task.responses.addResponse(response)


    def doAfterTrial(self):
        """Draws intertarget fixation and the response feedback if response feedback is enabled for block."""
       #First need to wait for the full target display period to complete
        while(self.getTime() < self.targetDisplayDuration):
            self.wait(.010)

        #clear targets
        if(self.responseTrial==True):
            self.drawBackground("Black")
            self.yesStimuli.draw()
            self.noStimuli.draw()
            self.task.refreshWindow()




class TwoBackDemoBlock(TwoBackBlock):
    """Extends TwoBackBlock class to implement Demo block specific trial functionality.


    There are two initial trials for which responses are not collected.  The remaining trials
        require a response to continue.

        Non response trials
        1) targets: Displayed with instructions until spacebar is hit.
        2) 1 second delay

        Response Trials
        1) Probe: displayed with instructions until response (first three trials include YES/NO Instructions)
        2) User input: wait for user input (may be provided as soon as the probe is displayed)
        3) 500 ms delay after the response is provided
        4) Feedback Displayed for 2 seconds

        note) Yes/No Stimuli: once displayed on a block, they stay on

    """
    def __init__(self,task,name,keys=["left","right","space"],trialData=None):
        TwoBackBlock.__init__(self,task,name,keys,trialData)
        self.totalCorrect=0 #count of the number of correct responses
        self.dataTemplates = {}

        self.dataTemplates.clear()
        self.dataTemplates['demo_a']= [ \
        {'trial_number':0,'location':14,'similarity':None,'corr_resp':'none'},
        {'trial_number':1,'location':11,'similarity':None,'corr_resp':'none'},
        {'trial_number':2,'location':2,'similarity':4,'corr_resp':'right'},
        {'trial_number':3,'location':11,'similarity':0,'corr_resp':'left'},
        {'trial_number':4,'location':5,'similarity':3,'corr_resp':'right'},
        {'trial_number':5,'location':9,'similarity':3,'corr_resp':'right'},
        {'trial_number':6,'location':5,'similarity':0,'corr_resp':'left'},
        {'trial_number':7,'location':9,'similarity':0,'corr_resp':'left'},
        {'trial_number':8,'location':1,'similarity':4,'corr_resp':'right'},
        {'trial_number':9,'location':12,'similarity':2,'corr_resp':'right'},
        {'trial_number':10,'location':1,'similarity':0,'corr_resp':'left'},
        {'trial_number':11,'location':12,'similarity':0,'corr_resp':'left'},
        ]
        self.dataTemplates['demo_b'] = self.dataTemplates['demo_a']
        self.dataTemplates['demo_c'] = self.dataTemplates['demo_a']




    def doBeforeTrialBlock(self):
        """Sets up common stimuli for the block."""

        TwoBackBlock.doBeforeTrialBlock(self)
        self.demoProbePrompt = visual.TextStim(win=self.task.window, ori=0,text=lavatask.base.UnicodeResource("2demo_probe_prompt.txt",self.task).getCenteredText(),pos=[0,0], height=.8,color=[-1,-1,1],wrapWidth=50)
        self.demoTarget1Prompt = visual.TextStim(win=self.task.window, ori=0,text=lavatask.base.UnicodeResource("2demo_target1_prompt.txt",self.task).getCenteredText(),pos=[0, 0], height=.8, color=[-1,-1,1],wrapWidth=50)
        self.demoTarget2Prompt = visual.TextStim(win=self.task.window, ori=0,text=lavatask.base.UnicodeResource("2demo_target2_prompt.txt",self.task).getCenteredText(),pos=[0, 0], height=.8, color=[-1,-1,1],wrapWidth=50)
        self.demoProbeYesNoPrompt = visual.TextStim(win=self.task.window, ori=0,text=lavatask.base.UnicodeResource("2demo_yesno_prompt.txt",self.task).getCenteredText(),pos=[0,0], height=.8,color=[-1,-1,1],wrapWidth=50)
        self.correctStimuli=visual.TextStim(win=self.task.window, ori=0,text=lavatask.base.UnicodeResource("feedback_correct.txt",self.task).getCenteredText(),pos=[0, 0], height=.8, color=[1,1,-1],wrapWidth=50)
        self.incorrectStimuli=visual.TextStim(win=self.task.window, ori=0,text=lavatask.base.UnicodeResource("feedback_incorrect.txt",self.task).getCenteredText(),pos=[0, 0], height=.8, color=[1,-1,-1], wrapWidth=50)





    def doBeforeTrialResponse(self):

        if(self.trialDrawStage == 0):
            self.drawBackground("Black")
            self.target.draw()
            self.enableResponse()

            if(self.currentTrial.trial_number==0):
                self.demoTarget1Prompt.draw()
            elif(self.currentTrial.trial_number==1):
                self.demoTarget2Prompt.draw()
            elif(self.currentTrial.trial_number <= 5):
                self.demoProbeYesNoPrompt.draw()
            else:
                self.demoProbePrompt.draw()

            if(self.responseTrial == True):
                self.yesStimuli.draw()
                self.noStimuli.draw()
            self.trialDrawStage = 1
            self.task.refreshWindow()



    def doAfterTrial(self):
        """Draws intertarget fixation and the response feedback if response feedback is enabled for block."""
       #First need to wait for the full target display period to complete
        while(self.getTime() < self.targetDisplayDuration):
            self.wait(.010)


        #clear target and wait 500 milliseconds
        self.drawBackground("Black")
        if(self.responseTrial == True):
            self.yesStimuli.draw()
            self.noStimuli.draw()
        self.task.refreshWindow()
        self.wait(self.standardDelay)

        #display feedback if this is a response trial
        if(self.responseTrial==True):
            self.drawBackground("Black")
            if(self.lastTrialCorrect == True):
                self.correctStimuli.draw()
            elif(self.lastTrialCorrect == False):
                self.incorrectStimuli.draw()

            if(self.responseTrial == True):
                self.yesStimuli.draw()
                self.noStimuli.draw()

            self.task.refreshWindow()
            self.wait(self.displayFeedbackDuration)

            #clear feedback
            self.drawBackground("Black")
            if(self.responseTrial == True):
                self.yesStimuli.draw()
                self.noStimuli.draw()
            self.task.refreshWindow()




class NBackResponses(lavatask.base.TaskResponses):
    """Extends TaskResponses class to implement NBack specific summary scoring.

    Summary scoring for NBack is
        1) Total Correct
        2) Total Errors
        3) Mean of reaction times to correct responses
        4) Median reaction time to correct responses
        5) Stdev of reaction times to correct responses

    These scoring values are calculated for:

        1) Overall Total (all trials)
        2) Similarity Match
        3) Similarity 1
        4) Similarity 2
        5) Similarity 3
        6) Similarity 4
        7) Visual Hemifield Left
        8) Visual Hemifield Right
        9) Interference (2Back only)

    There is also a total trials attempted score that helps identify incomplete testing sessions.

    There are also overall adjusted "score" and "bias" variables (using dprime).

    """
    def __init__(self,task):
        lavatask.base.TaskResponses.__init__(self,task)

    def getSummaryStatsColumns(self):
        """Return column names for the summary statistics."""
        columns = lavatask.base.TaskResponses.getSummaryStatsColumns(self)
        for column in ['response_device','nb1_total_trials','nb1_score','nb1_bias',
            'nb1_corr','nb1_errors','nb1_mean','nb1_median','nb1_stdev',
            'nb1sm_corr','nb1sm_errors','nb1sm_mean','nb1sm_median','nb1sm_stdev',
            'nb1s1_corr','nb1s1_errors','nb1s1_mean','nb1s1_median','nb1s1_stdev',
            'nb1s2_corr','nb1s2_errors','nb1s2_mean','nb1s2_median','nb1s2_stdev',
            'nb1s3_corr','nb1s3_errors','nb1s3_mean','nb1s3_median','nb1s3_stdev',
            'nb1s4_corr','nb1s4_errors','nb1s4_mean','nb1s4_median','nb1s4_stdev',
            'nb1vhL_corr','nb1vhL_errors','nb1vhL_mean','nb1vhL_median','nb1vhL_stdev',
            'nb1vhR_corr','nb1vhR_errors','nb1vhR_mean','nb1vhR_median','nb1vhR_stdev',
            'nb2_total_trials','nb2_score','nb2_bias',
            'nb2_corr','nb2_errors','nb2_mean','nb2_median','nb2_stdev',
            'nb2sm_corr','nb2sm_errors','nb2sm_mean','nb2sm_median','nb2sm_stdev',
            'nb2s1_corr','nb2s1_errors','nb2s1_mean','nb2s1_median','nb2s1_stdev',
            'nb2s2_corr','nb2s2_errors','nb2s2_mean','nb2s2_median','nb2s2_stdev',
            'nb2s3_corr','nb2s3_errors','nb2s3_mean','nb2s3_median','nb2s3_stdev',
            'nb2s4_corr','nb2s4_errors','nb2s4_mean','nb2s4_median','nb2s4_stdev',
            'nb2vhL_corr','nb2vhL_errors','nb2vhL_mean','nb2vhL_median','nb2vhL_stdev',
            'nb2vhR_corr','nb2vhR_errors','nb2vhR_mean','nb2vhR_median','nb2vhR_stdev',
            'nb2int_corr','nb2int_errors','nb2int_mean','nb2int_median','nb2int_stdev',
            'nb2noint_corr','nb2noint_errors','nb2noint_mean','nb2noint_median','nb2noint_stdev',
        ]:
            columns.append(column)
        return columns

    def getSummaryStatsFields(self):
        """Calculate the summary stats and return the data as a dictionary."""
        fields = lavatask.base.TaskResponses.getSummaryStatsFields(self)
        response_device=None
        nb1_total = []
        nb1_sm = []
        nb1_s1 = []
        nb1_s2 = []
        nb1_s3 = []
        nb1_s4 = []
        nb1_vhL = []
        nb1_vhR = []
        nb2_total = []
        nb2_sm = []
        nb2_s1 = []
        nb2_s2 = []
        nb2_s3 = []
        nb2_s4 = []
        nb2_vhL = []
        nb2_vhR = []
        nb2_int = []
        nb2_noint = []

        nb1_total_errors = 0
        nb1_sm_errors = 0
        nb1_s1_errors = 0
        nb1_s2_errors = 0
        nb1_s3_errors = 0
        nb1_s4_errors = 0
        nb1_vhL_errors = 0
        nb1_vhR_errors = 0
        nb2_total_errors = 0
        nb2_sm_errors = 0
        nb2_s1_errors = 0
        nb2_s2_errors = 0
        nb2_s3_errors = 0
        nb2_s4_errors = 0
        nb2_vhL_errors = 0
        nb2_vhR_errors = 0
        nb2_int_errors = 0
        nb2_noint_errors = 0


        nb1_attempted=0
        nb2_attempted=0

        #compile correct response data into groups for summary stats
        for response in self.data:
            if(response['block_name']=='nb1TestingBlock'):
                if(response['response_device']!='none'):
                    if(response_device == None):
                        response_device = response['response_device']
                    elif (response_device != 'multiple' and response_device != response['response_device']):
                        response_device = 'multiple'
                #exclude initial trials
                if(response['trial_corr_resp']!='none'):
                    nb1_attempted+=1
                    if(response['resp_corr']==1):
                        rt = response['resp_rt']
                        nb1_total.append(rt)
                        if(response['trial_similarity']==0):nb1_sm.append(rt)
                        elif(response['trial_similarity']==1):nb1_s1.append(rt)
                        elif(response['trial_similarity']==2):nb1_s2.append(rt)
                        elif(response['trial_similarity']==3):nb1_s3.append(rt)
                        elif(response['trial_similarity']==4):nb1_s4.append(rt)

                        if(response['trial_visual_hemi']==1):nb1_vhL.append(rt)
                        elif(response['trial_visual_hemi']==2):nb1_vhR.append(rt)

                    else:
                        nb1_total_errors += 1
                        if(response['trial_similarity']==0):nb1_sm_errors += 1
                        elif(response['trial_similarity']==1):nb1_s1_errors += 1
                        elif(response['trial_similarity']==2):nb1_s2_errors += 1
                        elif(response['trial_similarity']==3):nb1_s3_errors += 1
                        elif(response['trial_similarity']==4):nb1_s4_errors += 1

                        if(response['trial_visual_hemi']==1):nb1_vhL_errors += 1
                        elif(response['trial_visual_hemi']==2):nb1_vhR_errors += 1


            elif(response['block_name']=='nb2TestingBlock'):
                if(response['response_device']!='none'):
                    if(response_device == None):
                        response_device = response['response_device']
                    elif (response_device != 'multiple' and response_device != response['response_device']):
                        response_device = 'multiple'
                #exclude initial trials
                if(response['trial_corr_resp']!='none'):
                    nb2_attempted+=1
                    if(response['resp_corr']==1):
                        rt = response['resp_rt']
                        nb2_total.append(rt)
                        if(response['trial_similarity']==0):nb2_sm.append(rt)
                        elif(response['trial_similarity']==1):nb2_s1.append(rt)
                        elif(response['trial_similarity']==2):nb2_s2.append(rt)
                        elif(response['trial_similarity']==3):nb2_s3.append(rt)
                        elif(response['trial_similarity']==4):nb2_s4.append(rt)

                        if(response['trial_visual_hemi']==1):nb2_vhL.append(rt)
                        elif(response['trial_visual_hemi']==2):nb2_vhR.append(rt)

                        if(response['trial_interference']==0):nb2_noint.append(rt)
                        elif(response['trial_interference']==1):nb2_int.append(rt)

                    else:
                        nb2_total_errors += 1
                        if(response['trial_similarity']==0):nb2_sm_errors += 1
                        elif(response['trial_similarity']==1):nb2_s1_errors += 1
                        elif(response['trial_similarity']==2):nb2_s2_errors += 1
                        elif(response['trial_similarity']==3):nb2_s3_errors += 1
                        elif(response['trial_similarity']==4):nb2_s4_errors += 1

                        if(response['trial_visual_hemi']==1):nb2_vhL_errors += 1
                        elif(response['trial_visual_hemi']==2):nb2_vhR_errors += 1

                        if(response['trial_interference']==0):nb2_noint_errors += 1
                        elif(response['trial_interference']==1):nb2_int_errors += 1


        #do summary stats on each summary group and add to fields collection

        fields.update({'response_device':response_device})
        fields.update({'nb1_total_trials':nb1_attempted})
        fields.update({'nb1_corr':self.calcCorrect(nb1_total),'nb1_errors':nb1_total_errors,'nb1_mean':self.calcMean(nb1_total),'nb1_median':self.calcMedian(nb1_total),'nb1_stdev':self.calcStDev(nb1_total)})
        fields.update({'nb1sm_corr':self.calcCorrect(nb1_sm),'nb1sm_errors':nb1_sm_errors,'nb1sm_mean':self.calcMean(nb1_sm),'nb1sm_median':self.calcMedian(nb1_sm),'nb1sm_stdev':self.calcStDev(nb1_sm)})
        fields.update({'nb1s1_corr':self.calcCorrect(nb1_s1),'nb1s1_errors':nb1_s1_errors,'nb1s1_mean':self.calcMean(nb1_s1),'nb1s1_median':self.calcMedian(nb1_s1),'nb1s1_stdev':self.calcStDev(nb1_s1)})
        fields.update({'nb1s2_corr':self.calcCorrect(nb1_s2),'nb1s2_errors':nb1_s2_errors,'nb1s2_mean':self.calcMean(nb1_s2),'nb1s2_median':self.calcMedian(nb1_s2),'nb1s2_stdev':self.calcStDev(nb1_s2)})
        fields.update({'nb1s3_corr':self.calcCorrect(nb1_s3),'nb1s3_errors':nb1_s3_errors,'nb1s3_mean':self.calcMean(nb1_s3),'nb1s3_median':self.calcMedian(nb1_s3),'nb1s3_stdev':self.calcStDev(nb1_s3)})
        fields.update({'nb1s4_corr':self.calcCorrect(nb1_s4),'nb1s4_errors':nb1_s4_errors,'nb1s4_mean':self.calcMean(nb1_s4),'nb1s4_median':self.calcMedian(nb1_s4),'nb1s4_stdev':self.calcStDev(nb1_s4)})
        fields.update({'nb1vhL_corr':self.calcCorrect(nb1_vhL),'nb1vhL_errors':nb1_vhL_errors,'nb1vhL_mean':self.calcMean(nb1_vhL),'nb1vhL_median':self.calcMedian(nb1_vhL),'nb1vhL_stdev':self.calcStDev(nb1_vhL)})
        fields.update({'nb1vhR_corr':self.calcCorrect(nb1_vhR),'nb1vhR_errors':nb1_vhR_errors,'nb1vhR_mean':self.calcMean(nb1_vhR),'nb1vhR_median':self.calcMedian(nb1_vhR),'nb1vhR_stdev':self.calcStDev(nb1_vhR)})

        fields.update({'nb2_total_trials':nb2_attempted})
        fields.update({'nb2_corr':self.calcCorrect(nb2_total),'nb2_errors':nb2_total_errors,'nb2_mean':self.calcMean(nb2_total),'nb2_median':self.calcMedian(nb2_total),'nb2_stdev':self.calcStDev(nb2_total)})
        fields.update({'nb2sm_corr':self.calcCorrect(nb2_sm),'nb2sm_errors':nb2_sm_errors,'nb2sm_mean':self.calcMean(nb2_sm),'nb2sm_median':self.calcMedian(nb2_sm),'nb2sm_stdev':self.calcStDev(nb2_sm)})
        fields.update({'nb2s1_corr':self.calcCorrect(nb2_s1),'nb2s1_errors':nb2_s1_errors,'nb2s1_mean':self.calcMean(nb2_s1),'nb2s1_median':self.calcMedian(nb2_s1),'nb2s1_stdev':self.calcStDev(nb2_s1)})
        fields.update({'nb2s2_corr':self.calcCorrect(nb2_s2),'nb2s2_errors':nb2_s2_errors,'nb2s2_mean':self.calcMean(nb2_s2),'nb2s2_median':self.calcMedian(nb2_s2),'nb2s2_stdev':self.calcStDev(nb2_s2)})
        fields.update({'nb2s3_corr':self.calcCorrect(nb2_s3),'nb2s3_errors':nb2_s3_errors,'nb2s3_mean':self.calcMean(nb2_s3),'nb2s3_median':self.calcMedian(nb2_s3),'nb2s3_stdev':self.calcStDev(nb2_s3)})
        fields.update({'nb2s4_corr':self.calcCorrect(nb2_s4),'nb2s4_errors':nb2_s4_errors,'nb2s4_mean':self.calcMean(nb2_s4),'nb2s4_median':self.calcMedian(nb2_s4),'nb2s4_stdev':self.calcStDev(nb2_s4)})
        fields.update({'nb2vhL_corr':self.calcCorrect(nb2_vhL),'nb2vhL_errors':nb2_vhL_errors,'nb2vhL_mean':self.calcMean(nb2_vhL),'nb2vhL_median':self.calcMedian(nb2_vhL),'nb2vhL_stdev':self.calcStDev(nb2_vhL)})
        fields.update({'nb2vhR_corr':self.calcCorrect(nb2_vhR),'nb2vhR_errors':nb2_vhR_errors,'nb2vhR_mean':self.calcMean(nb2_vhR),'nb2vhR_median':self.calcMedian(nb2_vhR),'nb2vhR_stdev':self.calcStDev(nb2_vhR)})
        fields.update({'nb2int_corr':self.calcCorrect(nb2_int),'nb2int_errors':nb2_int_errors,'nb2int_mean':self.calcMean(nb2_int),'nb2int_median':self.calcMedian(nb2_int),'nb2int_stdev':self.calcStDev(nb2_int)})
        fields.update({'nb2noint_corr':self.calcCorrect(nb2_noint),'nb2noint_errors':nb2_noint_errors,'nb2noint_mean':self.calcMean(nb2_noint),'nb2noint_median':self.calcMedian(nb2_noint),'nb2noint_stdev':self.calcStDev(nb2_noint)})


        if(nb1_attempted == 30 and fields['nb1_corr'] > 0):
            nb1_hits = ((fields['nb1sm_corr']) +.500) / 11.000
            nb1_nonmatch_corr = (fields['nb1s1_corr'] + fields['nb1s2_corr'] + fields['nb1s3_corr'] + fields['nb1s4_corr']) * 1.000
            nb1_false_alarms = (((20.000 - nb1_nonmatch_corr)) + .500) / 21.000
            nb1_z_fa = norm.ppf(nb1_false_alarms)
            nb1_z_hit = norm.ppf(nb1_hits)
            nb1_score = round(nb1_z_hit - nb1_z_fa,3)
            nb1_bias = round((nb1_z_hit + nb1_z_fa) / 2.000,3)

            fields.update({'nb1_bias':nb1_bias,'nb1_score':nb1_score})
        else:
            fields.update({'nb1_bias':-5,'nb1_score':-5})


        if(nb2_attempted == 90 and fields['nb2_corr'] > 0):
            nb2_hits = ((fields['nb2sm_corr']) +.500) / 31.000
            nb2_nonmatch_corr = (fields['nb2s1_corr'] + fields['nb2s2_corr'] + fields['nb2s3_corr'] + fields['nb2s4_corr']) * 1.000
            nb2_false_alarms = (((60.000 - nb2_nonmatch_corr)) + .500) / 61.000
            nb2_z_fa = norm.ppf(nb2_false_alarms)
            nb2_z_hit = norm.ppf(nb2_hits)
            nb2_score = round(nb2_z_hit - nb2_z_fa,3)
            nb2_bias = round((nb2_z_hit + nb2_z_fa) / 2.000,3)
            fields.update({'nb2_bias':nb2_bias,'nb2_score':nb2_score})
        else:
            fields.update({'nb2_bias':-5,'nb2_score':-5})

# alternative where we equalize the ranges....
#        if(nb1_attempted == 30 and fields['nb1_corr'] > 0):
#            nb1_hits = ((fields['nb1sm_corr']*10.000) +.500) / 101.000
#            nb1_nonmatch_corr = (fields['nb1s1_corr'] + fields['nb1s2_corr'] + fields['nb1s3_corr'] + fields['nb1s4_corr']) * 1.000
#            nb1_false_alarms = (((20.000 - nb1_nonmatch_corr)*5.000) + .500) / 101.000
#            nb1_z_fa = norm.ppf(nb1_false_alarms)
#            nb1_z_hit = norm.ppf(nb1_hits)
#            nb1_score = round(nb1_z_hit - nb1_z_fa,3)
#            nb1_bias = round((nb1_z_hit + nb1_z_fa) / 2.000,3)
#
#            fields.update({'nb1_bias':nb1_bias,'nb1_score':nb1_score})
#        else:
#            fields.update({'nb1_bias':-5,'nb1_score':-5})
#
#
#        if(nb2_attempted == 90 and fields['nb2_corr'] > 0):
#            nb2_hits = ((fields['nb2sm_corr']*(100.000/30.000)) +.500) / 101.000
#            nb2_nonmatch_corr = (fields['nb2s1_corr'] + fields['nb2s2_corr'] + fields['nb2s3_corr'] + fields['nb2s4_corr']) * 1.000
#            nb2_false_alarms = (((60.000 - nb2_nonmatch_corr)*(100.000/60.000)) + .500) / 101.000
#            nb2_z_fa = norm.ppf(nb2_false_alarms)
#            nb2_z_hit = norm.ppf(nb2_hits)
#            nb2_score = round(nb2_z_hit - nb2_z_fa,3)
#            nb2_bias = round((nb2_z_hit + nb2_z_fa) / 2.000,3)
#            fields.update({'nb2_bias':nb2_bias,'nb2_score':nb2_score})
#        else:
#            fields.update({'nb2_bias':-5,'nb2_score':-5})

        return fields


class NBackResponse(lavatask.base.TrialResponse):
    """Extends TrialResponse class to implement NBack specific trial configuration in output files.

    """
    def __init__(self):
        lavatask.base.TrialResponse.__init__(self)


        {'trial_number':2,'location':6,'similarity':0,'fixation_number':9,'corr_resp':'left'},

    def getTrialConfigurationFields(self):
        """Returns the NBack specific trial configuration data as a dictionary."""

        return {'trial_number':self.trialData.get('trial_number'),'trial_location':self.trialData.get('location'),
                'trial_similarity':self.trialData.get('similarity'),'trial_corr_resp':self.trialData.get('corr_resp'),
                'trial_visual_hemi':self.trialData.get('visual_hemifield'),'trial_interference':self.trialData.get('interference')}

    def getTrialConfigurationColumns(self):
        """Returns the NBack specific trial configuration column names."""
        return ['trial_number','trial_location','trial_similarity','trial_corr_resp','trial_visual_hemi','trial_interference']
