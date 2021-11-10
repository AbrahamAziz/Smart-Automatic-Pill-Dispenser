from bs4 import BeautifulSoup
import RPi.GPIO as GPIO
import requests
import datetime
import serial
import time
import os
import subprocess



# Setting up the pins for the motors
GPIO.setmode(GPIO.BOARD)

# Which GPIO pin to which motor

Servo1Pin = 13
Servo2Pin = 11
Servo3Pin = 12


# Specify them as outputs

GPIO.setup(Servo1Pin, GPIO.OUT)
GPIO.setup(Servo2Pin, GPIO.OUT)
GPIO.setup(Servo3Pin, GPIO.OUT)


Servo1 = GPIO.PWM(Servo1Pin, 50)
Servo2 = GPIO.PWM(Servo2Pin, 50)
Servo3 = GPIO.PWM(Servo3Pin, 50)


# Turn everything off
Servo1.start(0)
Servo2.start(0)
Servo3.start(0)


# We in this for the long haul
while True:

    pill1_hour_list = []
    pill1_minute_list = []
    pill1_numpills = []

    pill2_hour_list = []
    pill2_minute_list = []
    pill2_numpills = []

    pill3_hour_list = []
    pill3_minute_list = []
    pill3_numpills = []

   
    # Get the website data from the URL
    r = requests.get("http://0.0.0.0:80")

    # Grab and transcribe the raw html using Beautiful Soup
    data = r.content
    page_soup = BeautifulSoup(data, "html.parser")

    # Find and store all the time elements on the web page
    pill1 = page_soup.findAll("td", {"class": "pill1Time"})
    pill2 = page_soup.findAll("td", {"class": "pill2Time"})
    pill3 = page_soup.findAll("td", {"class": "pill3Time"})
  
    numpill1 = page_soup.findAll("td", {"class": "pill1num"})
    numpill2 = page_soup.findAll("td", {"class": "pill2num"})
    numpill3 = page_soup.findAll("td", {"class": "pill3num"})
 

    # Loop through all elements in the list of pill times and store them in lists
    for x in range(len(pill1)):
        # Add the number of pills in the list
        pill1_numpills.append(int(numpill1[x].text))

        # Split the pill times into hours and minutes and add to respective lists
        this_time = pill1[x].text.split()
        pill1_hour_list.append(this_time[0])
        pill1_minute_list.append(this_time[2])

    for x in range(len(pill2)):
        # Add the number of pills in the list
        pill2_numpills.append(int(numpill2[x].text))

        # Split the pill times into hours and minutes and add to respective lists
        this_time = pill2[x].text.split()
        pill2_hour_list.append(this_time[0])
        pill2_minute_list.append(this_time[2])

    for x in range(len(pill3)):
        # Add the number of pills in the list
        pill3_numpills.append(int(numpill3[x].text))

        # Split the pill times into hours and minutes and add to respective lists
        this_time = pill3[x].text.split()
        pill3_hour_list.append(this_time[0])
        pill3_minute_list.append(this_time[2])

    
    # Update the current time
    now = datetime.datetime.now()
    print(now)
    sleep = 0
   

    STEPS = 10  # the number of steps either side of nominal
    NOMINAL = 8.5  # the 'zero' PWM %age
    RANGE = 1.0  # the maximum variation %age above/below NOMINAL

    for x in range(len(pill1_hour_list)):
        # Compare the current hour to the hour in the list and the current minute to the minute in the list
        if now.hour == int(pill1_hour_list[x]) and now.minute == int(pill1_minute_list[x]):
            dutycycle = NOMINAL + (-1) * .5 * 20 / 10
            Servo1.ChangeDutyCycle(dutycycle)
            sleep += pill1_numpills[x] * 2.1
            time.sleep(pill1_numpills[x] * 2.1)
            Servo1.ChangeDutyCycle(0)
            # Allows you to see it actually working
            print("Dispensing Pill")
           

    for x in range(len(pill2_hour_list)):
        # Compare the current hour to the hour in the list and the current minute to the minute in the list
        if now.hour == int(pill2_hour_list[x]) and now.minute == int(pill2_minute_list[x]):
            dutycycle = NOMINAL + (-1) * .5 * 20 / 10
            Servo2.ChangeDutyCycle(dutycycle)
            sleep += pill2_numpills[x] * 1.6
            time.sleep(pill2_numpills[x] * 1.6)
            Servo2.ChangeDutyCycle(0)
            # Allows you to see it actually working
            print("Dispensing Pill")
            

    for x in range(len(pill3_hour_list)):
        # Compare the current hour to the hour in the list and the current minute to the minute in the list
        if now.hour == int(pill3_hour_list[x]) and now.minute == int(pill3_minute_list[x]):
            dutycycle = NOMINAL + (-1) * .5 * 20 / 10
            Servo3.ChangeDutyCycle(dutycycle)
            sleep += pill3_numpills[x] * 1.9
            time.sleep(pill3_numpills[x] * 1.9)
            Servo3.ChangeDutyCycle(0)
            # Allows you to see it actually working
            print("Dispensing Pill")
            

    

    # This is dependent on how fast the machine is. For us it would generally take a second to run through the code
    time.sleep(60 - sleep)