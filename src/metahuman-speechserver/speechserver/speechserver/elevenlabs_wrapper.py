import os
import json
import requests

from speechserver.config import config
#from elevenlabs import set_api_key

CHUNK_SIZE = 1024

headers = {
    'Accept': 'audio/mpeg',
    'Content-Type': 'application/json',
    'xi-api-key': config.elevenlabs_api_key 
}

def get_voices():
# {{{
    url = 'https://api.elevenlabs.io/v1/voices'
    headers = {
        'Accept': 'application/json',
        'xi-api-key': config.elevenlabs_api_key 
    }

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)

    path = os.path.join('./elevenlabs_voices.json')
    with open(path, 'w') as f:
        print(json.dumps(data, indent=2))
# }}}

def text_to_mp3(file_id, model_id, voice_id, text):
# {{{
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'

    headers = {
        'Accept': 'audio/mpeg',
        'Content-Type': 'application/json',
        'xi-api-key': config.elevenlabs_api_key
    }

    data = {
        'text': text,
        'model_id': model_id,
        'voice_settings': {
            'stability': 0.5,
            'similarity_boost': 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)
    path = os.path.join(config.audio_path, f'{file_id}.mp3')

    with open(path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

    return path
# }}}

