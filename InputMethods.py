import json
from CustomErrors import *


def input_json(path=None, file_name=None):
    file_name= path + file_name
    try:
        with open(file_name, mode='r') as f:
            data = json.load(f)
            return data
    except Exception:
        raise InputDataError()