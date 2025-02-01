import os
import pathlib
import random
#from playsound import playsound
from speechserver.configuration import serverconfig

class NonVerbalProviderCharacterNotFoundException(Exception):
    def __init__(self, character):
        self.message = f"NonVerbalProvider Error! Character not found: {character}"
        super().__init__(self.message)

class NonVerbalProvider:

    def __init__(self):

        self.audio = {}

        # get folders
        flist = []
        for p in pathlib.Path(serverconfig.nonverbal_db).iterdir():
            if p.is_dir():
                flist.append(p)

        # check for audio files
        for f in flist:
            c_name = f.stem
            files = os.listdir(f)
            for file in files:
                if file.endswith(".wav"):
                    if not c_name in self.audio.keys():
                        self.audio[c_name] = []
                    self.audio[c_name].append(f / file) 

    
    def get_audio(self, character, message):
        if not character in self.audio.keys():
            raise NonVerbalProviderCharacterNotFoundException(character)
        
        return random.choice(self.audio[character]) 


    def get_bytes(self, character, message):
        path = self.get_audio(character, message)

        with open(path,"rb") as b:
            return b.read()

