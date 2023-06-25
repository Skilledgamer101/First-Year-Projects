import time
import RPi.GPIO as GPIO
from sensor_library import Distance_Sensor
import random
import sys
sensor = Distance_Sensor()
distance_list = []

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pwmFreq = 100

GPIO.setup(18, GPIO.OUT)                # PIN 12 ON BOARD
GPIO.setup(24, GPIO.OUT)                # PIN 18 ON BOARD
GPIO.setup(23, GPIO.OUT)                # PIN 16 ON BOARD
GPIO.setup(25, GPIO.OUT)                # PIN 22 ON BOARD
GPIO.setup(22, GPIO.OUT)                # PIN 15 ON BOARD
GPIO.setup(27, GPIO.OUT)                # PIN 13 ON BOARD
GPIO.setup(17, GPIO.OUT)                # PIN 11 ON BOARD

pwma = GPIO.PWM(18, pwmFreq)
pwmb = GPIO.PWM(17, pwmFreq)
pwma.start(100)
pwmb.start(100)

def runMotor(spd, direction = 0):       # direction = 0 = CW, direction = 1 = CCW
    
    GPIO.output(25, GPIO.HIGH)
    in1 = GPIO.HIGH
    in2 = GPIO.LOW

    if direction == 1:
        in1 = GPIO.LOW
        in2 = GPIO.HIGH

    GPIO.output(23, in1)
    GPIO.output(24, in2)
    pwma.ChangeDutyCycle(spd)

def motorStop():
    GPIO.output(25, GPIO.LOW)


def input_data():                                                                   # gathers a data point every 0.5 seconds, appends data to list and returns list
  value = sensor.distance()
  time.sleep(0.5)
  distance_list.append(value)
    
  return distance_list

def average_calc(distance_list):                                                    # if list contains less then 5 values return None

  if len(distance_list) < 5:
    return None

  else:                                                                             # when list has more than 5 values, divide by the length of the list and return average rounded to 2 decimal places
    average = sum(distance_list)/len(distance_list)
    rounded = round(average,2)
    return rounded

def display_average():

  for i in range(5):
      distance_list = input_data()                                                  # get a list with most recent value from distance sensor
  rounded = average_calc(distance_list)                                             # if list contains 5 items, find rounded average. Otherwise, return None
  print("Distance (raw)\tDistance (avg)")                                           # display distance values and status of output devices to shell
  print(str(distance_list[-1])+'\t\t'+str(rounded))
  distance_list.clear()
  return rounded

def runner(ans):
  avg = display_average()
  while True:
    try:
      while avg < 200:
        try:
          runMotor(ans)
          avg = display_average()
        except KeyboardInterrupt:
          motorStop()
          sys.exit(0)
      motorStop()
      avg = display_average()
    except KeyboardInterrupt:
      sys.exit(0)
  

def process(rounded):

    ans = input("Which fan speed would you like? (1, 2, 3, 4, increasing, or random)\n")
    if ans == "1":
        runner(25)

    elif ans == "2":
        runner(50)

    elif ans == "3":
        runner(75)

    elif ans == "4":
        runner(100)

    elif ans == "random":
      avg = display_average()
      while True:
        try:
          while avg < 200:
            try:
              runMotor(random.randrange(0, 100))
              avg = display_average()
            except KeyboardInterrupt:
              motorStop()
              sys.exit(0)
          motorStop()
          avg = display_average()
        except KeyboardInterrupt:
          sys.exit(0)

    elif ans == "increasing":
      avg = display_average()
      while True:
        try:
          while avg < 200:
            try:
              for i in range(100):
                runMotor(i)
                time.sleep(0.1)
              avg = display_average()
            except KeyboardInterrupt:
              motorStop()
              sys.exit(0)
          motorStop()
          avg = display_average()
        except KeyboardInterrupt:
          sys.exit(0)

    else:
        print("Please enter either 1, 2, 3, 4, increasing, or random\n")
        


while True:
  rounded = display_average()                                                    # find 5 most recent distance values and print their average

  while rounded > 200:                                                           # if there is nothing in front of the sensor initially, do nothing (keep on getting data and printing values)
      try:
        rounded = display_average()
      except KeyboardInterrupt:
        sys.exit(0)
  
  process(rounded)
    
    
