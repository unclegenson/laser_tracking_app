# import cv2
from kivy.app import App 
from kivy.uix.button import Button
# from kivy.uix.camera import Camera
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import  BoxLayout


class BoxLayoutExample(BoxLayout):
    def on_open_camera_clicked(seld):
        print('on_open_camera_clicked')     


class bagherZadehLaser(App):
    pass
if __name__ == '__main__':
    bagherZadehLaser().run()
