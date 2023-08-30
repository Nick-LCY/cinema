import os, yaml

with open("configs.yaml", "r") as file:
    yaml_obj = yaml.load(file, Loader=yaml.CLoader)
default_settings = {}


def get_config(key: str) -> str:
    if os.getenv(key) is not None:
        if "," in os.getenv(key):
            return os.getenv(key).split(",")
        return os.getenv(key)
    if key in yaml_obj:
        return yaml_obj[key]
    return default_settings[key]

VIDEO_ROOT = get_config("video_root")
SUB_ROOT = get_config("sub_root")
VIDEO_EXT = get_config("video_ext")
SUB_EXT = get_config("sub_ext")
