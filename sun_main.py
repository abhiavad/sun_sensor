# Import necessary packages
from pymeasure.instruments.keithley import Keithley2400
import numpy as np
import pandas as pd
import time
import serial
# import matplotlib.pyplot as plt

# Define the data structure
data = []
i=0 #number of readings taken
j=0 #number of readings at current angle
no_tot_readings=10000
no_ang_readings=5

I_o=0.00587 #Io value in A (short circuit current at 0 degrees, check and set it before testing)

# Configure the serial ports 
#Arduino
ser = serial.Serial('COM3', 9600, timeout=1) #Check this at device manager and set it accordingly 
response = ser.readline()
print('\n',response)
time.sleep(1)

def getLatestAngles():
    while ser.inWaiting() > 0:
        Angles = ser.readline()
    else:
        Angles = ser.readline()
    return Angles
    

    
#Connect and configure the Keithley
sourcemeter = Keithley2400("ASRL5::INSTR") #Check this at device manager and set it accordingly 
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
    Tilt, x, y, z = Angles.split(',')
    Tilt=float(Tilt)
    x = float(x)
    y = float(y)
    z = float(z)

    if (Tilt%(0.5)>=0.45 or Tilt%(0.5)<=0.05) and i<no_tot_readings and j<no_ang_readings: 
        #rn this is set at 0.05 degrees above or below 0.5 degrees increments
        i=i+1
        j=j+1

        #Timestamp
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        
        #Make Keithley Measurements
        #use front terminals for primary cell
        sourcemeter.use_front_terminals()
        sourcemeter.enable_source()
        sourcemeter.beep(frequency=1000,duration=0.01)
        time.sleep(0.5)
        current_measured_front=float(sourcemeter.current)
        sourcemeter.disable_source()

        #use rear terminals for redundant cell
        sourcemeter.use_rear_terminals()
        sourcemeter.enable_source()
        sourcemeter.beep(frequency=1000,duration=0.01)
        time.sleep(0.5)
        current_measured_rear=float(sourcemeter.current)
        sourcemeter.disable_source()
        
        #calculate expected current using Io value
        current_expected = I_o*np.cos(Tilt*np.pi/180.00)

        #Print for refernce
        print('\nTilt:',Tilt,', x:',x,', y:',y,', z:',z,', i:',i,', j:',j,', time:',timestamp,', cur_frnt:',current_measured_front,', cur_bck:',current_measured_rear,', cur_exp:',current_expected)
        #store the data with a timestamp
        data.append([Tilt,x,y,z,timestamp,current_measured_front,current_measured_rear,current_expected])
        df = pd.DataFrame(data, columns=['Tilt (deg.)','x (deg.)','y (deg.)','z (deg.)','Timestamp','Short Circuit Current Primary (A)','Short Circuit Current Redundant (A)','Current Expected (A)'])
        
        #RESET THIS AFTER EVERY SET OF READINGS TO NOT OVERWRITE PREVIOUS READINGS
        df.to_excel(".\Results\May30_2023_ADN01_AxisA_1.xlsx", index=False) 
        df.to_csv(".\Results\May30_2023_ADN01_AxisA_1.csv")
        
        # df.plot(x='Y',y=['Short Circuit Current Front', 'Short Circuit Current Rear','Current Expected'],title="Current(A) vs Angle(deg)", xlabel="Angle(deg)", ylabel="Current (A)", legend=(['Short Circuit Current Front', 'Short Circuit Current Rear','Current Expected']))
    
    elif i>=no_tot_readings:
        ser.close()
        sourcemeter.shutdown()
        exit()
    elif j>=no_ang_readings:
        sourcemeter.beep(frequency=2000,duration=1)
        time.sleep(2)
        j=0
    else:
        print('\nTilt', Tilt,', x:',x,', y:',y,', z:',z,', i:',', i:',i,', j:',j)
        time.sleep(0.1)
        j=0

        

        
    