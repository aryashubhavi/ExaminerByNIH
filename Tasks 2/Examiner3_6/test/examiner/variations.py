#!/usr/bin/env python
# -*- coding: utf-8 -*-

import testCPT
import testDotCounting
import testFlanker
import testNBack
import testSaccades
import testSetShifting

def run():
    
    testCPT.runVariationsTests()
    testDotCounting.runVariationsTests()
    testFlanker.runVariationsTests()
    testNBack.runVariationsTests()
    testSaccades.runVariationsTests()
    testSetShifting.runVariationsTests()

if __name__ == "__main__":
   run() 