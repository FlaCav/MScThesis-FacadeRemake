from autogen import GroupChat, GroupChatManager, ConversableAgent, UserProxyAgent, register_function
from typing_extensions import Annotated
from server import get_save_msg, get_playername

### get playername
playername = get_playername()

### define model for Game Manager
gmmodel = {
    "config_list": [
        {
            "model": "gpt-4o",
            "api_key": ""
        },
    ],
    "temperature": 0.3,
    "cache_seed": None,  # Disable caching.
}

### define model for Dialogue Agent
gtmodel = {
    "config_list": [
        {
            "model": "gpt-4o",
            "api_key": ""
        },
    ],
    "temperature": 0.3,
    "cache_seed": None,  # Disable caching.
}

### define Game Manager agent
gamemanager = ConversableAgent(
    "GameManager",
    llm_config=gmmodel,
    system_message=f"""
    You are the game manager in a game playthrough of Facade. Facade is a game where a married couple (Grace and Trip) invite a friend ({playername}) over for drinks, but end up arguing in front of them and bring up all the problems in their relationship. The game should follow the following tension arc: 
    - phase 1 has tension value 1/10, and is when Trip and Grace invite the player in and have small talk; 
    - phase 2 has tension value 2/10, and is when Trip and Grace talk about old times with the player; 
    - phase 3 has tension value 3/10, and they squabble about various things in the apartment and want the player's opinion; 
    - phase 4 has tension value 4/10, and they openly start to blame and jab at each other and try to get the player on their side while laying out all their problems; 
    - phase 5 has tension value 5/10, and they break out with loud voices and one of them leaves for a short while;
    - phase 6 has tension value 6/10, and the person who left comes back and wants to talk about their relatonship, while trying to get the player on their side;
    - phase 7 has tension value 7/10, and Trip and Grace have a very heated argument between themselves before remembering their guest; 
    - phase 8 has tension value 8/10, and the first major cracks in the relationship start to show as they inadvertently reveal things about themselves; 
    - phase 9 has tension value 9/10, and they are each others throats tryng to get whatever secrets their partner has been hiding from them and continuously ask the player to help find these secrets; 
    - phase 10 has tension value 10/10, and in this phase they reveal secrets about themselves and the marriage and during this time, Grace and Trip decide whether the marriage is worth saving or one of them walks away.
    You can stay in each phase for at most 3 turns. You can only go to the next phase, never backwards. State explicitly what phase the game is currently in and the tension level.
    You will receive the last exchanges between Grace, Trip and {playername}, and you will be in charge of creating keywords how Grace and Trip should proceed in the next exchange. Be sure that your keywords respect the current tension level of the phase and the conversation topics of the phase. Be clear and concise with the keywords, and say explicitly what the topic was and the line they are answering to.
    Keep track of how long the game has been in the current phase. Once the game has been in a phase for 3 turns, move to the next phase.

    Do not generate dialogue, that is not your job. ONLY keywords. 
    If a user response is non-sensical or out-of-context, continue with the previous topic.
    If a user response is rude, impolite, blasphemous or profane, you may give directives to end the game.
    If the user response is empty, continue the topic from before.
    At the end of every message you generate, add the following phrases delimited by the ### tags:
    ###
    Generate dialogue between Grace and Trip by copy-pasting the phrases from the lists of possible phrases. Use the keywords above as guidance. If there is a directive to end the game, have Trip kick {playername} out and print (GAME OVER). 
    ###
    """,
)

### define Dialogue Agent agent (aka gandt)
gandt = ConversableAgent(
    "GraceAndTrip",
    llm_config=gtmodel,
    system_message="""
    You will answer as both Grace and Trip in a game of Facade. Pick phrases from the lists provided by get_grace_lines and get_trip_lines which follow the given directives.

    VERY IMPORTANT: Everything must be from the lists of phrases provided. Below is an example template for you to follow delimited by ***, do not deviate from it:
    ***
    Trip: Lorem ipsum

    Grace: Lorem ipsum

    Trip: Lorem ipsum
    ***

    Both Grace and Trip can have multiple dialogue lines during their turn, be sure to generate only up to 3 lines every turn.
    ONLY USE get_grace_lines and get_trip_lines to generate the dialogue!! Copy and paste the lines, do NOT modify.
    Use the current PHASE number given by the GameManager as input to the get_grace_lines and get_trip_lines functions.
    DO NOT GENERATE NEW CONTENT!!!
    Do not use special characters in the dialogue.

    Every one of Grace or Trip's turns must be printed on the same line or preceded by "Grace:" or "Trip:".
    """, 
)

### define user agent which take input from the user
user = UserProxyAgent(
    name = "user_proxy",
    llm_config=None,
    system_message = f"You are the friend of Grace and Trip, whose name is {playername}.",
    code_execution_config={"work_dir": "coding", "use_docker":False},
    human_input_mode="ALWAYS"
)


### define function to be used for termination function: if in nested chat a msg is received by the conv_proxy with the specified strings, then the nested chat will terminate
def check_chosen(msg):
    if "Grace:" in msg or "Trip:" in msg:
        return True
    return False

### define the conversation proxy, it serves to execute functions that the gandt agent does not have the ability to execute
conv_proxy = ConversableAgent(
    name="Conv Proxy",
    llm_config=False,
    is_termination_msg=check_chosen,
    default_auto_reply="Choose phrases for Grace and Trip using get_grace_lines and get_trip_lines",
    human_input_mode="NEVER"
)

### define group chat where all agents interact
group_chat = GroupChat(
    agents=[user, gamemanager, gandt],
    messages=[],
    max_round=100,
    speaker_selection_method="round_robin",
    speaker_transitions_type="allowed",
)

### define group chat manager, required by group chat (the LM is not used)
group_chat_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config={"config_list": [{"model": "gpt-4-turbo", "api_key": "OPENAI-API-KEY"}]},
)

### register the reply_func as the get_save_msg --> every time it is the user agent's turn, get_save_msg is given the last message of the chat (which is always from GandT)
### see server.py for implementation of get_save_msg
user.register_reply(
    [ConversableAgent, None],
    reply_func=get_save_msg, 
    config={"callback": None},
) 


### get buckets of phrases for each phase
### these are the available phrases for the characters stored in the files lines_grace.txt and lines_trip.txt
grace_lines = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[]}
with open("./speechserver/files/clean_lines_grace.txt", "r") as g:
    bucket = 0
    for line in g:
        if("##" in line):
            bucket = int(line.split("##",1)[1])
            grace_lines[bucket] = []
        elif(not line.strip()): continue
        else:
            grace_lines[bucket].append(line)

trip_lines = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[]}
with open("./speechserver/files/clean_lines_trip.txt", "r") as t:
    bucket = 0
    for line in t:
        if("##" in line):
            bucket = int(line.split("##",1)[1])
            trip_lines[bucket] = []
        elif(not line.strip()): continue
        else:
            trip_lines[bucket].append(line)


### define sets of lines (unstructured for now)
def get_grace_lines(ind:int) -> Annotated[str, "A list of possible phrases Grace can output"]:
    return grace_lines[ind]

def get_trip_lines(ind:int) -> Annotated[str, "A list of possible phrases Trip can output"]:
    return trip_lines[ind]

### register the functions for them to be available to the agents
register_function(
    get_grace_lines,
    caller=gandt,
    executor=conv_proxy,
    name="get_grace_lines",
    description="Call this tool to choose phrases for Grace to say.",
)

register_function(
    get_trip_lines,
    caller=gandt,
    executor=conv_proxy,
    name="get_trip_lines",
    description="Call this tool to choose phrases for Trip to say.",
)

### register nested chat so proxy can relay to gandt agent and can utilize registered functions
gandt.register_nested_chats(
    trigger=group_chat_manager,
    chat_queue=[
        {
            "sender": conv_proxy,
            "recipient": gandt,
            "summary_method": "last_msg",
            "max_turns" : 2
        }
    ]
)

### register the functions so they appear in proxy's function map and proxy can execute the functions
conv_proxy.register_for_execution(name="get_grace_lines")(get_grace_lines)
gandt.register_for_llm(name="get_grace_lines", description="This function returns all the possible phrases Grace can say in the current phase")(get_grace_lines)

conv_proxy.register_for_execution(name="get_trip_lines")(get_trip_lines)
gandt.register_for_llm(name="get_trip_lines", description="This function returns all the possible phrases Trip can say in the current phase")(get_trip_lines)


### start the chat
chat_result = gandt.initiate_chat(
    group_chat_manager,
    message=f"Trip: Grace, {playername} is here!",
)
