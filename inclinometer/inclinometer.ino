#include <SPI.h>
#include <SCL3300.h>
#include <math.h>
#include <SimpleKalmanFilter.h>

SCL3300 inclinometer;
SimpleKalmanFilter kf(0.02, 0.02, 0.01);

double RawXAng, RawYAng, RawZAng, Tilt, Tilt_prev, Tilt_delta, filteredTilt = 0.00;
double dt=0.05;
int flag=0;

// Serial output refresh time
const long SERIAL_REFRESH_TIME = 100;
long refresh_time;

// Need the following define for SAMD processors
#if defined(ARDUINO_SAMD_ZERO) && defined(SERIAL_PORT_USBVIRTUAL)
#define Serial SERIAL_PORT_USBVIRTUAL
#endif

void printDouble( double val, int precision){
  // prints val with number of decimal places determine by precision
  // NOTE: precision is 1 followed by the number of zeros for the desired number of decimial places
  // example: printDouble( 3.1415, 100); // prints 3.14 (two decimal places)
  if(val>-1 && val<0) 
    Serial.print("-");
  
  Serial.print (int(val)); //prints the int part
  Serial.print("."); // print the decimal point
  
  int frac;
  if(val >= 0) 
    frac = (val - int(val)) * precision;
  else 
    frac = (int(val)- val ) * precision;
  Serial.print(frac) ;
}

void setup() {
  Serial.begin(9600);
  delay(2000); //SAMD boards may need a long time to init SerialUSB
  Serial.println("Reading Raw register values from SCL3300 Inclinometer");
  if (inclinometer.begin() == false) {
    Serial.println("Murata SCL3300 inclinometer not connected.");
    while(1); //Freeze
  }
  inclinometer.setMode(4);

}

void loop() {
  if (inclinometer.available()) {
    //Get Tilt readings
    RawXAng=((inclinometer.sclData.AngX)/ 16384.00)*90.00;
    RawYAng=((inclinometer.sclData.AngY)/ 16384.00)*90.00;
    RawZAng=((inclinometer.sclData.AngZ)/ 16384.00)*90.00;

    // //Get acceleration readings
    // double RawXAcc=(inclinometer.sclData.AccX)/12000.00;
    double RawYAcc=(inclinometer.sclData.AccY)/12000.00;
    double RawZAcc=(inclinometer.sclData.AccZ)/12000.00;
    double Tilt=(180.00-(acos(RawZAcc/(pow((pow(RawYAcc,2.00)+pow(RawZAcc,2.00)),0.5))))*(180.00/M_PI));
    if (RawYAcc>=0)
      Tilt=360.00-Tilt;
    
    Tilt_delta=Tilt_prev-Tilt;

    if(Tilt_delta>300 || Tilt==0 || filteredTilt==0)
      flag=0;

    // filteredXAng=kf.updateEstimate(RawXAng);
    // filteredYAng=kf.updateEstimate(RawYAng);
    // filteredZAng=kf.updateEstimate(RawZAng);

     // calculate Tilt 
    // if(filteredYAng<=0 && filteredYAng>-90 && filteredZAng>=-90 && filteredZAng<0) 
    //   Tilt= (-RawYAng); 
    // else if(filteredYAng>=-90 && filteredYAng<0 && filteredZAng>=0 && filteredZAng<90) 
    //   Tilt= (RawYAng+180); 
    // else if(filteredYAng>=0 && filteredYAng<90 && filteredZAng<=90 && filteredZAng>0) 
    //   Tilt=(RawYAng+180); 
    // else if(filteredYAng<=90 && filteredYAng>0 && filteredZAng<=0 && filteredZAng>-90 ) 
    //   Tilt=(360-RawYAng);
    // if(RawYAng<=0)
    //   Tilt=(-RawYAng);
    // else if(RawYAng>0)
    //   Tilt=(360-RawYAng);

    // Calculate Tilt
    if (flag==1)
      filteredTilt = kf.updateEstimate(Tilt);
    else if (flag==0){
      filteredTilt=kf.resetKalman(Tilt, 0.02, 0.02, 0.01);
      flag=1;
    }


    // Print stuff
    // Serial.print("Tilt: ");
    // printDouble(Tilt,10000);
    // Serial.print(", ");

    Tilt_prev=Tilt;
    Serial.print(filteredTilt);
    Serial.print(",");
    Serial.print(RawXAng);
    Serial.print(",");
    Serial.print(RawYAng);
    Serial.print(",");
    Serial.print(RawZAng);
    Serial.println("");

    delay(100); 
 
  } else {
    inclinometer.reset();
  }
}
