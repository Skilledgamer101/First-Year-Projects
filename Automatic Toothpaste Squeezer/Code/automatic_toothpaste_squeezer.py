from sensor_library import *
from gpiozero import LED
from gpiozero import Buzzer
from gpiozero import Motor
import sys
import time
import datetime

factor = 1

sensor = Distance_Sensor()
led_object1 = LED(26)
led_object2 = LED(20)
buzzer_object = Buzzer(27)
distance_list = []
status1 = "Off"
status2 = "Off"
motor = "Off"
buzzer = "Off"
same_count = 0
dcmotor = Motor(forward = 16, backward = 12)
cycle = 0
counter = 0

def input_data():                                                               # gathers a data point every 0.5 seconds, appends data to list and returns list
  value = sensor.distance()
  time.sleep(0.5)
  distance_list.append(value)
    
  return distance_list

def average_calc(distance_list):                                                # if list contains less then 5 values return None

  if len(distance_list) < 5:
    return None

  else:                                                                         # when list has more than 5 values, divide by the length of the list and return average rounded to 2 decimal places
    average = sum(distance_list)/len(distance_list)
    rounded = round(average,2)
    return rounded

def display_average():
  
  distance_list = input_data()                                                  # get a list with most recent value from distance sensor
  rounded = average_calc(distance_list)                                         # if list contains 5 items, find rounded average. Otherwise, return None
  print("Distance (raw)\tDistance (avg)\tLED 1\tLED 2\tMotor\tBuzzer")          # display distance values and status of output devices to shell
  print(str(distance_list[-1])+'\t\t'+str(rounded)+'\t\t'+status1+'\t'+status2+'\t'+motor+'\t'+buzzer)
  return rounded

def process_1(rounded):                                                         # rotate motor based on time elapsed and distance values



  current = time.time()
  global distance_list
  global status1
  global status2
  global motor
  global buzzer
  global factor

  while True:
    
    if rounded < 50:
      newcurrent = time.time()
      if (newcurrent - current) < 5:                                              # when time from when toothbrush has been is less than 5 seconds motor turns on at 4rpm for 2 seconds
        motor = "On"
        print("\n\nDistance (raw)\tDistance (avg)\tLED 1\tLED 2\tMotor\tBuzzer")
        print(str(distance_list[-1])+'\t\t'+str(rounded)+'\t\t'+status1+'\t'+status2+'\t'+motor+'\t'+buzzer)
        dcmotor.forward(0.5)
        time.sleep(2)
        dcmotor.stop()
        motor = "Off"
        print('\n')
        
        
      elif (newcurrent - current) >= 5 and (newcurrent - current) <= 10:          # if the toothbrush has been placed for over 5 seconds but under 10 seconds, the motor will run again at a 6rpm for 2 seconds
        motor = "On"
        print("\n\nDistance (raw)\tDistance (avg)\tLED 1\tLED 2\tMotor\tBuzzer")
        print(str(distance_list[-1])+'\t\t'+str(rounded)+'\t\t'+status1+'\t'+status2+'\t'+motor+'\t'+buzzer)
        dcmotor.forward(0.75)
        time.sleep(2)
        dcmotor.stop()
        motor = "Off"
        print('\n')
        

      else:                                                                       # runs through if more than 10 seconds has gone by with toothbrush still in front of sensor
        motor = "On"
        print("\n\nDistance (raw)\tDistance (avg)\tLED 1\tLED 2\tMotor\tBuzzer")
        print(str(distance_list[-1])+'\t\t'+str(rounded)+'\t\t'+status1+'\t'+status2+'\t'+motor+'\t'+buzzer)
        dcmotor.backward(0.25)                                                    # motor spins in opposite direction at 2rpm for 1 second
        time.sleep(1)                                                           
        motor = "Off"
        print('\n')
        dcmotor.stop()
        return

    if rounded > 50:                                                              # same function as 'else' statement above, but occurs when previous loop is exited out of. so, if the user were to keep their toothbrush in from of the sensor for 5 seconds or less, this segment of code would execute for the device to run backwards. 
        motor = "On"
        print("\n\nDistance (raw)\tDistance (avg)\tLED 1\tLED 2\tMotor\tBuzzer")
        print(str(distance_list[-1])+'\t\t'+str(rounded)+'\t\t'+status1+'\t'+status2+'\t'+motor+'\t'+buzzer)
        dcmotor.backward(0.25)
        time.sleep(1)                                                             # motor spins in opposite direction at 2rpm for 1 second
        motor = "Off"
        print('\n')
        dcmotor.stop()
        return

    distance_list.clear()                                                         # the list clears with every 5 data points that are collected
    for i in range(5):
      rounded = display_average() 

def process_1_output(rounded):                                                    # turn on LEDs based on how many times the user has done brush (e.g., 1 time brush = 1 LED). 
                                                                                  # Turn off all at midnight

  current1 = time.time()
  timenow = time.localtime(current1)
  hour = int(time.strftime("%H", timenow))
  global distance_list
  global status1
  global status2
  global motor
  global buzzer
  global counter
  global cycle

  if counter % 2 == 0:                                                            # If the counter variable is even (e.g., brush for the first time in the day)
    print('\n')
    while True:
      if rounded > 50:                                                            # If there is nothing in front of the sensor (brush has finished)
        cycle = 0                                                                 # cycle = number of times the motor has completed a cycle of rotation (this can be set to 0 now since brush is done and nothing sensed in front of the sensor. Its purpose is to inform)
                                                                                  
        status1 = "On"
        print("Distance (raw)\tDistance (avg)\tLED 1\tLED 2\tMotor\tBuzzer")
        print(str(distance_list[-1])+'\t\t'+str(rounded)+'\t\t'+status1+'\t'+status2+'\t'+motor+'\t'+buzzer)
        led_object1.on()                                                          # TURN ON FIRST LED -- morning
        distance_list.clear()
        for i in range(5):
            distance_list = input_data()
        rounded = average_calc(distance_list)
        if hour == 0:                                                             # If midnight comes, reset all LEDs to off position (ready for new day)
          status1 = "Off"
          print("\n\nDistance (raw)\tDistance (avg)\tLED 1\tLED 2\tMotor\tBuzzer")
          print(str(distance_list[-1])+'\t\t'+str(rounded)+'\t\t'+status1+'\t'+status2+'\t'+motor+'\t'+buzzer)
          led_object1.off()
          distance_list.clear()
          counter = 0
          return

      else:                                                                        # OR if toothbrush is brought back, reset all LEDs to off position (ready for next brush)
        status1 = "Off"
        print("\n\nDistance (raw)\tDistance (avg)\tLED 1\tLED 2\tMotor\tBuzzer")
        print(str(distance_list[-1])+'\t\t'+str(rounded)+'\t\t'+status1+'\t'+status2+'\t'+motor+'\t'+buzzer)
        led_object1.off()
        distance_list.clear()
        counter += 1
        return

  else:                                                                            # If the counter variable is odd (e.g., brush for the second time in the day)
    print('\n')
    while True:
      if rounded > 50:                                                             # If there is nothing in front of the sensor (brush has finished)
        cycle = 0                                                                  # cycle = number of times the motor has completed a cycle of rotation (this can be set to 0 now since brush is done)
        status1 = "On"                                                          
        status2 = "On"
        print("Distance (raw)\tDistance (avg)\tLED 1\tLED 2\tMotor\tBuzzer")
        print(str(distance_list[-1])+'\t\t'+str(rounded)+'\t\t'+status1+'\t'+status2+'\t'+motor+'\t'+buzzer)
        led_object1.on()
        led_object2.on()                                                           # TURN ON FIRST AND SECOND LED -- night
        distance_list.clear()
        for i in range(5):
            distance_list = input_data()
        rounded = average_calc(distance_list)
        if hour == 0:                                                              # If midnight comes, reset all LEDs to off position (ready for new day)
          status1 = "Off"
          status2 = "Off"
          print("\n\nDistance (raw)\tDistance (avg)\tLED 1\tLED 2\tMotor\tBuzzer")
          print(str(distance_list[-1])+'\t\t'+str(rounded)+'\t\t'+status1+'\t'+status2+'\t'+motor+'\t'+buzzer)
          led_object1.off()
          led_object2.off()
          distance_list.clear()
          counter == 0
          return
      else:                                                                         # OR turn off LED when user returns (reminder done)
        status1 = "Off"
        status2 = "Off"
        print("\n\nDistance (raw)\tDistance (avg)\tLED 1\tLED 2\tMotor\tBuzzer")
        print(str(distance_list[-1])+'\t\t'+str(rounded)+'\t\t'+status1+'\t'+status2+'\t'+motor+'\t'+buzzer)
        led_object1.off()
        led_object2.off()
        distance_list.clear()
        counter += 1
        return

def process_2():                                                                    # tells the buzzer if it needs to run

    global status1
    global status2
    global motor
    global buzzer
    global same_count
    global rounded

    while True:

      for i in range(10):
        for j in range(2):                                                          # Find a pair of distance values 10 times
          rounded = display_average()
        if distance_list[-1] > 100:                                                 # If the most recent distance value is greater than 100 (i.e., really big)... 
                                                                                    # this means that there is actually nothing in front of the distance sensor (just wall) and buzzer code does not need to run! (return false)
          return False
        if distance_list[-2] == distance_list[-1]:                                  # If the pair of distance values is the same (something is left in front of the sensor), 
                                                                                    # increase variable by 1            
          same_count += 1
      return same_count

def process_2_output(same_count):
  
  global distance_list
  global buzzer
  global rounded
  global motor

  if same_count >= 1:                                                               # if at least 2 data points out of the last 20 in list are the same
    motor = "Off"
    buzzer = "On"
    buzzer_object.on()                                                              # turn on buzzer to notify user that something has probably been left in front of the sensor
    print('\n\n')
    
    while True:
      same_count = 0
      distance_list.clear()
      result = process_2()                                                          # continuously evaluate if distance values start varying or become really big (brush is back/object has been removed)
    
      if result == False or result == 0:                                            # if distance either becomes really big or starts varying, turn off buzzer
        break
  buzzer_object.off()
  buzzer = "Off"
  print("\n\nDistance (raw)\tDistance (avg)\tLED 1\tLED 2\tMotor\tBuzzer")
  print(str(distance_list[-1])+'\t\t'+str(rounded)+'\t\t'+status1+'\t'+status2+'\t'+motor+'\t'+buzzer)
  same_count = 0
  distance_list.clear()
  return
  
while True:
  for i in range(5):
  
    rounded = display_average()                                                    # find 5 most recent distance values and print their average
  
  while rounded > 50:                                                              # if there is nothing in front of the sensor initially, do nothing (keep on getting data and printing values)
    distance_list.clear()
    for i in range(5):
      rounded = display_average() 
  
  process_1(rounded)                                                               # squeeze toothpaste tube based on distance values and time elapsed

  if cycle >= 3:

    same_count = process_2()                                                       # initiate buzzer if squeezing cycle has occurred 3 times and at least 2 out of the last 20 distance values are the same
                                   

    process_2_output(same_count)

    cycle = 0

  for i in range(10):

    rounded = display_average()

  process_1_output(rounded)                                                        # turn on LEDs based on time of day and distance

  cycle += 1
