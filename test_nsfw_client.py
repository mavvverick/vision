# -*-coding:utf-8-*-
import sys
from nsfw import load_image, predict

_IMAGE_SIZE = 299
SERVER_URL = 'http://localhost:8501/v1/models/nsfw:predict'
_LABEL_MAP = {0: 'drawings', 1: 'hentai', 2: 'neutral', 3: 'porn', 4: 'sexy'}


if __name__ == '__main__':
    image_path = ''
    args = sys.argv
    if len(args) < 2:
        print("usage: python serving_client.py <image_folder>")
    image_path = args[1]
    images_data_list = load_image(image_path)
    predict = predict(images_data_list)
    print(predict)
