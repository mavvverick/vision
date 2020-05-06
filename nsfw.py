# -*-coding:utf-8-*-
import numpy as np
from PIL import Image
import sys
import json
import requests
import glob
import settings
from tensor_utils import img_to_array

_IMAGE_SIZE = 299
SERVER_URL = settings.HOST + '/v1/models/nsfw:predict'
_LABEL_MAP = {0: 'drawings', 1: 'hentai', 2: 'neutral', 3: 'porn', 4: 'sexy'}


def load_image(folder_path):
    files = [f for f in glob.glob(
        folder_path + "/**/*.jpg", recursive=True)[:1]]
    input_list = []

    for image_path in files:
        img = Image.open(image_path)
        img = img.resize((_IMAGE_SIZE, _IMAGE_SIZE))
        img.load()
        img = img_to_array(img) / 255
        img = img.astype('float16')
        input_list.append(img.tolist())
        if hasattr(img, 'close'):
            img.close()
    return input_list


def predict(images_data_list):
    # pay_load = json.dumps(
    #     {"inputs": [image_data.tolist(), image_data.tolist()]})
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
                _LABEL_MAP[3]: output[3],
                _LABEL_MAP[4]: output[4]
            }
            predict_result_map.append(predict_result)
        return predict_result_map
    else:
        return data


async def http(post_id):
    # folder_path = settings.FOLDER_PATH + post_id
    # await download_unzip(folder_path, post_id)
    images_data_list = load_image(settings.FOLDER_PATH)
    result = predict(images_data_list)
    return result
