// =================타미야 모터====================

// 핀 설정
const int ena = 9;
const int tamiyaIn1 = 10;
const int tamiyaIn2 = 11;
const int tamiyaIn3 = 12;
const int tamiyaIn4 = 4;

void setup() {
  Serial.begin(115200);

  pinMode(ena, OUTPUT);
  pinMode(tamiyaIn1, OUTPUT);
  pinMode(tamiyaIn2, OUTPUT);
  pinMode(tamiyaIn3, OUTPUT);
  pinMode(tamiyaIn4, OUTPUT);

  analogWrite(ena, 200); // 속도 제어

  Serial.println("--- 타미야 모터 정/역방향 개별 제어 ---");
  Serial.println("모터 1: 999(상승), 777(하강)");
  Serial.println("모터 2: 888(하강), 666(상승)");
}

// 1번 모터 동작 (정/역방향 선택)
void runMotor1(bool forward) {
  if (forward) {
    digitalWrite(tamiyaIn1, HIGH);
    digitalWrite(tamiyaIn2, LOW);
    Serial.println("모터 1 정방향 가동...");
  } else {
    digitalWrite(tamiyaIn1, LOW);
    digitalWrite(tamiyaIn2, HIGH);
    Serial.println("모터 1 역방향 가동...");
  }
}

// 2번 모터 동작 (정/역방향 선택)
void runMotor2(bool forward) {
  if (forward) {
    digitalWrite(tamiyaIn3, HIGH);
    digitalWrite(tamiyaIn4, LOW);
    Serial.println("모터 2 정방향 가동...");
  } else {
    digitalWrite(tamiyaIn3, LOW);
    digitalWrite(tamiyaIn4, HIGH);
    Serial.println("모터 2 역방향 가동...");
  }
}

// 모든 모터 정지
void stopAllMotors() {
  digitalWrite(tamiyaIn1, LOW);
  digitalWrite(tamiyaIn2, LOW);
  digitalWrite(tamiyaIn3, LOW);
  digitalWrite(tamiyaIn4, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    int cmd = Serial.parseInt();
    
    // 모터 1 제어 이송용 타미야
    if (cmd == 999) { runMotor1(true); delay(3000); stopAllMotors(); }
    else if (cmd == 777) { runMotor1(false); delay(300); stopAllMotors(); }
    
    // 모터 2 제어 노광 차폐
    else if (cmd == 888) { runMotor2(true); delay(3000); stopAllMotors(); }
    else if (cmd == 666) { runMotor2(false); delay(300); stopAllMotors(); }
  }
}

