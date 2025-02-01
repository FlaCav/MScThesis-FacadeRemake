## Speechserver 
This folder contains the code to run the server connecting OpenAI, Audio2Face and the Unreal project. The server runs on localhost. To change the IP address or the port, see [speechserver/argparser.py](./speechserver/argparser.py).

To run the server, make sure the packages in requirements.txt are installed correctly. After activating the venv, run ``` python main.py ```.

At the moment it is not possible to run the server in a virtual environment due to a [known issue with wexpect](https://stackoverflow.com/questions/68302352/wexpect-in-a-python-virtual-environment). 

## IMPORTANT
This code assumes the API keys are stored in [config.json](./config.json) in this folder. 

```Wexpect``` is used to initiate a cmd.exe terminal in [the chathandler.py](./speechserver/chathandler.py). This is Windows specific. To run on Linux, you would need to substitute this with ```pexpect```.

### From the NVIDIA tutorial
For the [Audio2Face Python example](https://www.youtube.com/watch?v=qKhPwdcOG_w) to work install (these are already in the requirements.txt):
```
google
protobuf===3.20.3
google-cloud
google-api-core
grpcio
numpy
soundfile
```
