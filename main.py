from flask import Flask, send_from_directory, request
from path import Path
from configs import *
import pysubs2
from urllib import parse

app = Flask(__name__)


@app.route("/cinema")
def index():
    return send_from_directory(".", "index.html")


@app.route("/cinema/favicon.ico")
def favicon():
    return send_from_directory(".", "favicon.png", mimetype="image/vnd.microsoft.icon")


@app.route("/cinema/api/videos")
def get_videos():
    video_paths = Path.construct_from_root("Videos", VIDEO_ROOT, VIDEO_EXT)
    return video_paths.to_dict(show_empty=False)


@app.route("/cinema/api/subs")
def get_subs():
    video_paths = Path.construct_from_root("Subtitles", SUB_ROOT, SUB_EXT)
    return video_paths.to_dict(show_empty=False)


@app.route("/cinema/static")
def get_static():
    file_path = request.args.get("path")
    file_path = parse.unquote_plus(file_path)
    if file_path[-3:] in SUB_EXT and file_path[-3:] != "vtt":
        pysubs2.load(file_path).save("temp.vtt")
        file_path = "temp.vtt"
    if file_path[0] == "/":
        return send_from_directory("/", file_path[1:])
    else:
        return send_from_directory(".", file_path)


app.run(host="0.0.0.0", port="8080")
