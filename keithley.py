# Import necessary packages
from pymeasure.instruments.keithley import Keithley2400
import numpy as np
import pandas as pd
import time

#define data structure
data =[]
i=0
no_data_points=10;

# Connect and configure the instrument
sourcemeter = Keithley2400("ASRL4::INSTR")
print('\n',sourcemeter.id)
sourcemeter.reset()
sourcemeter.apply_voltage(voltage_range=0,compliance_current=0.01)
sourcemeter.measure_current(nplc=1,current=0.01,auto_range=True)
time.sleep(0.1) # wait here to give the instrument time to react
#  measure and record the current
while True:
    if i<no_data_points:
        #use front terminals
        sourcemeter.use_front_terminals()
        sourcemeter.enable_source()
        timestamp_front = time.strftime('%Y-%m-%d %H:%M:%S')
        current_measured_front=float(sourcemeter.current)
        sourcemeter.disable_source()
        sourcemeter.beep(frequency=1000000,duration=0.01)
        time.sleep(0.01)
        #use rear terminals
        sourcemeter.use_rear_terminals()
        sourcemeter.enable_source()
        timestamp_rear = time.strftime('%Y-%m-%d %H:%M:%S')
        current_measured_rear=float(sourcemeter.current)
        sourcemeter.disable_source()
        sourcemeter.beep(frequency=1000,duration=0.01)
        time.sleep(0.01)
        #Record 
        data.append([timestamp_front,current_measured_front,timestamp_rear,current_measured_rear])
        # data.append([timestamp_front,current_measured_front])
        i=i+1;
    else:
        sourcemeter.shutdown()
        df=pd.DataFrame(data, columns=['Timestamp Front','Short Circuit Current Front','Timestamp Rear','Short Circuit Current Rear'])
        # df=pd.DataFrame(data, columns=['Timestamp Front','Short Circuit Current Front'])
        df.to_excel("keithley_data.xlsx",index=False)
        exit()