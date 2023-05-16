# Import necessary packages
from pymeasure.instruments.keithley import Keithley2400
import numpy as np
import pandas as pd
import time
import serial


#define data structure
data =[]
i=0
no_data_points=10;

# Connect and configure the instrument
#Arduino
ser = serial.Serial('COM6', 9600, timeout=1)
response = ser.readline()
print('\n',response)
time.sleep(1)

def getLatestAngles():
    while ser.inWaiting() > 0:
        Angles = ser.readline()
    return Angles
    
#Keithley
sourcemeter = Keithley2400("ASRL4::INSTR")
print('\n',sourcemeter.id)
sourcemeter.reset()
sourcemeter.apply_voltage(voltage_range=0,compliance_current=0.01)
sourcemeter.measure_current(nplc=1,current=0.01,auto_range=True)
sourcemeter.beep(frequency=100000,duration=1)
time.sleep(1) # wait here to give the instrument time to react

#  measure and record the current
while True:
    if i<no_data_points:
        #Timestamp
        timestamp=time.strftime('%Y-%m-%d %H:%M:%S')

        # Read the sensor data from the Arduino
        response = getLatestAngles().decode("utf-8").strip()
        x, y, z = response.split(',')
        x = float(x)
        y = float(y)
        z = float(z)

        #Keithley
        #use front terminals
        sourcemeter.use_front_terminals()
        sourcemeter.enable_source()
        sourcemeter.beep(frequency=1000,duration=0.01)
        time.sleep(0.1)
        current_measured_front=float(sourcemeter.current)
        sourcemeter.disable_source()

        #use rear terminals
        sourcemeter.use_rear_terminals()
        sourcemeter.enable_source()
        sourcemeter.beep(frequency=1000,duration=0.01)
        time.sleep(0.1)
        current_measured_rear=float(sourcemeter.current)
        sourcemeter.disable_source()
        
        # Print
        print('\nTime:',timestamp,', Angle(x):',x, ', Angle(y):',y, ', Angle(z):',z,', cur_frnt:',current_measured_front,', cur_bck',current_measured_rear)
        time.sleep(5)
        i=i+1
    else:
        ser.close()
        sourcemeter.shutdown()
        exit()