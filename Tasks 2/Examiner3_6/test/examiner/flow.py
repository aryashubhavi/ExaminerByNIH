#!/usr/bin/env python
# -*- coding: utf-8 -*-

import testCPT
import testDotCounting
import testFlanker
import testNBack
import testSaccades
import testSetShifting

def run():
    testCPT.runFlowTests()
    testDotCounting.runFlowTests()
    testFlanker.runFlowTests()
    testNBack.runFlowTests()
    testSaccades.runFlowTests()
    testSetShifting.runFlowTests()

if __name__ == "__main__":
   run() 