#include <SPI.h>
#include <Kalman.h>
#include <SCL3300.h>

Kalman kalmanX;  // Kalman filter for tilt along the X-axis
Kalman kalmanY;  // Kalman filter for tilt along the Y-axis
float kalmanXAngle;
float kalmanYAngle;
float angle_now_x=0;
float angle_prev_x=0;
float angle_now_y =0;
float angle_prev_y=0;
SCL3300 scl3300;


// Need the following define for SAMD processors
#if defined(ARDUINO_SAMD_ZERO) && defined(SERIAL_PORT_USBVIRTUAL)
#define Serial SERIAL_PORT_USBVIRTUAL
#endif

void setup() {
  Serial.begin(9600);
  delay(2000);  //SAMD boards may need a long time to init SerialUSB

  if (scl3300.begin() == false) {
    Serial.println("Murata SCL3300 inclinometer not connected.");
    while (1);
      }  //Freeze
  

  // Initialize the Kalman filters
  kalmanX.setAngle(scl3300.getCalculatedAngleX());
  kalmanY.setAngle(scl3300.getCalculatedAngleY());
  angle_now_x=scl3300.getCalculatedAngleX();
  angle_prev_x=scl3300.getCalculatedAngleX();
  angle_now_y =scl3300.getCalculatedAngleY();
  angle_prev_y=scl3300.getCalculatedAngleY();
}

void loop() {
if (scl3300.available()){
  angle_now_x=scl3300.getCalculatedAngleX();
  angle_now_y=scl3300.getCalculatedAngleY();

  // Update the Kalman filters with the tilt readings
  kalmanXAngle = kalmanX.getAngle(scl3300.getCalculatedAngleX(), (angle_prev_x-angle_now_x)/1, 1);
  kalmanYAngle = kalmanY.getAngle(scl3300.getCalculatedAngleY(), (angle_prev_y-angle_now_y)/1, 1);

  // Print the tilt angles
  Serial.print("Tilt X: ");
  Serial.print(kalmanXAngle);
  Serial.print(" degrees\t");

  Serial.print("Tilt Y: ");
  Serial.print(kalmanYAngle);
  Serial.println(" degrees");
  angle_prev_x=angle_now_x;
  angle_prev_y=angle_now_y;

  delay(1000);  // Adjust the delay as necessary
}
else scl3300.reset();
}
