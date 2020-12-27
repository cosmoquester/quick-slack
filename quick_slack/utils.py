import json
import os

CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "config.json")


def load_config():
    with open(CONFIG_FILE_PATH) as f:
        config = json.load(f)
    return config


def modify_config(key, value):
    config = load_config()
    config[key] = value

    with open(CONFIG_FILE_PATH, "w") as f:
        json.dump(config, f, indent=4)
