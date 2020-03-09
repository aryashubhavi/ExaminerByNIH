#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Class library that provides extensions to the base EXAMINER computer based task classes for the dot counting task

:Classes:
    DotCountingTask - extends Task class to implement block configuration and control of flow for the DotCounting task.
    DotCountingImageSlide - extends SlideshowSlide class to implement an image based slide
    DotCountingTextSlide - extends SlideshowSlide class to implement a text based slide
    DotCountingQuestionMarkSlide - extends SlideshowSlide class to implement the question mark slides

::Author:
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
import lavatask.base



class DotCountingTask(lavatask.base.Task):
    """Extends Task class to implement block configuration and control of flow for the DotCounting task.

    """
    def __init__(self,configuration,environment=None,sessionConfig=None):
        lavatask.base.Task.__init__(self,configuration,environment,sessionConfig)
        self.name='DotCounting'
        self.version='3.2.0.1'
        self.versionDate='12/30/2011'
        self.resourcePath = os.path.join(self.resourcePath,'examiner','dotcounting')
        self.responses = None #no response recording for the task

    def doBeforeTask(self):
        """Configure task blocks based on ageCohort and language of the task."""
        self.setupTask()
        #log error and quit if no configuration found for the ageCohort and language settings
        if(self.getBlockByName('dotCountingBlock')==None):
            logging.error("DotCounting task not configured.  AgeCohort=" + self.ageCohort +", Language=" + self.language + ".")
            core.quit();



    def setupTask(self):
        """Configure task blocks."""
        slideshow = lavatask.base.SlideshowBlock(self,"dotCountingBlock")
        slideshow.bufferSize=1

        prac1InstrText = lavatask.base.UnicodeResource("practice.txt",self).getCenteredText()

        slideshow.slides.append(DotCountingTextSlide(slideshow,prac1InstrText))


        slideshow.slides.extend(self.getSlidesFromImages(slideshow,['prac1_1.jpg',]))
        questionText = lavatask.base.UnicodeResource("question.txt",self).getCenteredText()

        slideshow.slides.append(DotCountingQuestionMarkSlide(slideshow,1, questionText))

        prac2InstrText = lavatask.base.UnicodeResource("additional_practice.txt",self).getCenteredText()
        slideshow.slides.append(DotCountingTextSlide(slideshow,prac2InstrText))

        slideshow.slides.extend(self.getSlidesFromImages(slideshow,['prac2_1.jpg','prac2_2.jpg',]))

        slideshow.slides.append(DotCountingQuestionMarkSlide(slideshow,2, questionText))


        slideshow.slides.extend(self.getSlidesFromImages(slideshow,['prac3_1.jpg','prac3_2.jpg','prac3_3.jpg',]))
        slideshow.slides.append(DotCountingQuestionMarkSlide(slideshow,3))

        testingText = lavatask.base.UnicodeResource("testing.txt",self).getCenteredText()
        slideshow.slides.append(DotCountingTextSlide(slideshow,testingText))
        slideshow.slides.extend(self.getSlidesFromImages(slideshow,['dots2_1.jpg','dots2_2.jpg',]))
        slideshow.slides.append(DotCountingQuestionMarkSlide(slideshow,2))

        slideshow.slides.extend(self.getSlidesFromImages(slideshow,['dots3_1.jpg','dots3_2.jpg','dots3_3.jpg',]))
        slideshow.slides.append(DotCountingQuestionMarkSlide(slideshow,3))

        slideshow.slides.extend(self.getSlidesFromImages(slideshow,['dots4_1.jpg','dots4_2.jpg','dots4_3.jpg','dots4_4.jpg',]))
        slideshow.slides.append(DotCountingQuestionMarkSlide(slideshow,4))

        slideshow.slides.extend(self.getSlidesFromImages(slideshow,['dots5_1.jpg','dots5_2.jpg','dots5_3.jpg','dots5_4.jpg','dots5_5.jpg',]))
        slideshow.slides.append(DotCountingQuestionMarkSlide(slideshow,5))

        slideshow.slides.extend(self.getSlidesFromImages(slideshow,['dots6_1.jpg','dots6_2.jpg','dots6_3.jpg','dots6_4.jpg','dots6_5.jpg','dots6_6.jpg',]))
        slideshow.slides.append(DotCountingQuestionMarkSlide(slideshow,6))

        slideshow.slides.extend(self.getSlidesFromImages(slideshow,['dots7_1.jpg','dots7_2.jpg','dots7_3.jpg','dots7_4.jpg','dots7_5.jpg','dots7_6.jpg','dots7_7.jpg',]))
        slideshow.slides.append(DotCountingQuestionMarkSlide(slideshow,7))


        completeText = lavatask.base.UnicodeResource("complete.txt",self).getCenteredText()
        slideshow.slides.append(DotCountingTextSlide(slideshow,completeText))

        self.addBlock(slideshow)

    def getSlidesFromImages(self,slideshow, images):
        imageSlides = []
        for image in images:
            imageSlides.append(DotCountingImageSlide(slideshow,image))
        return imageSlides







class DotCountingImageSlide(lavatask.base.SlideshowSlide):
    def __init__(self,slideshow,image):
        lavatask.base.SlideshowSlide.__init__(self,slideshow);
        self.image = image
        self.imageStim = None
        self.size = 28


    def doLoad(self):
        if(self.loaded == False):
            image = lavatask.base.Resource(self.image,self.slideshow.task)
            self.imageStim = visual.ImageStim(win=self.slideshow.task.window, image=image.getResourceLocation(),size=self.size,units='cm')

    def doStart(self):
        if(self.done == False and self.imageStim != None):
            self.slideshow.drawBackground("White")
            self.imageStim.draw();
            self.slideshow.task.refreshWindow();
            return True;

    def doUnload(self):
        self.imageStim = None

class DotCountingTextSlide(lavatask.base.SlideshowSlide):
    def __init__(self,slideshow,text):
        lavatask.base.SlideshowSlide.__init__(self,slideshow);
        self.text = text
        self.textStim = None
        self.size = 26

    def doLoad(self):
        if(self.loaded == False):
            self.textStim = visual.TextStim(win=self.slideshow.task.window, ori=0,text=self.text,pos=[0, 0], \
                                            alignHoriz = 'center',alignVert='center',font=self.slideshow.task.fontName, height=self.slideshow.task.fontSize,color='#000000',wrapWidth=50)

    def doStart(self):
        if(self.done == False and self.textStim != None):
            self.slideshow.drawBackground("White")
            self.textStim.draw();
            self.slideshow.task.refreshWindow();
            return True;

    def doUnload(self):
        self.textStim = None

class DotCountingQuestionMarkSlide(lavatask.base.SlideshowSlide):
    def __init__(self,slideshow,count,text=None):
        lavatask.base.SlideshowSlide.__init__(self,slideshow);
        self.text = text
        self.textStim = None
        self.count = count
        self.size = 26
        self.questionMarkStims = None

    def doLoad(self):
        if(self.loaded == False):
            if(self.text!=None):
                self.textStim = visual.TextStim(win=self.slideshow.task.window, ori=0,text=self.text,pos=[0, 3], \
                                            alignHoriz = 'center',alignVert='center',font=self.slideshow.task.fontName, height=self.slideshow.task.fontSize,color='#000000',wrapWidth=50)
            if(self.count > 0):
                self.questionMarkStims = []
                questionMark =   lavatask.base.Resource('question_mark.jpg',self.slideshow.task)
                for i in range(self.count):
                    xpos = (((self.count-1)/2.0)*-3.0)+(i*3.0);
                    self.questionMarkStims.append(visual.ImageStim(win=self.slideshow.task.window, depth=0, pos=[xpos,0],
                                                      image=questionMark.getResourceLocation(),size=3,units='cm'))

    def doStart(self):
        if(self.done == False):
            self.slideshow.drawBackground("White")
            if (self.textStim != None):
                self.textStim.draw();
            if(self.questionMarkStims!= None):
                for stim in self.questionMarkStims:
                    stim.draw()
            self.slideshow.task.refreshWindow();
            return True;

    def doUnload(self):
        self.textStim = None
        self.questionMarkStims = None
