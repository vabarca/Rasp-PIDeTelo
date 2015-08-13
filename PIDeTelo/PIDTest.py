#!/usr/bin/python

from CTemp import CTempRasp
from CPID import CArduPID
import time

fTemperatureSetPoint = 40.0 #C
fPIDSampleTime = 1.0 				#seconds
bAggresiveTunning = True

pProcessorTemp = CTempRasp()

myArduPIDCtrl = CArduPID(fTemperatureSetPoint,150.0,255.0,1)
myArduPIDCtrl.setSampleTime(fPIDSampleTime)
myArduPIDCtrl.setAggressiveTunning()

while True:

	currentTemp = pProcessorTemp.getTemp()
	myardupid = myArduPIDCtrl.update(currentTemp)
	diffTemp = abs(fTemperatureSetPoint - currentTemp)

	if (bAggresiveTunning == True) & (diffTemp < 2.0):
		bAggresiveTunning = False
		myArduPIDCtrl.setConservativeTunning()
	elif (bAggresiveTunning == False) & (diffTemp >= 2.0):
		bAggresiveTunning = True
		myArduPIDCtrl.setAggressiveTunning()
	
	print currentTemp,myardupid
	print "---"

	time.sleep(fPIDSampleTime)

