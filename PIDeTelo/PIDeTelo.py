#!/usr/bin/python


#Para controlar el GPIO utilizo la siguiente libreria
#https://github.com/WiringPi/WiringPi2-Python
import wiringpi2
from CTemp import CTempRasp
from CPID import CArduPID
import time
import sys, getopt



def printHelp():
	print ' '
	print 'Usage: PIDeTelo.py [OPTION]'
	print '  -h         help'
	print '  -v         verbose'
	print ' '

def main(argv):
	verbose = False


	try:
		opts, args = getopt.getopt(argv,'hv')
	except getopt.GetoptError:
		printHelp()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-h'):
			printHelp()
			sys.exit()
		elif opt in ('-v'):
			verbose = True

	# Setting up PWM
	PWM_PIN_CONTROL  = 1 # gpio pin 12 = wiringpi no. 1 (BCM 18)
	io = wiringpi2.GPIO(wiringpi2.GPIO.WPI_MODE_PINS)
	io.pinMode(PWM_PIN_CONTROL,io.OUTPUT)
	io.digitalWrite(PWM_PIN_CONTROL, io.LOW)
	io.pinMode(PWM_PIN_CONTROL,io.PWM_OUTPUT)


	# Setting up PID
	fTemperatureSetPoint = 40.0 #C
	fPIDSampleTime = 1.0 				#seconds
	bAggresiveTunning = True

	pProcessorTemp = CTempRasp()
	myArduPIDCtrl = CArduPID(fTemperatureSetPoint,400.0,1024.0,1)
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

		#set pwm value
		io.pwmWrite(PWM_PIN_CONTROL, int(myardupid))

		if verbose == True:
			print currentTemp,int(myardupid)
			print "---"

		time.sleep(fPIDSampleTime)



if __name__ == "__main__":
	main(sys.argv[1:])


