import base64
import os
import re
import time
import json
import random
import uuid
import datetime
from urllib.parse import unquote
from concurrent.futures import ThreadPoolExecutor
import flask
from flask import Flask, request, make_response, send_file
from flask import render_template
from flask_cors import CORS
import speech_recognition as sr

from speechserver import audio2face 
from speechserver import elevenlabs_wrapper as el 
from speechserver import chatgpt
from speechserver import stt
from speechserver.config import config
import speechserver.argparser as argparser
from speechserver import chathandler
from speechserver import chatparser

executor = ThreadPoolExecutor(max_workers=20)

### global vars ###
log_file = None
flag = None
###

app = Flask(__name__)
CORS(app)

### function to delete the audio files 90 seconds after they were created, should be enough time for it to be played back
def delete_after(path, seconds=90, max_files=10):
# {{{
    print(f'Deleting after {seconds}')
    time.sleep(seconds)
    print(f'Deleting {path}')
    if os.path.exists(path):
        os.remove(path)

    # Clean if more files than max_files:
    files = [f for f in os.listdir(config.audio_path) if (f.endswith('.wav') or f.endswith('.mp3'))]
    if len(files) > max_files:
        for f in files:
            os.remove(os.path.join(config.audio_path, f))
# }}}


############# CODE FOR REMOTE SERVER ##############


### plays an audio file through audio2face, no text
### only for debugging purposes
@app.route('/audio2face_static', methods=['POST'])
def say_static():
# {{{
    path = request.form.get('path')

    # Create audio2face subprocess:
    audio2face.play_wav(path)
    
    # Return file path:
    return json.dumps({'path': path})
# }}}

### the player name is received and saved in files/tempname.json 
### return value is not used in Unreal
@app.route('/sendname', methods=['GET', 'POST'])
# {{{
def sendname():
    f = request.form.get('playername')
    file = open('./speechserver/files/tempname.json', 'w', encoding='utf8')
    file.write(json.dumps({"name" : f}))
    file.close()

    return json.dumps({"status": "ok"})
# }}}

### the two flags (local [stored in tempflag] and from Unreal app) are compared; if local flag is different, then new dialogue line is available and is sent to Unreal app
### return value is used in Unreal; either new dialogue line or 'abort'
@app.route('/flagstatus', methods=['GET', 'POST'])
# {{{
def flagstatus():
    global flag
    f =  unquote(request.form.get('flag'))
    with open('./speechserver/files/tempflag.json', 'r', encoding='utf8') as flag:
        line = flag.read()
        #print("*** line: " + line + " *** f : " + f) ## uncomment for debugging
        fstat = json.loads(line)
        if (f == "true" and fstat['flag'] == False) or (f == "false" and fstat['flag'] == True):
            with open("./speechserver/files/tempunreal.json", "r") as file:
                data = file.read()
                return data
        else:
            return json.dumps({"status": "abort"})
# }}}

### the log file for the current gameplay is created, then the Autogen chat is started and the first line appended to the log
### return value is not used in Unreal
@app.route('/startchat', methods=['GET', 'POST'])
# {{{
def startchat():
    # create log for this stageplay before starting the chat
    global log_file

    namefile = open("./speechserver/files/tempname.json", "r")
    namejs = namefile.read()
    name = json.loads(namejs)['name']
    namefile.close()

    # create the log file name, will be stored in the 'Stageplays' folder
    date = datetime.datetime.now()
    formated_string = date.strftime("%d-%m-%Y--%H%M")
    log_file = f"./speechserver/stageplays/Stageplay--{argparser.get_args().user_id}--{argparser.get_args().game_version}--{formated_string}.txt"
    with open(log_file, 'a+') as f: pass

    # write to the flag file to synchronize reading with Unreal application
    flag = open('./speechserver/files/tempflag.json', 'w', encoding='utf8')
    data = {'flag' : False}
    flag.write(json.dumps(data))
    flag.close()

    #start the autogen chat and append first line
    print("starting")
    chathandler.startchat()
    print("started")
    chatparser.append_lines(log_file)
    print("appended")

    return json.dumps({'status': "ok"})
# }}}

### the Autogen chat is closed gracefully
### no return value
@app.route('/endchat', methods=['GET', 'POST'])
# {{{
def endchat():
    chathandler.closechat()
# }}}

### the input from the user is received and sent to the Autogen chat, then the input and the chat response are appended to the log file
### return value is not used in Unreal
@app.route('/autogenchat', methods=['POST'])
def say_autogen():
# {{{
    global log_file
    global flag

    # unpack prompt from POST request
    prompt = unquote(request.form.get('prompt'))

    # write to the flag file to synchronize reading with Unreal application
    flag = open('./speechserver/files/tempflag.json', 'w', encoding='utf8')
    data = {'flag' : False}
    flag.write(json.dumps(data))
    flag.close()

    # give prompt to autogen chat - see @get_save_msg for what happens when reading the generated chat response
    chathandler.sendinput(prompt)

    # append lines of input and chat response
    chatparser.add_input(log_file, prompt)
    chatparser.append_lines(log_file)
    print("appended")

    return json.dumps({"status" : "ok"})
# }}}


##### LOCAL FUNCTIONS #####


model_id = "eleven_multilingual_v2"
grace_voice_id = "JolzjVeaSE5CBOGYtPtJ"
trip_voice_id = "IQ2zVrjvWD0QNIm93GRv"

### is called from autogen_chat.py and autogen_chat_pre.py after every output from gandt agent (=== Dialogue Agent)
### reply_func method for autogen agents to record the responses
### return values are given by Autogen documentation and GitHub issue threads (do not change)
def get_save_msg(recipient, messages, sender, config):
    #global flag
    text = messages[-1]['content']
    splitls = text.split('\n')
    data = {'flag' : False}

    with open('./speechserver/files/templines.jsonl', 'w', encoding="utf8") as f:
        for line in splitls:
            if line == '' or line == "": continue
            match = re.match(r'^([^:]+):\s*(.*)$', line)
            if match:
                name, dialogue = match.groups()
                g = open('./speechserver/files/tempunreal.json', 'w', encoding="utf8")
                g.write(json.dumps({"name" : name , "dialogue" : dialogue}))
                g.close()

                flag = open('./speechserver/files/tempflag.json', 'w', encoding='utf8')
                data['flag'] = not data['flag']
                flag.write(json.dumps(data))
                flag.close()

                if name == "Grace":
                    path = el.text_to_mp3(str(uuid.uuid4()), model_id, grace_voice_id, dialogue)
                    audio2face.play_wav_grace(path)
                else:
                    path = el.text_to_mp3(str(uuid.uuid4()), model_id, trip_voice_id, dialogue)
                    audio2face.play_wav_trip(path)
                
                executor.submit(delete_after, path)
                f.write(json.dumps({"name" : name , "dialogue" : dialogue}) + '\n')

    return False, None

### function to retrieve the player's given name
def get_playername():
    with open('./speechserver/files/tempname.json', 'r', encoding='utf8') as file:
        line = file.read()
        dname = json.loads(line)
    return dname["name"]


####### ORIGINAL SERVER, THESE FUNCTIONS ARE NOT USED #######

@app.route('/')
def main():
# {{{
    response = make_response('Please use /stt or /chatgpt to invoke API requests')
    response.mimetype = 'text/plain'
    return response
# }}}

@app.route('/status', methods=['GET', 'POST'])
# {{{
def status():
    return json.dumps({'status': 'ok'})
# }}}

@app.route('/stt', methods=['POST'])
def stt_route():
# {{{
    # Create file UUID to avoid clashes on parallel requests: 
    _id = str(uuid.uuid4())
    # Create the create the filename based on the UUID: 
    filename = f'{_id}.wav'
    file = request.files.get('audio')
    path = os.path.join(serverconfig.audio_path, filename)

    # write the audio file to the server file system:
    with open(path, 'wb') as f:
        f.write(file.read())

    # Speech to text:
    text = stt.wav_to_text(str(path))

    # Submit a delete request:
    executor.submit(delete_after, path)

    # Return result:
    return json.dumps({'text': text})
# }}}

@app.route('/audio2face', methods=['POST'])
def say():
# {{{
    prompt = unquote(request.form.get('prompt'))
    model_id = request.form.get('model_id')
    voice_id = request.form.get('voice_id')

    messages = []
    message = {
        'role': 'user',
        'content': prompt
    }
    messages.append(message)
    chatgpt.completion(messages)
    text = messages[-1]['content']

    # Create audio file:
    _id = str(uuid.uuid4())
    path = el.text_to_mp3(_id, model_id, voice_id, text)

    # Create audio2face subprocess:
    audio2face.play_wav(path)

    # Submit file delete:
    executor.submit(delete_after, path)
    
    # Return file ID:
    return json.dumps({'id': _id})
# }}}


@app.route('/tts_elevenlabs', methods=['POST'])
def tts_elevenlabs_route():
# {{{
    # Extract input data:
    #character = json.loads(request.form.get('character'))
    text = request.form.get('text')
    model_id = request.form.get('model_id')
    voice_id = request.form.get('voice_id')

    # Create audio file:
    _id = str(uuid.uuid4())
    path = el.text_to_mp3(_id, model_id, voice_id, text)

    # Submit file delete:
    executor.submit(delete_after, path)
    
    # Return file ID:
    return json.dumps({'id': _id})
# }}}

@app.route('/completion', methods=['POST'])
def completion():
# {{{
    chat = json.loads(request.form.get('chat'))
    messages = chat['messages']
    chatgpt.completion(messages)
    return json.dumps({'chat': chat})
# }}}

@app.route('/audio', methods=['GET'])
def audio():
# {{{
    #_id = request.args.get('id')
    file_id = request.args.get('file_id')
    path = os.path.join(config.audio_path, f'{file_id}')
    return send_file(path, as_attachment=True)
# }}}


