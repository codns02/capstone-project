// 1. 상태 정의
enum SystemState { MOVE_LEFT, LINEAR_FWD, TAMIYA_DOWN_2, TAMIYA_DOWN_HOME };
SystemState currentStep = MOVE_LEFT;

// 2. 핀 설정
const int ena = 9;
const int tamiyaIn1 = 10;
const int tamiyaIn2 = 11;
const int tamiyaIn3 = 12;
const int tamiyaIn4 = 13;
const int hcSensorPin = 39; // HC 모듈 연결 핀

void setup() {
  Serial.begin(115200);

  pinMode(ena, OUTPUT);
  pinMode(tamiyaIn1, OUTPUT);
  pinMode(tamiyaIn2, OUTPUT);
  pinMode(tamiyaIn3, OUTPUT);
  pinMode(tamiyaIn4, OUTPUT);
  pinMode(hcSensorPin, INPUT_PULLUP); // 센서 핀 설정

  analogWrite(ena, 200);

  // 시리얼 모니터 입력 대기
  Serial.println("시스템 대기 중... 시작하려면 's'를 입력하세요.");
  while (true) {
    if (Serial.available() > 0) {
      char cmd = Serial.read();
      if (cmd == 's' || cmd == 'S') {
        Serial.println("시스템 시작!");
        break;
      }
    }
  }
}

// 하강하며 원점 찾기 함수
void runDownUntilHome() {
  Serial.println("하강 시작 (원점 찾는 중)...");
  digitalWrite(tamiyaIn1, LOW);
  digitalWrite(tamiyaIn2, HIGH); 

  // 센서가 LOW가 될 때까지 반복
  while (digitalRead(hcSensorPin) == HIGH) {
    // 센서 감지 대기
  }

  stopAllMotors();
  Serial.println("원점(HC모듈) 감지 완료! 하강 정지.");
}

void stopAllMotors() {
  digitalWrite(tamiyaIn1, LOW); digitalWrite(tamiyaIn2, LOW);
  digitalWrite(tamiyaIn3, LOW); digitalWrite(tamiyaIn4, LOW);
}

void loop() {
  switch (currentStep) {
    case MOVE_LEFT:
      // MOVE_LEFT 동작 로직 구현
      currentStep = LINEAR_FWD; // 다음 단계로
      break;

    case LINEAR_FWD:
      // LINEAR_FWD 동작 로직 구현
      currentStep = TAMIYA_DOWN_2;
      break;

    case TAMIYA_DOWN_2:
      // 하강 명령 수행
      runDownUntilHome(); 
      currentStep = TAMIYA_DOWN_HOME; // 완료 후 다음 상태로
      break;

    case TAMIYA_DOWN_HOME:
      // 이후 동작 로직
      break;
  }
}