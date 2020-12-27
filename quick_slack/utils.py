import json
import os
from multiprocessing import Process
from typing import Callable, Dict, List, Union

CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "config.json")


def load_config() -> Dict[str, Union[str, List[str]]]:
    """ Load config file """
    with open(CONFIG_FILE_PATH, encoding="utf-8") as f:
        config = json.load(f)
    return config


def modify_config(key: str, value: Union[str, List[str]]):
    """
    Modify config for (key, value) pair and Save

    :param key: (str) config key
    :param value: (str, List[str]) config value
    """
    config = load_config()
    config[key] = value

    with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


def run_background(function: Callable):
    """ Run function in backgroud """
    process = Process(target=function)
    process.start()
    os._exit(0)
