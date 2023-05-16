# Import necessary packages
from pymeasure.instruments.keithley import Keithley2400
import numpy as np
import pandas as pd
import time
import serial
# import matplotlib.pyplot as plt

# Define the data structure
data = []
i=0
j=0
no_tot_readings=10000
no_ang_readings=10

I_o=0.01 #Io value in A

# Configure the serial ports 
#Arduino
ser = serial.Serial('COM6', 9600, timeout=1)
response = ser.readline()
print('\n',response)
time.sleep(1)

def getLatestAngles():
    while ser.inWaiting() > 0:
        Angles = ser.readline()
    return Angles
    
#Connect and configure the Keithley
sourcemeter = Keithley2400("ASRL4::INSTR")
print('\n',sourcemeter.id)
sourcemeter.reset()
sourcemeter.apply_voltage(voltage_range=0,compliance_current=0.01)
sourcemeter.measure_current(nplc=1,current=0.01,auto_range=True)
time.sleep(1) # wait here to give the instrument time to react
sourcemeter.beep(frequency=100000,duration=1)

# Loop 
while True:
    # Read the sensor data from the Arduino
    Angles = getLatestAngles().decode("utf-8").strip()
    x, y, z = Angles.split(',')
    x = float(x)
    y = float(y)
    z = float(z)
    
    if (y%(0.5)>=0.4 or y%(0.5)<=0.1) and i<no_tot_readings and j<no_ang_readings:
        
        #Timestamp
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        
        #Make Keithley Measurements
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
        current_measured_rear=float(sourcemeter.current)
        sourcemeter.disable_source()
        time.sleep(0.1)

        #calculate expected current
        current_expected = I_o*np.cos(y*np.pi/180.00)

        #Print for refernce
        print('\nx:',x,', y:', y,', z:', z,', i:',i,', j:',j,', time:',timestamp,', cur_frnt:',current_measured_front,', cur_bck:',current_measured_rear,', cur_exp:',current_expected)
        #store the data with a timestamp
        data.append([x, y, z,timestamp,current_measured_front,current_measured_rear,current_expected])
        df = pd.DataFrame(data, columns=['X', 'Y', 'Z','Timestamp','Short Circuit Current Front','Short Circuit Current Rear','Current Expected'])
        df.to_excel("experiment_results.xlsx", index=False)
        df.to_csv("experiment_results.csv")
        i=i+1
        j=j+1
        # df.plot(x='Y',y=['Short Circuit Current Front', 'Short Circuit Current Rear','Current Expected'],title="Current(A) vs Angle(deg)", xlabel="Angle(deg)", ylabel="Current (A)", legend=(['Short Circuit Current Front', 'Short Circuit Current Rear','Current Expected']))
    
    elif i>=no_tot_readings:
        ser.close()
        sourcemeter.shutdown()
        exit()
    elif j>=no_ang_readings:
        sourcemeter.beep(frequency=2000,duration=1)
        time.sleep(1)
        j=0
    else:
        print('\nx:',x,', y:', y,', z:', z,', i:',i,', j:',j)
        time.sleep(0.1)

        

        
    