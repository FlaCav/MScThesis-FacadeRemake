# Notes on the code

The src folder contains the repos for the Unreal Apartment scene and the Speechserver. 
Below are instructions how to set up the server, A2F and the Unreal Engine scene. At the end there are instructions how to run the game. 

Details on how to set up the Python environment for the server can be found in [the speechserver folder](./metahuman-speechserver/speechserver/).

## Speechserver

The Speechserver code is the most recent working code for the server and is meant to be run on a remote computer. The IP addresses in both the server and the Unreal project (BP_FirstPersonCharacter) need to be revised and changed if necessary. The Unreal blueprint should have the IP address of the computer running the server.

The Audio2Face files are also included in the metahuman-speechserver. There are two files, one for each character: [Grace's file](./metahuman-speechserver/Facade_Grace_instance.usd) and [Trip's file](./metahuman-speechserver/Facade_Trip_instance.usd). Each file needs to be opened in individual A2F instances (i.e. open the app twice to have two windows running). The Grace file should be opened on the app that was opened first, then Trip's on the second. This is due to the listening ports. These can be checked via various tools to see which app is listening on which port. 

The Audio2Face client script, whose default path can be found under "audio2face_client_path" in [the config file](./metahuman-speechserver/speechserver/config.json), should be copied twice, once for the Grace instance and once for the Trip instance. The two files should differ in the listening ports. I used 50051 (default) for the Grace instance and 50052 for the Trip instance. If the files are opened on the wrong instance (e.g. Trip's file opened on the instance listening on port 50051), then there will be problems sending and playing audio. This is because the individual "audio2face_prim_path" (also in the config file) for each character will not match.

Audio2Face has to be run on the same computer as the server (otherwise GPU overload with both Unreal and Audio2Face on the same computers). The IP addresses need to be changed for the A2F files as well. The IP address can be found n the StreamLiveLink configurations near the middle/bottom. This needs to be set to the IP of the computer running the Unreal scene. 

The configs in the [config file](./metahuman-speechserver/speechserver/config.json) of the server need to be double checked. The paths for the A2F client python scripts and the names of the A2F instances may be different. The APIs for OpenAI and ElevenLabs need to be inserted for the dialogue and audio generation to work.

The voice IDs need to be changed for the audio generation to work as well. These can be found in the [server.py](./metahuman-speechserver/speechserver/speechserver/server.py) under the variables grace_voice_id and trip_voice_id. To clone the voices of Grace and Trip from the game, the script [clone_voices.py](./metahuman-speechserver/get_voices/clone_voices.py) can be used. Audio samples can be taken from the following Youtube videos for [Grace's voice](https://www.youtube.com/watch?v=vXCzfhacVi0) and [Trip's voice](https://www.youtube.com/watch?v=CtuKUBV7g1Y).

## Unreal Engine Game Project

After cloning the repo, to open the scene in Unreal: open Unreal Engine 5.3, then browse to the [Unreal Project file](/src/unreal-facade-apartment-scene/Apartment.uproject) and open it. It can happen that the program tells you some Omniverse plugins are outdated and you must build the project manually. The solution for this is to recopy the ACE plugin from the Audio2Face files (the path should be similar to the following: ```C:\Users\your-username\AppData\Local\ov\pkg\audio2face-2023.2.0\ue-plugins\audio2face-ue-plugins\ACEUnrealPlugin-5.3```). For this folder to be present, Audio2Face 2023.2.0 needs to be installed. Delete the [ACE folder in the Plugins folder](./unreal-facade-apartment-scene/Plugins/ACE/) and replace it with a fresh copy from the aforementioned path. When opening the project again, there should be no problems. If there are, consult the official docs for the Audio2Face Omniverse UE plugins.  

All the logic for connecting to the server is in the file BP_FirstPersonCharacter.uasset. The IP address needs to be changed in the Async POST request nodes, as mentioned previously. 

For the Unreal scene to be connected to A2F, a Live Link window needs to be opened. When adding a new connection, match the ports with those set in the A2F files. If running multiple A2F instances (like was done for this project, hence two A2F files), then do not forget to have the ports and A2F instance names be different from each other. 

## How to run

To run the server, make sure the Audio2Face instances are already running and set up with the correct files. In the Audio2Face instances, once the file has been loaded, go to the tab "Audio2Face Tool" on the right of the window, then under the "Audio Player Streaming" section, right click on the large audio bar and select "Play example track". ![Example track image](./example-track.jpg "Example track") Do it for both A2F instances, otherwise the audio files cannot be run. Then go to the Omnigraph node called audio2face, go to StreamLivelink, open it. At the bottom of the window, the Stream LiveLink Node should be visible. Click the "Activate" box. ![Activate image](./activate.jpg "activate") This makes the instance visible to Unreal Engine. Do this for both instances. Check that the ports and IP addresses are set and are distinct for both A2F instances. Check that the subject names of the instances are the same as the prim_paths in [the config file](./metahuman-speechserver/speechserver/config.json). You can see this in the Stream Livelink Node. ![Ports image](./ports-a2f.jpg "ports")  Check that the instances are listening on the correct ports. If the A2F client script for Grace is listening on port 50051, check using a network tool that the Grace A2F file was opened on the A2F instance listening on port 50051. This causes cryptic errors when it isn't set up correctly.

In the Unreal Engine scene, check for each MetaHuman that they are listening for the right A2F connection. You can see this when clicking on one of the MetaHumans, then scrolling down the Details window to the Live Link section. ![MetaHuman details image](./unreal-live-link-mh.jpg "Live Link")

Open the server folder in a terminal and navigate to the [main.py file](./metahuman-speechserver/speechserver/main.py). Run `python main.py` and make sure the server is ready to receive calls. The default options are the LLM version of the game and the userid `0000`. To change these, see [argparser.py](./metahuman-speechserver/speechserver/speechserver/argparser.py).

Now if the setup of the IP addresses and of Unreal, A2F and the server were done correctly, the game should run correctly when pressing the 'Play' button in Unreal. After the game starts, in the top left corner a small message should show up saying either the connection to the server has been established or failed. If it connected, soon a message from Trip should show up greeting the player. Responses to user inputs usually appear 2-5 seconds after submission. Enjoy!

# Known bugs

- Grace has male voice: usually happens when name formatting deviates from the given template (pre scripted version has tendency to write \**Grace:**); when this happens, the name is not matched with 'Grace', and the default speaker is Trip

- audio but no text and input bar is visible: fetching loop in Unreal BP_FirstPersonCharacter is over due to very long LLM response and not enough iterations (-> fix: can increase iterations)

- text glitch: GUI not optimized/fixed, possibly some settings with the text wrapping need to be changed

- phrases not from file: LLM has low but not 0.0 temperature, sometimes it actually generates own input based on user input and GM keywords/directives (about autogen_chat_pre.py)

- early termination (end menu shows up but story is not yet over): probably 'end game keywords' were used by the characters in the dialogue
