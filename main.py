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
        self.title = Label(text='🎯 ENEMY DETECTOR', font_size=32)
        self.layout.add_widget(self.title)
        self.btn = Button(text='▶ BẮT ĐẦU', size_hint=(1, 0.2))
        self.btn.bind(on_press=self.toggle)
        self.layout.add_widget(self.btn)
        self.img = Image(size_hint=(1, 0.5))
        self.layout.add_widget(self.img)
        self.status = Label(text='Sẵn sàng')
        self.layout.add_widget(self.status)
        self.detecting = False
        self.cap = None
        return self.layout
    
    def toggle(self, instance):
        if not self.detecting:
            self.detecting = True
            self.btn.text = '⏹ DỪNG'
            self.status.text = 'Đang phát hiện...'
            self.cap = cv2.VideoCapture(0)
            Clock.schedule_interval(self.detect, 0.05)
        else:
            self.detecting = False
            self.btn.text = '▶ BẮT ĐẦU'
            self.status.text = 'Đã dừng'
            Clock.unschedule(self.detect)
            if self.cap:
                self.cap.release()
                self.cap = None
    
    def detect(self, dt):
        ret, frame = self.cap.read()
        if not ret:
            return
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if not hasattr(self, 'prev'):
            self.prev = gray
            return
        diff = cv2.absdiff(self.prev, gray)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv2.contourArea(cnt) > 500:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        self.prev = gray
        cv2.imwrite('/tmp/frame.jpg', frame)
        self.img.source = '/tmp/frame.jpg'
        self.img.reload()

if __name__ == '__main__':
    EnemyDetectorApp().run()
