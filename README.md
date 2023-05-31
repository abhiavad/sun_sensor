# sun_sensor
keithley and inclinometer automated (thermistor to be added)

Install Arduino IDE and download the following libraries: 
1) https://github.com/denyssene/SimpleKalmanFilter
2) https://github.com/DavidArmstrong/SCL3300
3) https://www.arduino.cc/reference/en/libraries/sd/

Upload the inclinometer sketch to the arduino and make connections by referring the images included below:

![SLC3300](./references/SCL3300.png)
![Arduino_mega](./references/Arduino_mega.jpeg)  

Connect the sourcemeter to the laptop using rs-232 to usb cable. 
Connect the front and back input/outpt of the sourcemeter to 9 pin test jig by referring the following image: 

![PCB](./references/pcb.jpg)

make a virtual environment as per requirements.txt and run the sun_main.py code
