import cv2
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock

class EnemyDetectorApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        title = Label(text='🎯 ENEMY DETECTOR', font_size=32, size_hint=(1, 0.15))
        self.layout.add_widget(title)
        self.btn = Button(text='▶ BẮT ĐẦU', size_hint=(1, 0.2), background_color=(0.2, 0.8, 0.2, 1))
        self.btn.bind(on_press=self.toggle_detection)
        self.layout.add_widget(self.btn)
        self.img = Image(size_hint=(1, 0.55))
        self.layout.add_widget(self.img)
        self.status = Label(text='Sẵn sàng', size_hint=(1, 0.1))
        self.layout.add_widget(self.status)
        self.detecting = False
        self.cap = None
        self.prev_gray = None
        return self.layout
    
    def toggle_detection(self, instance):
        if not self.detecting:
            self.detecting = True
            self.btn.text = '⏹ DỪNG'
            self.status.text = 'Đang phát hiện...'
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.status.text = '❌ Không mở được camera'
                self.detecting = False
                return
            Clock.schedule_interval(self.detect_frame, 0.05)
        else:
            self.detecting = False
            self.btn.text = '▶ BẮT ĐẦU'
            self.status.text = 'Đã dừng'
            if self.cap:
                self.cap.release()
                self.cap = None
            Clock.unschedule(self.detect_frame)
    
    def detect_frame(self, dt):
        ret, frame = self.cap.read()
        if not ret:
            self.status.text = '❌ Lỗi đọc frame'
            return
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.prev_gray is not None:
            diff = cv2.absdiff(self.prev_gray, gray)
            _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
            thresh = cv2.dilate(thresh, None, iterations=2)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            enemy_count = 0
            for cnt in contours:
                if cv2.contourArea(cnt) > 500:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                    cv2.putText(frame, 'ENEMY', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    enemy_count += 1
            cv2.putText(frame, f'ENEMIES: {enemy_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            self.status.text = f'🎯 Đang phát hiện... {enemy_count} kẻ địch'
        self.prev_gray = gray
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.resize(frame_rgb, (640, 480))
        cv2.imwrite('/tmp/frame.jpg', frame_rgb)
        self.img.source = '/tmp/frame.jpg'
        self.img.reload()

if __name__ == '__main__':
    EnemyDetectorApp().run()
