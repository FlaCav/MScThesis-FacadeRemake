import json
import re

                
## append lines to log_file and tempunreal.json to be read
def append_lines(file):
    with open(file, 'a', encoding="utf8") as f:
        with open('./speechserver/files/templines.jsonl', 'r',  encoding="utf8") as t:
                for line in t:
                    jl = json.loads(line)
                    dial = jl["name"] + ": " + jl["dialogue"] #string
                    f.write(dial + "\n")

## add user input
def add_input(file, input):
    with open(file, 'a', encoding="utf8") as f:
        f.write("user: " + input + "\n")
