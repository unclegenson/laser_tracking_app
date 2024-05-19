from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import *
import cv2

class MainApp(MDApp):
    def build(self):
        layout = MDBoxLayout(orientation='vertical')
        self.image = Image()

        self.closeButton = MDRaisedButton(
            text='Close',
            pos_hint = {'center_x': 0.5,'center_y':1.5},
            size_hint = (None,None),
            )
        
        self.closeButton.bind(on_oress = self.close)

        layout.add_widget(
            self.closeButton
        )
        layout.add_widget(
            self.image
        )
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video,1/30)

        return layout
    
    def load_video(self,*args):
        ret,frame = self.capture.read()
        self.image_frame = frame
        buffer = cv2.flip(frame,1).tobytes()
        texture = Texture.create(size = (frame.shape[1],frame.shape[0]),colorfmt = 'bgr') # type: ignore
        texture.blit_buffer(buffer,colorfmt = 'bgr',bufferfmt = 'ubyte')
        self.image.texture = texture

    def close(self):
        MDApp.stop()
        

if __name__ == '__main__':
    MainApp().run()