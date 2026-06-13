import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import os
from datetime import datetime

class DataCollector(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI 학습 데이터 수집기 - Lee Chae-un")
        # 창 크기를 더 크게 키우고 화면 중앙 근처에 띄웁니다.
        self.geometry("800x700") 
        ctk.set_appearance_mode("dark")
        
        # 저장 폴더 설정
        self.save_path = "dataset"
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        # 레이아웃 구성
        self.v_l = ctk.CTkLabel(self, text="카메라 연결 중...", fg_color="black", width=640, height=480)
        self.v_l.pack(pady=20)

        # 버튼을 카메라 바로 아래, 눈에 잘 띄는 노란색으로 배치
        self.btn_capture = ctk.CTkButton(self, text="📸 사진 저장 (키보드 S)", 
                                         command=self.save_image, 
                                         width=300, height=60,
                                         fg_color="#f1c40f", text_color="black",
                                         hover_color="#f39c12",
                                         font=("Apple SD Gothic Neo", 20, "bold"))
        self.btn_capture.pack(pady=20)

        # 안내 문구
        self.info_label = ctk.CTkLabel(self, text="S 키를 누르면 'dataset' 폴더에 저장됩니다", font=("Apple SD Gothic Neo", 14))
        self.info_label.pack()

        self.bind("<s>", lambda e: self.save_image())
        self.bind("<S>", lambda e: self.save_image()) # 대문자 S도 대비

        self.cap = cv2.VideoCapture(0) # 기본 카메라 시도
        self.last_frame = None
        self.upd()

    def save_image(self):
        if self.last_frame is not None:
            now = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"wafer_{now}.jpg"
            full_path = os.path.join(self.save_path, filename)
            
            save_frame = cv2.cvtColor(self.last_frame, cv2.COLOR_RGB2BGR)
            cv2.imwrite(full_path, save_frame)
            
            # 저장 성공 시 버튼 색을 잠시 녹색으로 바꿔서 알림
            self.btn_capture.configure(fg_color="#2ecc71", text="✅ 저장 완료!")
            self.after(500, lambda: self.btn_capture.configure(fg_color="#f1c40f", text="📸 사진 저장 (키보드 S)"))
            print(f"저장 성공: {full_path}")

    def upd(self):
        ret, frame = self.cap.read()
        if ret:
            self.last_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(self.last_frame).resize((640, 480))
            itk = ImageTk.PhotoImage(image=img)
            self.v_l.configure(image=itk)
            self.v_l.image = itk
        self.after(30, self.upd)

if __name__ == "__main__":
    app = DataCollector()
    app.mainloop()