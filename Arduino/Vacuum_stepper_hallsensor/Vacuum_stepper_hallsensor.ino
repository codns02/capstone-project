#include <AccelStepper.h>

// 핀 설정
const int pumpPin = 8;
const int hallPin = A1;
const int transPul = 25;
const int transDir = 26;

AccelStepper stepper(1, transPul, transDir);
bool motorRunning = false;    

unsigned long lastTime = 0;
bool lastStatus = 0;

void setup() {
  Serial.begin(115200);
  pinMode(pumpPin, OUTPUT);
  digitalWrite(pumpPin, LOW); 
  
  stepper.setMaxSpeed(5000);
  stepper.setAcceleration(200);
  
  Serial.println("--- 시스템 통합 제어 시작 ---");
}

void loop() {
  // 1. 모터 구동
  if (motorRunning) {
    stepper.run();
    if (stepper.distanceToGo() < 1000) {
      stepper.moveTo(stepper.currentPosition() + 2000000000L);
    }
  } else {
    stepper.stop();
  }

  // 2. 시리얼 입력 (제어)
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == '1') { digitalWrite(pumpPin, HIGH); Serial.println("펌프 ON"); }
    else if (cmd == '0') { digitalWrite(pumpPin, LOW); Serial.println("펌프 OFF"); }
    else if (cmd == 'r') { motorRunning = true; stepper.moveTo(stepper.currentPosition() + 2000000000L); Serial.println("모터 회전"); }
    else if (cmd == 's') { motorRunning = false; Serial.println("모터 정지"); }
  }

  // 3. 센서 테스트 로직
  int hallValue = analogRead(hallPin);
  
  // 판정 기준값 (44로 수정)
  int currentStatus = (hallValue < 44) ? 1 : 0;

  // [확인용] 현재 상태 실시간 출력 (Status가 0과 1로 바뀌는지 확인하세요)
  static unsigned long lastStatusPrint = 0;
  if (millis() - lastStatusPrint > 500) {
    Serial.print("Status: ");
    Serial.print(currentStatus);
    Serial.print(" | Raw Value: ");
    Serial.println(hallValue);
    lastStatusPrint = millis();
  }

  // RPM 측정 로직
  if (currentStatus == 1 && lastStatus == 0) {
    unsigned long currentTime = millis();
    if (currentTime - lastTime > 50) { 
      float rpm = 60000.0 / (currentTime - lastTime);
      Serial.print(">>> 감지됨! RPM: ");
      Serial.println(rpm);
    }
    lastTime = currentTime;
  }
  lastStatus = currentStatus;
}