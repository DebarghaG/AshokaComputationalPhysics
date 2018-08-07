/* Arduino motor control with two motors attached on two ends of the L298N H-bridge
 * A secondary bluetooth module needs to be attached on the pins to control the same
 * Debargha Ganguly  Contact - maildebargha@gmail.com
 *
 * Baud rate for communication = 9600
 * Manual about how to use it :   
 *
 * Input 00 to stop both the motors through the serial input
 * Input 01 to start the first motor through the serial input
 *
 *
 *
 *
 */


#include <SoftwareSerial.h>

#define enA1 3
#define in1 5
#define in2 6

#define enA2 9
#define in3 10
#define in4 11

 unsigned int rot_direction1 = 0;
 unsigned int rot_direction2 = 0;
 unsigned int stepper_time = 3000;

void setup() {
  // put your setup code here, to run once:
  pinMode(enA1, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  pinMode(enA2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  // The pin configuration that is being written here dictates the direction of the motor
  // Feel free to change the digital write command to change the direction of the motor
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);

  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);

  //Setup for the bluetooth controller HC-05
  Serial.begin(9600); // Define baud rate for serial communication



}

void loop()
      {

            // Okay so now since there is no requirement to change the speed at which the motor is running,
            // We must set the PWM output to be the highest possible value.

            const int pwmOutput1 = 255;
            // Change this value to change the speed of rotation of the motor 1

            const int pwmOutput2 = 255;
            // Change this value to change the

            String state;




            // Writing a method to check if any input is coming in from the serial bus
            if(Serial.available() >0 ) // Checking if data is being transmitted from the bluetooth
            {
              state=Serial.read();
            }

            Serial.print(state);


            //Checks for 01 to switch on first motor
            if (state== "01")
            {
              analogWrite(enA1, pwmOutput1);
              delay(5000);

            }


            //Switches off the first motor by checking for 00
            else if (state== "00")
            {
               analogWrite(enA1, 0);
               delay(5000);

            }


            //To change the direction of the first motor
            else if (state== "11")
            {
              rot_direction1 = 1;

              //Delay

            }

            //To change the direction of the first motor
            else if (state== "00")
            {
              rot_direction1 = 0;

            }



            //To switch the pneumatic valve on
            else if (state== "02")
            {
              rot_direction2 = 0;
              if (rot_direction2 = 0)
              {
                    digitalWrite(in1, LOW);
                    digitalWrite(in2, HIGH);

              }


              analogWrite(enA2, pwmOutput2); // Starts the motor movement
              delay(stepper_time);
              analogWrite(enA2, 0); // Stops the motor after the time is done
            }

            //To switch the pneumatic valves off
            else if (state== "20")
            {
              rot_direction2= 1;
              if (rot_direction2 = 1)
              {
                    digitalWrite(in4, HIGH);
                    digitalWrite(in3, LOW);

              }
              analogWrite(enA2, pwmOutput2);// Start motor
              delay(stepper_time);
              analogWrite(enA2, 0);// Stops the motor once the time is done
            }
            state= ""; // Reseting the value of the state variable for the next loop iteration
      }
