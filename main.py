from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import *
import imutils
import numpy as np
import cv2
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

def kivy_play_sound(sound):
    SoundLoader.load(sound).play()

def reject_outliers(data, m = 3.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zeros(len(d))
    return data[s<m]

Y_distances = []
X_distances = []
cap = cv2.VideoCapture(0)

X_axis ,Y_axis= [],[]

class MainApp(App):
    def build(self):

        layout = BoxLayout(orientation='vertical')
        self.image = Image()

        self.closeButton = Button(
            text='Close App',
            pos_hint = {'center_x': 0.5,'center_y':0.5},
            size_hint = (None,None),
            )
        self.closeButton.bind(on_press=self.close_app)
        
        layout.add_widget(
            self.image
        )
        layout.add_widget(
            self.closeButton
        )
        Clock.schedule_interval(self.load_video,1/30)

        return layout
    
    def close_app(self):
        App.stop()
        exit()

    def load_video(self,*args):
        global X_axis,Y_axis

        _,captured_frame = cap.read()

        captured_frame = imutils.resize(captured_frame, width=Window.size[0], height=Window.size[1])
        
        output_frame = captured_frame.copy()

        captured_frame_bgr = cv2.cvtColor(captured_frame, cv2.COLOR_BGRA2BGR)

        captured_frame_bgr = cv2.medianBlur(captured_frame_bgr, 3)
        captured_frame_lab = cv2.cvtColor(captured_frame_bgr, cv2.COLOR_BGR2Lab)
        captured_frame_lab_red = cv2.inRange(captured_frame_lab, np.array([30, 150, 150]), np.array([190, 255, 255])) 

        sensitivity = 15
        lower_white = np.array([0,0,255-sensitivity])
        upper_white = np.array([255,sensitivity,255])  

        captured_frame_lab_white = cv2.inRange(captured_frame_lab, lower_white, upper_white) 
        captured_frame_lab_white = cv2.GaussianBlur(captured_frame_lab_red, (5, 5), 2, 2)
        circles = cv2.HoughCircles(captured_frame_lab_white, cv2.HOUGH_GRADIENT, 1, captured_frame_lab_white.shape[0] / 8, param1=100,
                                    param2=18, minRadius=2, maxRadius=20)
        
        
        if circles is None:
            # kivy_play_sound('nothing_detected.mp3')
            cv2.putText(output_frame,'0 laser detected',(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.6,255)

        elif circles is not None:
            if len(circles[0]) > 1:
                # kivy_play_sound('more_than_one.mp3')
                cv2.putText(output_frame,'more than 1 laser detected',(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.6,255)

            else:
                # x, y, radius
                # x az chap and y az bala 
                x = circles[0][0][0]
                y = circles[0][0][1]
                X_axis.append(x)
                Y_axis.append(y)

                circles = np.round(circles[0, :]).astype("int")
                cv2.circle(output_frame, center=(circles[0, 0], circles[0, 1]), radius=circles[0, 2], color=(0, 255, 0), thickness=2)
                cv2.putText(output_frame,'1 laser detected',(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.6,255)

                X_axis = reject_outliers(np.array(X_axis))
                Y_axis = reject_outliers(np.array(Y_axis))
                X_axis = list(X_axis)
                Y_axis = list(Y_axis)

                if len(X_axis) > 5:
                    for index in range(len(X_axis)):
                        if index == 0:
                            pass
                        else:
                            result = round(X_axis[index] - X_axis[index-1],3)
                            if result != 0:
                                X_distances.append(result)

                    for x_distance in X_distances:
                        if abs(x_distance) >=  2 * abs(sum(X_distances) / len(X_distances)):
                            cv2.putText(output_frame,'Paresh X',(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.6,255)   
                            kivy_play_sound('something_detected.mp3')
                            X_axis = list(X_axis)
                            X_axis.clear()
                            Y_axis = list(Y_axis)
                            Y_axis.clear()
                            X_distances.clear()
                            Y_distances.clear()
                            break

                        elif abs(x_distance) <=  abs(sum(X_distances) / len(X_distances)) / 3:
                            cv2.putText(output_frame,'Mane X',(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.6,255)
                            kivy_play_sound('something_detected.mp3')
                            X_axis = list(X_axis)
                            X_axis.clear()
                            Y_axis = list(Y_axis)
                            Y_axis.clear()
                            X_distances.clear()
                            Y_distances.clear()

                            break


                    if len(Y_axis) > 5:
                        for index in range(len(Y_axis)):
                            if index == 0:
                                pass
                            else:
                                result = round(Y_axis[index] - Y_axis[index-1],3)
                                if result != 0:
                                    Y_distances.append(result)

                        for y_distance in Y_distances:
                            if abs(y_distance) >=  2 * abs(sum(Y_distances) / len(Y_distances)):
                                cv2.putText(output_frame,'Paresh Y',(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.6,255)
                                kivy_play_sound('something_detected.mp3')
                                X_axis = list(X_axis)
                                X_axis.clear()
                                Y_axis = list(Y_axis)
                                Y_axis.clear()
                                Y_distances.clear()
                                X_distances.clear()
                                break

                            elif abs(y_distance) <=  abs(sum(Y_distances) / len(Y_distances)) / 3:
                                cv2.putText(output_frame,'Mane Y',(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.6,255)
                                kivy_play_sound('something_detected.mp3')
                                X_axis = list(X_axis)
                                X_axis.clear()
                                Y_axis = list(Y_axis)
                                Y_axis.clear()
                                Y_distances.clear()
                                X_distances.clear()
                                break
                # else:
                #     X_axis = list(X_axis)
                #     Y_axis = list(Y_axis)        
    
        self.image_frame = output_frame
        buffer = cv2.flip(output_frame,0).tobytes()
        texture = Texture.create(size = (output_frame.shape[1],output_frame.shape[0]),colorfmt = 'bgr') # type: ignore
        texture.blit_buffer(buffer,colorfmt = 'bgr',bufferfmt = 'ubyte')
        self.image.texture = texture        

if __name__ == '__main__':
    MainApp().run()
    
cv2.destroyAllWindows()
