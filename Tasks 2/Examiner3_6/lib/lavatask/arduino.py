"""Class library that provides routines to interact with an Arduino device through serial port communications
over USB connections for computer based tasks.

Modeled from the hardware.cedrus psychopy implementation.
Primary purpose for the class is to support keyboard latency testing. 
It may need significant refactoring for other uses.


:Classes:
    Arduino - base class for the device

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
from psychopy import core,logging
import sys,struct,re
try: import serial
except: serial=False


class Arduino (object):
    """The base object representing the arduino device.
    
    """
    
    class SensorEvent(object):
        """Wraps and parses sensor event from Arduino
        
        """
        def __init__(self,eventString):
            """e[sensorid]:[eventid]:[time]\n"""
            self.sensor=None
            self.event=None
            self.time=None
            
            m = re.match("e(.*?):(.*?):(.*)",eventString)
            if(m):
                self.sensor = int(m.group(1))
                self.event = int(m.group(2))
                self.time = int(m.group(3))
    
    def __init__(self,port,baudrate=115200):
        if not serial:
            raise ImportError("The module serial is needed to connect to the Arduino device.")
        self.portString=port
        
        self.baudrate=baudrate
        
        self.port = serial.Serial(self.portString,baudrate=self.baudrate,bytesize=8,parity='N',stopbits=1,timeout=0.0001)
        self.port.close() #solves access denied error on windows platform. 
        self.port.open()
        self.clearBuffer()
    
    def clearBuffer(self):
        """Empty the input buffer of all characters."""
        self.port.flushInput()
    
    def sendMessage(self,message):
        """Write to the port"""
        self.port.writelines(message)
    
    def readMessage(self):
        """Read and return an unformatted string from the device (and delete this from the buffer)"""
        nToGet = self.port.inWaiting()    
        return self.port.read(nToGet)
    
    def measureRoundtrip(self):
        self.clearBuffer()
        #round trip
        self.sendMessage('m')#start round trip
        #wait for 'x'
        while True:
            if self.readMessage()=='x':
                break     
        self.sendMessage('x')#send it back
        
        #wait for final time info
        msg = ''
        while len(msg)==0:
            msg=self.readMessage()
            msgStart = msg.find('m')
            if(msgStart != -1):
                msgEnd = msg.find('\n',msgStart)
                if(msgEnd != -1):
                    valueStr = msg[msgStart+1:msgEnd-1]
                    return long(valueStr)
        return None
    
    def getSensorEvents(self, allowedSensors=[1,2,3,4,5,6,7], allowedEvents=[0,1]):    
        """Return a list of sensorEvents
            Each event has the following attributes:
            
                event.sensor is the sensor
                event.event is the particular event (convention is 1 = sensor reading, 0 = sensor reading stops) 
                event.time is the time of the event in ms from the last timer reset
                
            allowedSensors will limit the set of sensors that are returned (WARNING: info from other sensors is discarded)
            allowedEvents limits the events returned (WARNING: other events are discarded)
                """
        events = []
        #get the events
        self.sendMessage('e')
        core.wait(0.5)
        msgStr = self.readMessage()
        #loop through messages for events
        msgs = msgStr.split('\n')
        for msg in msgs:
            event = self.SensorEvent(msg)
            if(event.sensor in allowedSensors and event.event in allowedEvents):
                events.append(event)
        return events
    
    def clearEvents(self):
        self.sendMessage('c')
        
    def waitEvents(self, allowedSensors=[1,2,3,4,5,6,7], allowedEvents=[0,1]):
        """Like getSensorEvents, but waits until a event occurs"""
        noEventYet = True
        while noEventYet:
            events = self.getSensorEvents(allowedSensors=allowedSensors, allowedEvents=allowedEvents)
            if len(events)>0:
                noEventYet=False
        return events
        
    def resetTimer(self):
        self.sendMessage('r')
    def getTimer(self):
        """Retrieve the current time on the base timer"""
        self.sendMessage('t')
        core.wait(0.010)
        msg = self.readMessage()
        timerMsgStart = msg.find('t')
        if(timerMsgStart != -1):
            timerMsgEnd = msg.find('\n',timerMsgStart)
            if(timerMsgEnd != -1):
                timerValueStr = msg[timerMsgStart+1:timerMsgEnd-1]
                return long(timerValueStr)
        return None
    
    def getSensorReading(self,sensorNumber):
        """Retrieve the current time on the base timer"""
        self.sendMessage(sensorNumber)
        core.wait(0.010)
        msg = self.readMessage()
        sensorMsgStart = msg.find(':')
        if(sensorMsgStart != -1):
            sensorMsgEnd = msg.find('\n',sensorMsgStart)
            if(sensorMsgEnd != -1):
                sensorValueStr = msg[sensorMsgStart+1:sensorMsgEnd-1]
                return long(sensorValueStr)
        return None
    
    
