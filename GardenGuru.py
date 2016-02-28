#!/usr/bin/env python
## Console interface for the GardenGuru

import sys
import Adafruit_DHT as sensorENV
import RPi.GPIO as GPIO

sensorenv_pin = 4
pump_pin = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def menu_main():       
    print 15 * "-" , "MAIN" , 15 * "-"
    print "1. Check Sensors"
    print "2. Power Cycle the pump"
    print "3. Tweet a Message"
    print "4. Schedule a Job"
    print "5. Exit Garden Guru"
    print 34 * "-"

def menu_sensor(temp, hum):
    print
    print 13 * "=" , "SENSORS" , 13 * "="
    print "Temperature: %d F" % temp
    print "Humidity: %d%%" % hum
    print 34 * "." 
    print "1. Update Readings"
    print "2. Exit to Main Menu"
    print 34 * "="
    
def menu_power(state):
    print
    print 15 * "=" , "POWER" , 14 * "="
    if state == 0:
        print "Pump is currently OFF"
        print 15 * "=" , "POWER" , 14 * "="
        print "1. Power ON the Pump"
    elif state == 1:
        print "Pump is currently ON" 
        print "1. Power OFF the Pump"
    else:
        print "Pump state unknown! (%s)" (state)
    print "2. Exit to Main Menu"
    print 34 * "="
  
loopMain=True      
  
while loopMain:          
    menu_main()   
    choice = input("Enter your choice [1-5]: ")
     
    if choice==1:
        loopSub=True
        while loopSub: 
            humidity, temperature = sensorENV.read_retry(sensorENV.DHT11, sensorenv_pin)
            if humidity is not None and temperature is not None:
                temperature = temperature * 9/5.0 + 32    #Convert C to F
                humidity = 100 - humidity    #Convert dryness to moisture
                menu_sensor(temperature, humidity)	
                choice_sensor = input("Select an option [1-2]: ")
	        if choice_sensor==1:
                    next
                elif choice_sensor==2:
	            loopSub=False 
                else:
                    print "Invalid option." 
            else:
                print "ERROR: Unable to read sensor."
            

    elif choice==2:
        loopSub=True
        GPIO.setup(pump_pin, GPIO.OUT)
        while loopSub:
            powerState=GPIO.input(pump_pin)
            menu_power(powerState)
            choice_power = input("Select an option [1-2]: ")
            if choice_power==1 and powerState==0:
                GPIO.output(pump_pin, True)
                print "Powering the pump ON"
            elif choice_power==1 and powerState==1:
                GPIO.output(pump_pin, False)
                print "Powering the pump OFF"
            elif choice_power==2:
                GPIO.cleanup()
                loopSub=False
            else:
                print "Invalid option."

    elif choice==3:
        print "Select your message type"
        ## You can add your code or functions here

    elif choice==4:
	print "Coming soon!"

    elif choice==5:
        print "Goodbye!"
        loopMain=False 

    else:
        print "Invalid option. Enter any key to try again.."
