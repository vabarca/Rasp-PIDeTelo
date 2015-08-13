#The recipe gives simple implementation of a Discrete Proportional-Integral-Derivative (PID) controller. PID controller gives output value for error between desired reference input and measurement feedback to minimize error value.
#More information: http://en.wikipedia.org/wiki/PID_controller
#
#cnr437@gmail.com
#
#######	Example	#########
#
#p=PID(3.0,0.4,1.2)
#p.setPoint(5.0)
#while True:
#     pid = p.update(measurement_value)
#
#

class CPID:
	"""
	Discrete PID control
	"""

	def __init__(self, P=2.0, I=0.0, D=1.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500):

		self.Kp=P
		self.Ki=I
		self.Kd=D
		self.Derivator=Derivator
		self.Integrator=Integrator
		self.Integrator_max=Integrator_max
		self.Integrator_min=Integrator_min

		self.set_point=0.0
		self.error=0.0

	def update(self,current_value):
		"""
		Calculate PID output value for given reference input and feedback
		"""

		self.error = self.set_point - current_value

		self.P_value = self.Kp * self.error
		self.D_value = self.Kd * ( self.error - self.Derivator)
		self.Derivator = self.error

		self.Integrator = self.Integrator + self.error

		if self.Integrator > self.Integrator_max:
			self.Integrator = self.Integrator_max
		elif self.Integrator < self.Integrator_min:
			self.Integrator = self.Integrator_min

		self.I_value = self.Integrator * self.Ki

		PID = self.P_value + self.I_value + self.D_value

		return PID

	def setPoint(self,set_point):
		"""
		Initilize the setpoint of PID
		"""
		self.set_point = set_point
		self.Integrator=0
		self.Derivator=0

	def setIntegrator(self, Integrator):
		self.Integrator = Integrator

	def setDerivator(self, Derivator):
		self.Derivator = Derivator

	def setKp(self,P):
		self.Kp=P

	def setKi(self,I):
		self.Ki=I

	def setKd(self,D):
		self.Kd=D

	def getPoint(self):
		return self.set_point

	def getError(self):
		return self.error

	def getIntegrator(self):
		return self.Integrator

	def getDerivator(self):
		return self.Derivator
		

class CArduPID:
	"""
	Discrete PID control
	"""
	#DIRECT  = 0
	#REVERSE = 1

	def __init__(self, setPoint,  min, max , controllerDirection = 0, P=2.0, I=0.0, D=1.0): #DIRECT
		self.controllerDirection = controllerDirection
		self.Kp = P
		self.Ki = I
		self.Kd = D
		self.setPoint = setPoint
		self.lastInput = setPoint
		self.output = 0
		self.ITerm = 0
		self.sampleTime = 0.1 # in seconds
		self.error  = 0
		
		self.setOutputLimits(min,max)
		self.setControllerDirection(controllerDirection)
		self.setTunnings(P,I,D)
		
	'''
	from datetime import datetime
	from datetime import timedelta

	start_time = datetime.now()

	# returns the elapsed milliseconds since the start of the program
	def millis():
	   dt = datetime.now() - start_time
	   ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
	   return ms
	'''   

	def update(self,current_value):
		"""
		Calculate PID output value for given reference input and feedback
		"""
		
		#Compute all the working error variables
		self.error = self.setPoint - current_value;
		self.ITerm+= (self.Ki * self.error);
		if self.ITerm > self.outMax:
			self.ITerm= self.outMax;
		elif self.ITerm < self.outMin:
			self.ITerm= self.outMin;
			
		dInput = (current_value - self.lastInput)

		#*Compute PID Output
		self.output = self.Kp * self.error + self.ITerm- self.Kd * dInput;

		if self.output > self.outMax:
			self.output = self.outMax
		elif self.output < self.outMin:
			self.output = self.outMin
			
		#Remember some variables for next time*/
		self.lastInput = current_value;
			
		return self.output
		
	def setAggressiveTunning(self):
		self.setTunnings(4.0,0.2,1.0)
		
	def setConservativeTunning(self):
		self.setTunnings(1.0,0.05,0.25)
		
	def setControllerDirection(self, dir):
		if dir != 0 or dir != 1: #if dir != DIRECT or dir != REVERSE:
			return
		if dir != self.controllerDirection:
			self.Kp = 0-self.Kp
			self.Ki = 0-self.Ki
			self.Kd = 0-self.Kd
		self.controllerDirection = dir
		
	def setSampleTime(self, newSampleTime): # in seconds
		if newSampleTime <= 0:
			return
		ratio = newSampleTime / self.sampleTime
		self.Ki *= ratio
		self.Kd /= ratio
		self.sampleTime = newSampleTime
		
	def setOutputLimits(self,min,max):
		if min >= max:
			return
		
		self.outMin = min
		self.outMax = max
		
		if self.output > self.outMax:
			self.output  = self.outMax
		elif self.output < self.outMin:
			self.output  = self.outMin
			
		if self.ITerm > self.outMax:
			self.ITerm  = self.outMax
		elif self.ITerm < self.outMin:
			self.ITerm  = self.outMin
		

	def setPoint(self,set_point):
		"""
		Initilize the setpoint of PID
		"""
		self.setPoint = setPoint
		

	def setTunnings(self,P,I,D):
		if (P < 0 or I < 0 or D < 0):
			return
			
		self.Kp=P
		self.Ki=I * self.sampleTime;
		self.Kd=D / self.sampleTime;
		
		if self.controllerDirection == 1: #REVERSE:
			self.Kp = 0-self.Kp
			self.Ki = 0-self.Ki
			self.Kd = 0-self.Kd
		
	def getError(self):
		return self.error

