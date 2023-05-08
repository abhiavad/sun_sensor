import time
import pandas as pd
import serial

# Define the data structure
data = []
i=0

# Configure the serial ports 
#Arduino
ser = serial.Serial('COM3', 9600, timeout=1)

# Loop to read and store data every second
while True:
    if i==0:
         # Get the current time
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        # Read the sensor data from the Arduino
        ser.write(b'r\n')
        response = ser.readline()
        print('\n',response,'\n')

        time.sleep(1)
        i=i+1
    else:
        # Get the current timeww
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        # Read the sensor data from the Arduino
        #ser.write(b'r\n')
        response = ser.readline().decode("utf-8").strip()
        print('\n',response,'\n')
        x, y, z = response.split(',')
        x = float(x)
        y = float(y)
        z = float(z)
        
        i=i+1;

        if x%(0.5)<=0.01 and i<200:
            #store the data with a timestamp
             data.append([timestamp, x, y, z])
             # Wait for 10 milliseconds before the next reading
             time.sleep(0.01)
        elif i>=200:
            # Save the data to an Excel file
            df = pd.DataFrame(data, columns=['Timestamp', 'X', 'Y', 'Z'])
            df.to_excel("sensor_data.xlsx", index=False)
            ser.close()
            exit()