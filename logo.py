# -*-coding:utf-8-*-
import numpy as np
from PIL import Image
import sys
import json
import requests
import glob
from tensor_utils import img_to_array
import settings
_IMAGE_SIZE_WIDTH = 180
_IMAGE_SIZE_HEIGHT = 75
_STD = 255

SERVER_URL = settings.HOST + '/v1/models/logo:predict'
_LABEL_MAP = {0: 'likee', 1: 'neutral', 2: 'tiktok'}


def load_image(folder_path):
    try:
        files = [f for f in sorted(glob.glob(
            folder_path + "/**/*.jpg", recursive=True))[:1]]
    except Exception as e:
        print(e)
    input_list = []
    for image_path in files:
        img = Image.open(image_path)
        img = img.crop((0, 0, _IMAGE_SIZE_WIDTH, _IMAGE_SIZE_HEIGHT))
        img.load()
        img = img_to_array(img) / _STD
        img = np.reshape(img, (_IMAGE_SIZE_WIDTH, _IMAGE_SIZE_HEIGHT, 3))
        input_list.append(img.tolist())
        if hasattr(img, 'close'):
            img.close()
    return input_list


def predict(images_data_list):
    if len(images_data_list) < 1:
        return "False"
    try:
        pay_load = json.dumps({"inputs": images_data_list})
        response = requests.post(SERVER_URL, data=pay_load)
    except Exception as e:
        print(e)
    pay_load = json.dumps({"inputs": images_data_list})
    response = requests.post(SERVER_URL, data=pay_load)
    data = response.json()
    predict_result_map = []
    if 'outputs' in data:
        outputs = data['outputs']
        for output in outputs:
            predict_result = {
                _LABEL_MAP[0]: output[0],
                _LABEL_MAP[1]: output[1],
                _LABEL_MAP[2]: output[2],
            }
            predict_result_map.append(predict_result)
        return predict_result_map
    else:
        return data


async def http(post_id):
    # pick selected images
    folder_path = settings.FOLDER_PATH + post_id
    images_data_list = load_image(folder_path)
    result = predict(images_data_list)
    return result
