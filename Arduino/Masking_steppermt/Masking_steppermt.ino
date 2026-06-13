#include <AccelStepper.h>

const int transPul = 28;
const int transDir = 29;

const long STEPS_PER_90DEG = 200; 
const float MY_SPEED = 300.0;

AccelStepper stepper(1, transPul, transDir);

void setup() {
  Serial.begin(115200); // 시리얼 통신 시작
  stepper.setMaxSpeed(MY_SPEED);
  stepper.setAcceleration(999999.0);
  stepper.setCurrentPosition(0);
  
  Serial.println("--- 스텝 모터 제어 시작 ---");
  Serial.println("숫자 '1'을 입력하고 엔터를 치면 90도 회전합니다.");
}

void loop() {
  // 시리얼 데이터가 들어왔는지 확인
  if (Serial.available() > 0) {
    char input = Serial.read(); // 입력값 읽기

    if (input == '1') {
      Serial.println("[단계 1] 회전 명령 수신: 90도 회전 시작...");
      
      // 90도 이동
      stepper.moveTo(stepper.currentPosition() + STEPS_PER_90DEG);
      
      while (stepper.distanceToGo() != 0) {
        stepper.run();
      }
      
      Serial.println("[단계 2] 90도 회전 완료. 2초 대기 시작.");
      delay(2000);
      
      Serial.println("[단계 3] 2초 대기 완료. 다음 명령을 기다립니다.");
    }
  }
}