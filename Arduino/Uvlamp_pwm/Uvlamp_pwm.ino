// 5번 핀 (PWM 지원 핀)에 연결
const int uvLampPin = 5; 

void setup() {
  pinMode(uvLampPin, OUTPUT);
  // 속도 115200으로 설정 (시리얼 모니터 설정과 일치시키세요)
  Serial.begin(115200); 
  Serial.println("UV 램프 제어 모드 (0~255 입력)");
}

void loop() {
  if (Serial.available() > 0) {
    // 숫자를 읽어옵니다
    int pwmValue = Serial.parseInt(); 
    
    // 버퍼에 남아있는 줄바꿈 문자 등을 깔끔하게 비웁니다.
    while(Serial.available() > 0) Serial.read(); 

    // 0~255 범위 내일 때만 동작하도록 제한
    if (pwmValue >= 0 && pwmValue <= 255) {
      analogWrite(uvLampPin, pwmValue);
      Serial.print("UV 강도 설정값: ");
      Serial.println(pwmValue);
    }
  }
}