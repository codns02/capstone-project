# Capstone Project: Smart Transfer System
본 프로젝트는 스테퍼모터, 진공펌프, 리니어 액추에이터, 타미야 모터, 웹캠을 활용한 정밀 자동 이송 로봇 시스템입니다.

## 🛠 폴더 구조
- **Arduino/**: 시스템 제어용 아두이노 소스 코드
  - `Lenear/`: 리니어 모터 제어
  - `Masking_steppermt/`: 마스킹 스태퍼 모터 제어
  - `Tamiya/`: 타미야 모터 제어
  - `Transfer_steppermt/`: 이송용 스태퍼 모터 제어
  - `Vacuum_stepper_hallsensor/`: 흡착 및 RPM 측정 통합 코드
  - ... 외 유틸리티 코드

- **Python/**: 비전 처리 및 시스템 통합 스크립트
  - `main.py`: 메인 시스템 제어
  - `collect_data.py`: 센서 데이터 수집
  - `vision_test.py`: 비전 처리 테스트
  - `report.py`: 생산 리포트 생성

## ⚙️ 주요 기능
- **정밀 이송**: 스태퍼 모터를 활용한 위치 제어
- **통합 제어**: 흡착, 스태퍼 모터, 센서 데이터의 실시간 동기화
- **모니터링**: 홀센서를 이용한 실시간 RPM 측정 및 시스템 로그 기록

---
*본 프로젝트는 캡스톤 디자인 결과물입니다.*
