#!/usr/bin/python

import wiringpi2
import time

DELAY_PWM = 0.005

def reset_pins(io):
  pins = [0,1,2,3,4,5,6,7, ]
  for pin in pins:
    io.pinMode(pin,io.OUTPUT)
    io.digitalWrite(pin, io.LOW)

def pwm_dimm(io):
  STEP = 8
  pin = 1 # only supported on this pin
  io.pinMode(pin,io.PWM_OUTPUT)

  while 1:
    for i in range(0,1024,STEP): #print "Up"
      io.pwmWrite(pin, i)
      time.sleep(DELAY_PWM)
    for i in range(1023,-1,-STEP): #print "Down"
      io.pwmWrite(pin, i)
      time.sleep(DELAY_PWM)


# direct
#io = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_SYS)
io = wiringpi2.GPIO(wiringpi2.GPIO.WPI_MODE_PINS)

try:
  reset_pins(io)    
  pwm_dimm(io)

except (KeyboardInterrupt, SystemExit):
  reset_pins(io)