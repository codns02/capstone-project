# Capstone Project: 반도체 포토 공정

본 프로젝트는 반도체 포토 공정을 중심으로 스테퍼모터, 진공펌프, 리니어 액추에이터, 타미야 모터, 웹캠을 활용한 정밀 자동 이송 로봇 시스템입니다. 본 프로젝트에서 하드웨어 조립을 제외한 **모든 프로그래밍(Python 비전 처리, Tkinter GUI, 아두이노 연동 및 시스템 통합)**을 담당했습니다.

## 🛠 Tech Stack & Role
* **Role**: Lead Programmer (전체 소프트웨어 아키텍처 및 프로그래밍 총괄)
* **Programming & GUI**: Python, Tkinter (맥북 기반 GUI 환경)
* **Vision & AI**: OpenCV, YOLO (Roboflow 활용)
* **Hardware Control**: Arduino (스테퍼모터, 진공펌프, 리니어 액추에이터, 타미야 모터, 센서 연동)

## 🛠 폴더 구조

* **Arduino/**: 시스템 제어용 아두이노 소스 코드
  * `Lenear/`: 리니어 모터 제어
  * `Masking_steppermt/`: 마스킹 스태퍼 모터 제어
  * `Tamiya/`: 타미야 모터 제어
  * `Transfer_steppermt/`: 이송용 스태퍼 모터 제어
  * `Vacuum_stepper_hallsensor/`: 흡착 및 RPM 측정 통합 코드
  * *... 외 유틸리티 코드*
* **Python/**: 비전 처리 및 시스템 통합 스크립트
  * `main.py`: 메인 시스템 제어 및 Tkinter GUI 연동
  * `collect_data.py`: 센서 데이터 수집
  * `vision_test.py`: 비전 처리 테스트
  * `report.py`: 생산 리포트 생성

## ⚙️ 주요 기능

* **정밀 이송**: 스태퍼 모터를 활용한 위치 제어 및 리니어 액추에이터 연동
* **통합 제어 및 GUI**: 흡착, 스태퍼 모터, 센서 데이터의 실시간 동기화 및 맥북 환경 Tkinter GUI를 통한 시스템 제어
* **모니터링**: 홀센서를 이용한 실시간 RPM 측정 및 시스템 로그 기록

## 🔄 시스템 작동 흐름 (Logic Flow)

1. **비전 인식 (Python)**: 웹캠을 통해 공정 상황 및 대상 상태를 실시간 모니터링
2. **제어 명령 (Python/Tkinter -> Arduino)**: 맥북 Tkinter GUI의 인터페이스 조작에 따라 아두이노로 구동 명령 전달
3. **하드웨어 구동 (Arduino)**: 스태퍼모터, 진공펌프, 리니어 모터 등을 통해 물리적 이송 및 흡착 수행
4. **피드백 및 리포트**: 센서 데이터를 수집하여 RPM을 측정하고, `report.py`를 통해 공정 리포트 생성

본 프로젝트는 캡스톤 디자인 결과물입니다.
