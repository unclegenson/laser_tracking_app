# import cv2
import mimetypes
import os
import os.path
import mimetypes
from urllib.parse import urljoin

import sys
sys.platform = 'msys'

import requests

from jnius import autoclass, cast


from kivy.app import App 
from kivy.uix.button import Button

from kivy.uix.boxlayout import  BoxLayout
import requests


class BoxLayoutExample(BoxLayout):
    def on_open_camera_clicked(seld):
        print('on_open_camera_clicked') 

    def download_file(self, url):
        save_dir = self.user_data_dir
        local_filename = url.split('/')[-1]
        local_file = os.path.join(save_dir, local_filename)
        response = requests.get(url, stream=True)
        with open(local_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
        return local_file

    def open_image(self, button):
        # Android stuff
        PythonActivity = autoclass('org.renpy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')

        url = "http://www.mountvernon.org/sites/mountvernon.org/files/images/GW_Stuart-CT-6437.jpg"
        path = self.download_file(url)
        mimetype = mimetypes.guess_type(path)[0]
        image_uri = urljoin('file://', path)

        print("Starting intent...")
        intent = Intent()
        intent.setAction(Intent.ACTION_VIEW)
        intent.setDataAndType(Uri.parse(image_uri), mimetype)
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        currentActivity.startActivity(intent)
        print("Finished intent")  


class bagherZadehLaser(App):
    pass


if __name__ == '__main__':
    bagherZadehLaser().run()
