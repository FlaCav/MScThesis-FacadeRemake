import os
import subprocess

from speechserver.config import config

def play_wav(path):
    subprocess.call([
        'python',
        config.audio2face_client_path,
        path,
        config.audio2face_prim_path]
    )

def play_wav_grace(path):
    subprocess.call([
        'python',
        config.audio2face_client_path_grace,
        path,
        config.audio2face_prim_path_grace]
    )

def play_wav_trip(path):
    subprocess.call([
        'python',
        config.audio2face_client_path_trip,
        path,
        config.audio2face_prim_path_trip]
    )