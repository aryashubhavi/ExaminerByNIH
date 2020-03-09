#!/usr/bin/env python
# -*- coding: utf-8 -*-

import testCPT
import testDotCounting
import testFlanker
import testNBack
import testSaccades
import testSetShifting

def run():
    testCPT.runCalcTests()
    testDotCounting.runCalcTests()
    testFlanker.runCalcTests()
    testNBack.runCalcTests()
    testSaccades.runCalcTests()
    testSetShifting.runCalcTests()

if __name__ == "__main__":
   run() 