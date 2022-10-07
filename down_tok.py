"""
setup & requirements.txt
python3 -m pip install TikTokApi
python3 -m playwright install
python3 -m pip install ffmpeg-python
run brew install ffmpeg
"""
from TikTokApi import TikTokApi
import os
import requests
import ffmpeg
import whisper

def get_full_url(base_url):
    r = requests.get(base_url)
    return r.url

def get_id(link):
    id_idx = link.rfind("/")
    id = link[id_idx+1:]
    print(id)
    return id

def down_tik_tok(id):
    with TikTokApi() as api:
        video = api.video(id=id)

        # Bytes of the TikTok video
        video_data = video.bytes()

        with open("out.mp4", "wb") as out_file:
            out_file.write(video_data)

        video = ffmpeg.input("out.mp4")

        audio = video.audio

        stream = ffmpeg.output(audio, "out.mp3")
        ffmpeg.run(stream)
        return

def get_transcript():
    model = whisper.load_model("base")
    result = model.transcribe("out.mp3")
    print(result["text"])
    return result
# print(result["text"])

link = "https://www.tiktok.com/@basicfinancialliteracy/video/7151537228211080490"
full_url = get_full_url(link)
id = get_id(link)
down_tik_tok(id)
transcript = get_transcript()