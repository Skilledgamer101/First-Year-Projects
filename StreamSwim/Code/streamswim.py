# imports
import time
import math
from sensor_library import *
from gpiozero import *

# class for data managment and processing
class database:

    # class attributes
    def __init__(self):

        # indexing variable and empty list
        self.i = 0
        self.dataset = [0,0,0,0,0,0,0,0,0,0]
        

        # variables for data collection
        self.sensor = Orientation_Sensor()
        self.c_v = 0
        
        self.filled = False

        # variables for standard deviation caculation
        self.base = 0
        

        self.standarddev = 0
        

        # variable for replacing random sensor values
        self.average = 0
        

        # angle breakpoints
        self.caution = 20
        self.danger = 40


        # which side the user is on
        self.right = False
        self.left = False



    # FUNCTION: takes sensor value and adds it to the current dataset

    def sense(self,sensor_value,sv2):

        # take sensor value and put it in dataset and the indexed point
        
        self.c_v = self.sensor.euler_angles()[2]

        # somtimes the sesnor returns none, this replaces that value with the average of the dataset
        if self.c_v == None:
            total = 0

            # add total of list
            for j in range(0, len(self.dataset)):
                total += self.dataset[j]

            # get the average and set the result to it
            self.average = total / len(self.dataset)
            self.c_v = self.average

        self.dataset[self.i] = self.c_v
        


        # index control and checking to see if the list is full
        if self.i == 9:
            self.filled = True
        self.i+= 1

        if self.i == 10:
            self.i = 0

        # outputs for user reading/error checking
        return self.c_v

    # FUNCTION allows us to set the base angle
    def setbase(self):

        #Sets base angle and returns it
        self.base = self.c_v
        return self.base

    # FUNCTION caculates the standard devation of the current dataset if the list is filled
    def standdev_calc(self):

        # check to make sure the list is full
        if self.filled == True:

            # calculates the standard deviation and returns it
            totaldev = 0
            for j in range(0, len(self.dataset)):
                totaldev += (abs(self.dataset[j]-self.base))**2
            self.standarddev = math.sqrt((totaldev/len(self.dataset)))
            return self.standarddev

        # returns none if the list is not full
        else:
            return None

    # FUNCTION checks if user is in the caution zone and returns true or false
    def cautioncheck(self):

        # checks to see if the user is above the caution threshold but dosen't enter the danger threshold 
        if (self.standarddev >= self.caution and self.standarddev <= self.danger):

            # returns boolean to be used for outputs
            return True
        else:
             # returns boolean to be used for outputs
            return False

    # FUNCTION checks if user is in the danger zone and returns true or false
    def dangercheck(self):

        # checks to see if user is above the danger zone threshold and returns a boolean for output devices to use
        if (self.standarddev >= self.danger) :
            return True
        else:
            return False

    # FUNCTION returns which side david is leaning too far towards
    def sidecheck(self):

        # gets sum of the list
        totalamount =0
        for j in range(0, len(self.dataset)):
            totalamount += (self.dataset[j])

        # if the list total is postive it indicates the sensor is likely on the right side 
        if totalamount >= 0:
            self.right = True
            self.left = False

        # not right = Left
        else:
            self.right = False
            self.left = True

        # returns the status of left and right for ourput devices
        return self.right, self.left


# intalizing instances of all applicable classes including the above class and output devices
hello = database()
vibration_left = Buzzer(9)
vibration_right = Buzzer(13)
buzzer_left = Buzzer(27)
buzzer_right = Buzzer(26)

# FUNCTION: initiates vibration on the side David tilts too much on
def vibration():

    # initialize applicable instances of above class
    
    danger = hello.dangercheck()
    caution = hello.cautioncheck()
    sides = hello.sidecheck()

    # if user is tilting to right
    if sides [0] == True:
        
        # if tilt is slight activate output devices with lower intensity
        
        if caution == True:         
            vibration_right.on()
            vibration_left.off()
            
            buzzer_right.on()
            time.sleep(0.15)
            
            buzzer_right.off()
            vibration_right.off()

        # if tilt is severe activate output devices with higher intensity
        elif danger == True:
            vibration_right.on()
            vibration_left.off()
            buzzer_right.on()
            time.sleep(0.05)
            buzzer_right.off()

        # if neither danger or caution are true deactivate all devices
        
        else:
            vibration_right.off()
            vibration_left.off()
            buzzer_right.off()

    # if user is tilting to left

    else:

        # if tilt is slight activate output devices with lower intensity    

        if caution == True:
            vibration_left.on()
            
            buzzer_left.on()
            time.sleep(0.15)
            
            buzzer_left.off()
            vibration_right.off()
            
            vibration_left.off()


        # if tilt is severe activate output devices with higher intensity

        
        elif danger == True:
            buzzer_left.on()
            vibration_left.on()
            time.sleep(0.05)
            buzzer_left.off()
            vibration_right.off()
            
        # if neither danger or caution are true deactivate all devices

        else:
            vibration_left.off()
            vibration_right.off()
            buzzer_left.off()
        

    return None


# FUNCTION: main function, runs code
def main():

    # sense the current sensor orientation and set a base value
    start =hello.sense(0,0)
    hello.setbase()

    # while the device is on
    while True:

        # sense data and check sides
        test = 0
        test2 = 0
        sensey =hello.sense(test,test2)

        stdevcalc = hello.standdev_calc()
    
        caution_t = hello.cautioncheck()
    
        danger_t = hello.dangercheck()

        R_or_L = hello.sidecheck()

        # perform outputs
        vibration()

# main call
main()


