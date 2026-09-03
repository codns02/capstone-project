# 실시간 웨이퍼 상태 모니터링 시스템 (캡스톤 디자인)

실시간 웹캠 영상 및 YOLO 모델을 활용한 웨이퍼 상태 모니터링, 그리고 아두이노 기반 모터/하드웨어 제어가 통합된 실시간 시스템입니다.

## 📌 주요 기능
* **실시간 모니터링:** 웹캠을 통한 아크릴 웨이퍼 대체재의 색상 변화 및 상태 감지
* **YOLO 비전 모델 연동:** 객체 인식 및 결함 상태 분류
* **하드웨어 제어:** 스테퍼 모터 구동 및 아두이노 마이크로컨트롤러 연동을 통한 물리적 공정 제어
* **GUI 대시보드:** 상태 변화 실시간 시각화 및 센서/모터 동작 로그 출력

## 🛠️ 기술 스택
* **Language:** C# / Python / C++ (Arduino)
* **Framework & Tool:** Windows Forms / WPF / Roboflow (Model Training)
* **Hardware:** Arduino Microcontroller, Stepper Motor, MOSFET, Hall Sensor, SMPS

## 📁 디렉토리 구조
```text
├── src/
│   ├── ClientGUI/     # C# / Windows Forms 대시보드 및 UI
│   ├── VisionModel/   # YOLO 기반 웨이퍼 감지 및 비전 로직
│   └── Arduino/       # 스테퍼 모터 및 센서 제어용 펌웨어 코드
├── docs/              # 프로젝트 보고서 및 발표 자료
├── models/            # YOLO 학습 모델 파일 및 설정
└── README.md          # 프로젝트 개요 및 가이드
