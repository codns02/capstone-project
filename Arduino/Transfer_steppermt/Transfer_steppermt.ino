const int transPul = 22; // 펄스 핀
const int transDir = 23; // 방향 핀

const int STEPS_90 = 200;    // 90도 회전을 위한 스텝 수 (200 사용)
const int PULSE_DELAY = 2;   // 펄스 간격 (숫자가 클수록 모터가 느려짐)
const int WAIT_TIME = 2000;  // 동작 사이 대기 시간 (2초)

void setup() {
  pinMode(transPul, OUTPUT);
  pinMode(transDir, OUTPUT);
}

// 모터 회전 함수 (direction: true는 시계방향, false는 반시계방향)
void rotate(bool direction, int steps) {
  digitalWrite(transDir, direction);
  for (int i = 0; i < steps; i++) {
    digitalWrite(transPul, HIGH);
    delay(PULSE_DELAY);
    digitalWrite(transPul, LOW);
    delay(PULSE_DELAY);
  }
}

void loop() {
  // 1. 좌로 90도 (false 방향으로 가정)
  rotate(false, STEPS_90);
  delay(WAIT_TIME);

  // 2. 원점 복귀 (true 방향으로 90도)
  rotate(true, STEPS_90);
  delay(WAIT_TIME);

  // 3. 우로 90도 (true 방향으로)
  rotate(true, STEPS_90);
  delay(WAIT_TIME);

  // 4. 우측에서 좌로 180도 회전
  rotate(false, STEPS_90 * 2); 
  delay(5000);

  // 5. 최종 원점 복귀
  rotate(true, STEPS_90);
  delay(WAIT_TIME);
}