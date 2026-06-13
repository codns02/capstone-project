import cv2
import inference
import time

# 1. 로컬 엔진 설정 
model = inference.get_model("wafer-inspection-yquzm/4", api_key="EedFtNLDd9Or89P2LVgN")

# 2. 웹캠 설정
video = cv2.VideoCapture(0)

print("로컬 엔진 가동 (종료: q)")

while True:
    ret, frame = video.read()
    if not ret: break

    start_time = time.time()

    # 3. 로컬 추론 실행
    results = model.infer(frame, confidence=0.4)[0]

    # 4. 결과 직접 그리기 (라이브러리 버그를 피하는 가장 확실한 방법)
    for detection in results.predictions:
        # 박스 좌표 계산
        x, y, w, h = int(detection.x), int(detection.y), int(detection.width), int(detection.height)
        label = detection.class_name
        conf = detection.confidence
        
        # 사각형 그리기 (보라색: 255, 0, 255)
        cv2.rectangle(frame, (int(x-w/2), int(y-h/2)), (int(x+w/2), int(y+h/2)), (255, 0, 255), 2)
        # 라벨 표시
        cv2.putText(frame, f"{label} {conf:.2f}", (int(x-w/2), int(y-h/2)-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

    # 5. FPS 표시 및 출력
    fps = 1 / (time.time() - start_time)
    cv2.putText(frame, f"FPS: {fps:.1f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Wafer Detection - Local", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()