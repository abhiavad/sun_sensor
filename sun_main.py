import time
import pandas as pd
import serial

# Configure the serial port
ser = serial.Serial('COM3', 9600, timeout=1)

# Define the data structure
data = []
i=0;
# Loop to read and store data every second
while True:
    # Get the current time
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    # Read the sensor data from the Arduino
    ser.write(b'r')
    response = ser.readline().decode().strip()
    x, y, z = response.split(',')
    x = float(x)
    y = float(y)
    z = float(z)

    #store the data with a timestamp
    data.append([timestamp, x, y, z])

    # Wait for 10 milliseconds before the next reading
    time.sleep(0.01)
    i+=1
    if x%(0.5)<=0.01 and i<50000:
        # Save the data to an Excel file
        df = pd.DataFrame(data, columns=['Timestamp', 'X', 'Y', 'Z'])
        df.to_excel('sensor_data.xlsx', index=False)

    

    
    