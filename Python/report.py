import os
os.environ["CORE_MODEL_SAM_ENABLED"] = "False"
os.environ["CORE_MODEL_SAM2_ENABLED"] = "False"
os.environ["CORE_MODEL_SAM3_ENABLED"] = "False"
os.environ["CORE_MODEL_GAZE_ENABLED"] = "False"
os.environ["CORE_MODEL_YOLO_WORLD_ENABLED"] = "False"

import cv2
import inference
import time
import numpy as np
from datetime import datetime
from PIL import ImageFont, ImageDraw, Image

# 1. 모델 및 카메라 세팅
model = inference.get_model("wafer-inspection-yquzm/4", api_key="EedFtNLDd9Or89P2LVgN")
video = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

# 2. 통계 변수 초기화
total_count = 0
pass_count = 0
fail_count = 0
yield_rate = 100.0
pattern_ratio = 0.0  

has_counted_this_wafer = False   
missing_frame_counter = 0     
MAX_MISSING_FRAMES = 10       

failed_images_log = []

# M1 맥북 기본 한글 폰트 지정
FONT_PATH = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
font_title = ImageFont.truetype(FONT_PATH, 18)
font_body = ImageFont.truetype(FONT_PATH, 15)
font_yield = ImageFont.truetype(FONT_PATH, 20)

def draw_korean_text(img, text, position, font, color):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    draw = ImageDraw.Draw(img_pil)
    draw.text(position, text, font=font, fill=color)
    img_bgr = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    return img_bgr

# 하이브리드 제어 변수 (True: 자동 모드 활성화 / False: 수동 정지)
is_auto_mode_active = True 

print("📊 [시스템] 레이턴시 제로 하이브리드 모니터링 엔진 가동...")

while True:
    ret, frame = video.read()
    if not ret: break

    start_time = time.time()

    h_ori, w_ori, _ = frame.shape
    frame_area = h_ori * w_ori  

    # 중앙 영역 자동 감지 가이드 박스 설정 (크기 240px)
    center_y, center_x = h_ori // 2, w_ori // 2
    roi_size = 240
    roi_x1, roi_y1 = center_x - (roi_size // 2), center_y - (roi_size // 2)
    roi_x2, roi_y2 = center_x + (roi_size // 2), center_y + (roi_size // 2)

    total_pattern_area = 0
    detected_this_frame = False
    is_inspection_running = False

    # 수동 잠금 상태(False)일 때는 무거운 연산(밝기 계산, AI 추론)을 통째로 스킵하여 반응속도 극대화
    if is_auto_mode_active:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        roi_pixels = gray[roi_y1:roi_y2, roi_x1:roi_x2]
        avg_brightness = np.mean(roi_pixels)
        
        is_wafer_in_box = avg_brightness > 130 
        is_inspection_running = is_wafer_in_box

        if is_inspection_running:
            cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 0), 3)
            
            if has_counted_this_wafer:
                frame = draw_korean_text(frame, "● 해당 웨이퍼 검사 완료 (이탈 대기)", (roi_x1, roi_y1 - 25), font_body, (0, 255, 255))
            else:
                frame = draw_korean_text(frame, "● AI 실시간 공정 검사중", (roi_x1, roi_y1 - 25), font_body, (0, 255, 0))
                
                # AI 모델 추론
                results = model.infer(frame, confidence=0.35)[0]
                
                if len(results.predictions) > 0:
                    detected_this_frame = True
                    
                for detection in results.predictions:
                    x, y, w, h = int(detection.x), int(detection.y), int(detection.width), int(detection.height)
                    conf = detection.confidence
                    
                    cv2.rectangle(frame, (int(x-w/2), int(y-h/2)), (int(x+w/2), int(y+h/2)), (0, 255, 0), 2)
                    frame = draw_korean_text(frame, f"[패턴] {conf:.2f}", (int(x-w/2), int(y-h/2)-20), font_body, (0, 255, 0))
                    
                    total_pattern_area += (w * h)

                if detected_this_frame:
                    pattern_ratio = min((total_pattern_area / frame_area) * 800, 100.0)
                else:
                    pattern_ratio = 0.0

                if not has_counted_this_wafer:
                    if detected_this_frame:
                        missing_frame_counter = 0
                        total_count += 1
                        pass_count += 1
                        yield_rate = (pass_count / total_count) * 100
                        has_counted_this_wafer = True  
                        print(f"🟢 [PASS] 정상 판정 완료 (총: {total_count}개)")
                    else:
                        missing_frame_counter += 1
                        if missing_frame_counter >= MAX_MISSING_FRAMES:
                            total_count += 1
                            fail_count += 1
                            yield_rate = (pass_count / total_count) * 100
                            
                            now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                            img_path = f"fail_log_{total_count}_{now_str}.jpg"
                            cv2.imwrite(img_path, frame)
                            failed_images_log.append(img_path)
                            
                            missing_frame_counter = 0  
                            has_counted_this_wafer = True  
                            print(f"🚨 [FAIL] 불량 판정 완료 (총: {total_count}개)")
        else:
            has_counted_this_wafer = False 
            missing_frame_counter = 0
            pattern_ratio = 0.0
            cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 165, 255), 1)
            frame = draw_korean_text(frame, "○ 공정 웨이퍼 진입 대기중", (roi_x1, roi_y1 - 25), font_body, (0, 165, 255))
    else:
        has_counted_this_wafer = False 
        missing_frame_counter = 0
        pattern_ratio = 0.0
        cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 0, 255), 2)
        frame = draw_korean_text(frame, "■ 시스템 강제 일시정지됨", (roi_x1, roi_y1 - 25), font_body, (0, 0, 255))

    # 4. 우측 대시보드 UI 그리기
    dashboard_width = 330
    dashboard = np.zeros((h_ori, dashboard_width, 3), dtype=np.uint8)
    fps = 1 / (time.time() - start_time)
    
    cv2.line(dashboard, (15, 50), (310, 50), (100, 100, 100), 1)
    cv2.line(dashboard, (15, 235), (310, 235), (100, 100, 100), 1)

    dashboard = draw_korean_text(dashboard, "웨이퍼 모니터링 시스템", (15, 20), font_title, (255, 255, 255))
    dashboard = draw_korean_text(dashboard, f"검사 속도 : {fps:.1f} FPS", (20, 70), font_body, (255, 255, 0)) 
    dashboard = draw_korean_text(dashboard, f"총 검사 수량 : {total_count} 개", (20, 105), font_body, (255, 255, 255))
    dashboard = draw_korean_text(dashboard, f"정상 판정(PASS) : {pass_count} 개", (20, 140), font_body, (0, 255, 0)) 
    dashboard = draw_korean_text(dashboard, f"불량 감지(FAIL) : {fail_count} 개", (20, 175), font_body, (255, 0, 0)) 
    
    dashboard = draw_korean_text(dashboard, f"문양 잔존율 : {pattern_ratio:.1f} %", (20, 255), font_yield, (0, 255, 255))
    yield_color = (0, 255, 0) if yield_rate >= 90 else (0, 165, 255)
    dashboard = draw_korean_text(dashboard, f"실시간 라인 수율 : {yield_rate:.1f} %", (20, 295), font_yield, yield_color)
    
    if not is_auto_mode_active:
        dashboard = draw_korean_text(dashboard, "■ 상태: 시스템 일시정지", (20, h_ori - 95), font_title, (0, 0, 255))
    elif is_inspection_running:
        dashboard = draw_korean_text(dashboard, "● 상태: 검사 가동중", (20, h_ori - 95), font_title, (0, 255, 0))
    else:
        dashboard = draw_korean_text(dashboard, "○ 상태: 웨이퍼 대기중", (20, h_ori - 95), font_title, (150, 150, 150))
        
    dashboard = draw_korean_text(dashboard, "[S] 잠금 토글  |  [R] 리포트  |  [Q] 종료", (15, h_ori - 45), font_body, (120, 120, 120))

    # 5. 화면 결합 및 출력
    combined_screen = np.hstack((frame, dashboard))
    cv2.imshow("Smart Factory Dashboard", combined_screen)

    # 6. 키 입력 감지 (통합 단일 구조)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        is_auto_mode_active = not is_auto_mode_active
        print(f"🔄 [모드 변경] -> {'자동 감지 활성화' if is_auto_mode_active else '수동 잠금(정지)'}")
    elif key == ord('r'):
        # ⭐ [원복 완료] 한 줄에 하나씩 출력되던 원래의 깔끔한 리포트 포맷
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"Wafer_Production_Report_{now}.txt"
        with open(report_filename, "w", encoding="utf-8") as f:
            f.write("==================================================\n")
            f.write("      반도체 공정 모니터링 시스템 최종 분석 리포트\n")
            f.write("==================================================\n")
            f.write(f"출력 일시 : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"■ 총 검사 공정 수량 : {total_count} ea\n")
            f.write(f"■ 정상 판정 수량(PASS) : {pass_count} ea\n")
            f.write(f"■ 불량 검출 수량(FAIL) : {fail_count} ea\n")
            f.write(f"■ 공정 라인 최종 수율 : {yield_rate:.2f} %\n")
            f.write("==================================================\n")
        print(f"📊 [성공] 기존 양식으로 분석 리포트가 성공적으로 저장되었습니다: {report_filename}")
    elif key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()