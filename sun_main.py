# Import necessary packages
from pymeasure.instruments.keithley import Keithley2400
import numpy as np
import pandas as pd
import time
import serial

# Define the data structure
data = []
i=0
no_data_points=20

# Configure the serial ports 
#Arduino
ser = serial.Serial('COM3', 9600, timeout=1)
response = ser.readline()
print('\n',response,'\n')
time.sleep(1)
#Connect and configure the Keithley
sourcemeter = Keithley2400("ASRL4::INSTR")
print('\n',sourcemeter.id)
sourcemeter.reset()
sourcemeter.apply_voltage(voltage_range=0,compliance_current=0.01)
sourcemeter.measure_current(nplc=1,current=0.01,auto_range=True)
time.sleep(1) # wait here to give the instrument time to react

# Loop to read and store data every second
while True:
    # Read the sensor data from the Arduino
    response = ser.readline().decode("utf-8").strip()
    print('\n',response,'\t')
    x, y, z = response.split(',')
    x = float(x)
    y = float(y)
    z = float(z)
    
    if x%(0.5)<=0.01 and i<no_data_points:
        #Make Keithley Measurements
        #use front terminals
        sourcemeter.use_front_terminals()
        sourcemeter.enable_source()
        timestamp_front = time.strftime('%Y-%m-%d %H:%M:%S')
        sourcemeter.beep(frequency=1000000,duration=0.01)
        current_measured_front=float(sourcemeter.current)
        sourcemeter.disable_source()
        time.sleep(0.01)
        #use rear terminals
        sourcemeter.use_rear_terminals()
        sourcemeter.enable_source()
        timestamp_rear = time.strftime('%Y-%m-%d %H:%M:%S')
        sourcemeter.beep(frequency=1000000,duration=0.01)
        current_measured_rear=float(sourcemeter.current)
        sourcemeter.disable_source()
        time.sleep(0.01)
        print(current_measured_front,'\t',current_measured_rear)
        #store the data with a timestamp
        data.append([x, y, z,timestamp_front,current_measured_front,timestamp_rear,current_measured_rear])
        df = pd.DataFrame(data, columns=['X', 'Y', 'Z','Timestamp Front','Short Circuit Current Front','Timestamp Rear','Short Circuit Current Rear'])
        df.to_excel("experiment_results.xlsx", index=False)
        df.to_csv("experiment_results.csv")
        i=i+1
    elif i>=200:
        ser.close()
        sourcemeter.shutdown()
        exit()
    else:
        time.sleep(0.1)

        

        
    