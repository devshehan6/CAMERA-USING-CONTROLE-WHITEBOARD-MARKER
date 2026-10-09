#include <AccelStepper.h>
#include <Servo.h>

const int X_STEP_PIN = 2;
const int X_DIR_PIN = 5;
const int Y_STEP_PIN = 3;
const int Y_DIR_PIN = 6;
const int PEN_SERVO_PIN = 9;
const int PEN_UP_ANGLE = 80;
const int PEN_DOWN_ANGLE = 115;

AccelStepper xAxis(AccelStepper::DRIVER, X_STEP_PIN, X_DIR_PIN);
AccelStepper yAxis(AccelStepper::DRIVER, Y_STEP_PIN, Y_DIR_PIN);
Servo penServo;
String commandBuffer;

void setup() {
  Serial.begin(115200);
  xAxis.setMaxSpeed(1200);
  xAxis.setAcceleration(600);
  yAxis.setMaxSpeed(1200);
  yAxis.setAcceleration(600);
  penServo.attach(PEN_SERVO_PIN);
  penServo.write(PEN_UP_ANGLE);
}

void loop() {
  while (Serial.available() > 0) {
    char incoming = static_cast<char>(Serial.read());
    if (incoming == '\n') {
      handleCommand(commandBuffer);
      commandBuffer = "";
    } else if (incoming != '\r' && commandBuffer.length() < 80) {
      commandBuffer += incoming;
    }
  }
  xAxis.run();
  yAxis.run();
}

void handleCommand(String command) {
  command.trim();
  if (command.startsWith("MOVE ")) {
    long xTarget;
    long yTarget;
    if (sscanf(command.c_str(), "MOVE %ld %ld", &xTarget, &yTarget) == 2) {
      xAxis.moveTo(xTarget);
      yAxis.moveTo(yTarget);
      Serial.println("OK");
      return;
    }
  } else if (command == "PEN 0") {
    penServo.write(PEN_UP_ANGLE);
    Serial.println("OK");
    return;
  } else if (command == "PEN 1") {
    penServo.write(PEN_DOWN_ANGLE);
    Serial.println("OK");
    return;
  }
  Serial.println("ERR");
}