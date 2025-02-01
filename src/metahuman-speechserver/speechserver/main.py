import os
import json
from threading import Thread

from speechserver.argparser import args
from speechserver import chatgpt
from speechserver import stt
from speechserver import server
from speechserver import elevenlabs_wrapper
from speechserver import chathandler

if __name__ == "__main__":
    chathandler.spawnchat()
    print("spawned")
    # Start the Flask server: 
    server.app.run(
        host=args.host,
        port=args.port
    )
    