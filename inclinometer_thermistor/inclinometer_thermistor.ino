/* Read Tilt angles from Murata SCL3300 Inclinometer
 * Version 3.2.0 - September 3, 2021
 * Example2_BasicTiltReading
*/

#include <SPI.h>
#include <SCL3300.h>

SCL3300 inclinometer;
//Default SPI chip/slave select pin is D53

// Need the following define for SAMD processors
#if defined(ARDUINO_SAMD_ZERO) && defined(SERIAL_PORT_USBVIRTUAL)
  #define Serial SERIAL_PORT_USBVIRTUAL
#endif

void setup() {
  Serial.begin(9600);
  delay(2000); //SAMD boards may need a long time to init SerialUSB
  if (inclinometer.begin() == false) {
    Serial.println("Murata SCL3300 inclinometer not connected.");
    while(1); //Freeze
  }
  
}

void loop() {
  if (inclinometer.available()) { //Get next block of data from sensor
    Serial.print(inclinometer.getCalculatedAngleX());
    Serial.print(",");
    Serial.print(inclinometer.getCalculatedAngleY());
    Serial.print(",");
    Serial.println(inclinometer.getCalculatedAngleZ());
    delay(10); //Allow a little time to see the output
  } else inclinometer.reset();
}
