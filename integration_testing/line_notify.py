"""
Doc: https://notify-bot.line.me/doc/en/
Pypi: https://pypi.org/project/line_notify
Github: https://github.com/golbin/line-notify
"""

import os
import cv2
import requests


class LineNotify:
    API_URI = 'https://notify-api.line.me/api/notify'

    def __init__(self, access_token: str = None, room_name: str = None):
        self.access_token = access_token
        self.room_name = room_name
        self.enable = isinstance(self.access_token, str) and self.access_token is not None
        self.headers = {
            "Authorization": f"Bearer {str(self.access_token)}"
        }
        if not self.enable:
            print('WARNING: missing access token, please set the token with `set_token()` function')

    def enable(self):
        """enable notify message"""
        self.enable = True

    def disable(self):
        """disable notify message"""
        self.enable = False

    def set_token(self, token: str = None):
        """set or modify the access token"""
        self.access_token = token
        self.enable = isinstance(self.access_token, str) and self.access_token is not None
        self.headers = {
            "Authorization": f"Bearer {str(self.access_token)}"
        }
        print(f'INFO: change access token to "{self.access_token}"')

    def send_message(self, message: str, sticker_id: int = None, package_id: int = None):
        if self.enable:
            params = {'message': message}

            if sticker_id and package_id:
                params = {**params, "stickerId": sticker_id, "stickerPackageId": package_id}

            _ = requests.post(
                url=self.API_URI,
                headers=self.headers,
                params=params
            )

    def send_image(self, message: str, image_type: str, image_path: str, image_thumbnail: str = None, sticker_id: int = None, package_id: int = None):
        if self.enable:
            params = {'message': message}
            files = {}

            if sticker_id and package_id:
                params = {**params, "stickerId": sticker_id, "stickerPackageId": package_id}

            if image_type == 'local' and os.path.isfile(image_path):
                # sending local image have size limitation, need to resize the image first
                image_path = LineNotify.resize_image(image_path)
                files = {"imageFile": open(image_path, "rb")}

            elif image_type == 'url':
                if not image_thumbnail:
                    image_thumbnail = image_path
                params = {**params, 'imageThumbnail': image_thumbnail, 'imageFullsize': image_path}

            _ = requests.post(
                url=self.API_URI,
                headers=self.headers,
                params=params,
                files=files
            )

    @staticmethod
    def resize_image(image_path: str, max_width: int = 1500):
        image = cv2.imread(image_path)
        height, width, _ = image.shape

        if width > max_width:
            scale = max_width / width
            dim = (int(width * scale), int(height * scale))
            new_image = cv2.resize(image, dim)
            new_image_path = LineNotify.format_image_name(image_path)
            cv2.imwrite(new_image_path, new_image)
            return new_image_path
        else:
            return image_path

    @staticmethod
    def format_image_name(image_path: str):
        return f"{image_path.split('.')[0]}_1.jpg"


# function demo
if __name__ == '__main__':
    # TODO: config `LINE_ACCESS_TOKEN` credential before execute
    LINE_ACCESS_TOKEN = ''
    notify_client = LineNotify(LINE_ACCESS_TOKEN)

    image_url = 'https://media.jobthai.com/v1/images/logo-pic-map/318140_logo_20221219135346.jpeg'
    image_path = 'sample_image.jpg'

    # notify_client.send_message('message 1')
    # notify_client.send_message('message with sticker', sticker_id=283, package_id=4)

    # notify_client.send_image('message and local image', 'local', image_path)
    # notify_client.send_image('message with sticker and local image', 'local', image_path, sticker_id=283, package_id=4)

    # notify_client.send_image('message and url-image', 'url', image_url)
    # notify_client.send_image('message with sticker and url-image', 'url', image_url, sticker_id=283, package_id=4)
