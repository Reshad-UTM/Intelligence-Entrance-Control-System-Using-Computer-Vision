#include <Servo.h>

// Define the pin connected to the servo signal wire
const int servoPin = 8;
// Define the pin connected to the IR sensor output
const int irSensorPin = 11;

// Create a servo object
Servo servo;

// Define the command characters
const char openGateCmd = '1';
const char closeGateCmd = '0';

void setup() {
  // Attach the servo to the specified pin
  servo.attach(servoPin);

  // Set the initial position of the servo (closed gate position)
  servo.write(0);

  // Start the serial communication
  Serial.begin(9600);

  // Set the IR sensor pin as input
  pinMode(irSensorPin, INPUT);
}

void loop() {
  // Check if there is data available to read
  if (Serial.available() > 0) {
    // Read the incoming command
    char command = Serial.read();

    // Process the command
    if (command == openGateCmd) {
      openGate();
    } else if (command == closeGateCmd) {
      closeGate();
    }
  }

  // Check the IR sensor input
  if (digitalRead(irSensorPin) == HIGH) {
    // Car detected, send signal to close the gate
    closeGate();
  }
}

void openGate() {
  // Set the servo position to open the gate
  servo.write(90);
}

void closeGate() {
  // Set the servo position to close the gate
  servo.write(0);
}
