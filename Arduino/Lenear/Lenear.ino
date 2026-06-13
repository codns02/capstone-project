// ======================리니어모터===========================

const int linearIn1 = 6;
const int linearIn2 = 7;

void setup() {
  Serial.begin(115200);
  pinMode(linearIn1, OUTPUT);
  pinMode(linearIn2, OUTPUT);
  
  Serial.println("--- 리니어 모터 제어 ---");
  Serial.println("888: 전진 (5초)");
  Serial.println("777: 후진 (5초)");
}

void loop() {
  if (Serial.available() > 0) {
    int cmd = Serial.parseInt();
    
    if (cmd == 888) {
      Serial.println("전진 시작...");
      digitalWrite(linearIn1, HIGH); // 전진 신호
      digitalWrite(linearIn2, LOW);
      delay(13000); 
      stopMotor();
      Serial.println("전진 완료.");
    } 
    else if (cmd == 777) {
      Serial.println("후진 시작...");
      digitalWrite(linearIn1, LOW);  // 후진 신호
      digitalWrite(linearIn2, HIGH);
      delay(13000);
      stopMotor();
      Serial.println("후진 완료.");
    }
    
  }
}

void stopMotor() {
  digitalWrite(linearIn1, LOW);
  digitalWrite(linearIn2, LOW);
}