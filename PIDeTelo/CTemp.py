#Used to measure temperature
#	Example	#
#

import subprocess

class CTemp:
	"""
	Discrete Temperatura control
	"""

	def __init__(self):
		return

	def getTemp(self):
		"""
		Return Current processor temperature
		Install lm-sensors
		"""

		process = subprocess.Popen(["sensors"],stdout=subprocess.PIPE,shell=False)
		data = process.communicate()    # returns tuple
		temp = float(data[0].split()[10][1:5])
		return temp
		
	def printTemp(self):
		print self.getTemp()
		
	def __str__(self):
		return str(self.getTemp())
		

class CTempRasp:
	"""
	RaspberryPi temperature
	"""
	def __init__(self):
		return

	def getTemp(self):
		process =  subprocess.Popen("/opt/vc/bin/vcgencmd measure_temp",stdout=subprocess.PIPE,shell=True)
		data = process.communicate()
		temp = float((data[0].split('='))[1][0:4])
		return temp

	def printTemp(self):
		print self.getTemp()
		
	def __str__(self):
		return str(self.getTemp())

