from dotmap import DotMap
import json

config = None
with open('./config.json') as f:
    config = DotMap(json.loads(f.read()))
