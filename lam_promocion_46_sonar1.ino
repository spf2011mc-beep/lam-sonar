// =====================================
//  LICEO AERONÁUTICO MILITAR - PROMOCIÓN 46
//  Proyecto SONAR 2025
//  Autor: Cicolini - Franchi - Méndez - Santacroce
// =====================================

#include <Servo.h>

// Pines del HC-SR04
const int trigPin = 9;
const int echoPin = 10;

// Pines LED y buzzer
const int ledPin = 7;
const int buzzerPin = 6;

// Servo
Servo servoMotor;

// Variables
long duration;
int distance;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  servoMotor.attach(11);  // Servo en pin 3
  Serial.begin(9600);    // Comunicación con Python
}

void loop() {
  // Escaneo de 0° a 180°
  for (int angle = 0; angle <= 180; angle += 5) {
    moverYMedir(angle);
  }

  // Escaneo de 180° a 0°
  for (int angle = 180; angle >= 0; angle -= 5) {
    moverYMedir(angle);
  }
}

void moverYMedir(int angle) {
  // Mover servo
  servoMotor.write(angle);
  delay(200);

  // Medir distancia
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH, 20000); // timeout 20 ms
  distance = duration * 0.034 / 2;

  // Validar distancia
  if (distance > 0 && distance < 200) {
    // Alerta LED y buzzer
    if (distance < 20) {
      digitalWrite(ledPin, HIGH);
      digitalWrite(buzzerPin, HIGH);
    } else {
      digitalWrite(ledPin, LOW);
      digitalWrite(buzzerPin, LOW);
    }

    // Enviar datos a Python en formato "ángulo,distancia"
    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);
  }
}


