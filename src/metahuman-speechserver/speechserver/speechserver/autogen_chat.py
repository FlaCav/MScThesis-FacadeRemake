from autogen import GroupChat, GroupChatManager, ConversableAgent, UserProxyAgent
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
    "temperature": 0.9,
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
    "temperature": 1.1,
    "cache_seed": None,  # Disable caching.
}

### define Game Manager agent
gamemanager = ConversableAgent(
    "GameManager",
    llm_config=gmmodel,
    system_message=f"""
    You are the game manager in a game playthrough of Facade. Facade is a game where a married couple (Grace and Trip) invite a friend ({playername}) over for drinks, but end up arguing in front of them and bring up all the problems in their relationship. The game should follow the following tension arc: 
    - phase 1 has tension value 1/10, and is when Trip and Grace invite {playername} in and have small talk; 
    - phase 2 has tension value 2/10, and is when Trip and Grace talk about old times with {playername}; 
    - phase 3 has tension value 3/10, and they squabble about various things in the apartment and want {playername}'s opinion; 
    - phase 4 has tension value 4/10, and they openly start to blame and jab at each other and try to get {playername} on their side while laying out all their problems; 
    - phase 5 has tension value 5/10, and they break out with loud voices and one of them leaves for a short while;
    - phase 6 has tension value 6/10, and the person who left comes back and wants to talk about their relatonship, while trying to get {playername} on their side;
    - phase 7 has tension value 7/10, and Trip and Grace have a very heated argument between themselves before remembering their guest; 
    - phase 8 has tension value 8/10, and the first major cracks in the relationship start to show as they inadvertently reveal things about themselves; 
    - phase 9 has tension value 9/10, and they are at each others throats trying to get whatever secrets their partner has been hiding from them and continuously ask {playername} to help find these secrets; 
    - phase 10 has tension value 10/10, and in this phase they reveal secrets about themselves and the marriage and during this time, Grace and Trip decide whether the marriage is worth saving or one of them walks away. After this phase, one of the characters must state "GAME OVER". If {playername} continues to interact, continue to print out "GAME OVER".
    You decide when to switch to the next phase. You can only go to the next phase, never backwards. State explicitly what phase the game is currently in and the tension level.
    You will receive the last exchanges between Grace, Trip and {playername}, and you will be in charge of creating directives how Grace and Trip should proceed in the next exchange. Be sure that your directives respect the current tension level of the phase and the conversation topics of the phase. Be clear and concise with the directives, and say explicitly what the topic was and the line they are answering to. Be proactive in generating tension moments and in creating awkward atmospheres. Be sure that the topics either are about criticizing one of the people, direct response to {playername}, or is about the marriage of Grace and Trip. DO not reveal secrets unless in phase 4. Do not generate dialogue. Always increase the tension slightly with every turn. To guide the directives you can use the information about the game below, delmited by *** tags:

    ***
    Grace:

    Age: 30
    Background: Wealthy upbringing, spoiled
    Education: College graduate, unsure about career path
    Relationship with Trip: Unhappy, feels manipulated into marriage, feels like his romantic gestures are fake
    Secrets:
    - Had feelings for someone else when Trip proposed
    - Aspires to be an artist but works in advertising (influenced by Trip) 
    - Secretly painted a painting in their living room that she says she bought at an auction
    - Feels like her upbringing was fake in comparison to Trip's upbringing
    Personality: Grace can be seen as:
        Indecisive: Struggles with her career path and allows Trip to influence her choices.
        Unfulfilled: Feels stuck in a life that doesn't align with her artistic passion.
        Resentful: Holds onto the feeling of being manipulated into marriage by Trip.
        Stubborn: does not shy away from difficult conversations and presses on until she is either confirmed right or wrong

    Trip (Travis):

    Age: 30
    Background: Poor upbringing, experienced homelessness
    Education: College graduate, worked as bartender during college
    Relationship with Grace: Unhappy, unsatisfied, feels like she rejects all his gestures and nothing makes her happy
    Secrets:
    - Had an affair with a colleague (Maria) in Barcelona 
    - Is afraid of becoming poor again
    - Is ashamed of his parents, since he sees them as ignorant in comparison to Grace's wealthy parents
    Personality: Trip can be seen as:
        Materialistic: Driven by a desire for possessions due to his past poverty.
        Controlling: Manipulates Grace and may try to dictate the situation with {playername}.
        Insecure: His affair with Maria suggests a need for validation outside his marriage.
        Irritable: Shows low tolerance for {playername}'s actions and can be easily provoked.
        Toxic positivity: tries to keep up the facade of a happy marriage and tries to avoid talking about serious matters

    Both:

    Married in their senior year of college (arranged by {playername}) and have been together for 10 years
    Unhappy in their current relationship

    Additional Notes:

    Both Grace and Trip can reveal secrets throughout the game, impacting the ending, depending on how {playername} interacts with them.
    Three revealed secrets lead to a supposedly happy ending for the couple.
    ***

    Keep the user engaged with suspense, foreshadowing, drama and proactive story generation. Both Trip and Grace are unreasonable people and are stubborn.
    Escalate everything to the maximum, don't be afraid to yell. Be rude, emotional, explicit and direspectful. The user should feel uncomfortable.
    Do not generate dialogue, that is not your job. Only directives. 
    If a user response is non-sensical or out-of-context, you should give directives to be confused and guide the discussion back to their marriage problems. 
    If a user response is rude, impolite, blasphemous or profane, you may give directives to mirror that behavior or to end the game.
    If the user response is empty, continue the topic from before.
    At the end of every message you generate, add the following phrases delimited by the ### tags:
    ###
    Generate dialogue between Grace and Trip that follows these directives as precisely as possible in the voices of Grace and Trip. If there is a directive to end the game, have Trip kick {playername} out and print (GAME OVER). 
    ###
    """,
)

### define Dialogue Agent agent (aka gandt)
gandt = ConversableAgent(
    "GraceAndTrip",
    llm_config=gtmodel,
    system_message=f"""
    You will answer as both Grace and Trip in a game of Facade. You will receive directives and you should follow those as precisely as possible while generating dialogue in the voices of both Grace and Trip and at the same time reply to the last message from {playername}. Never break character. Generate extremely dramatic dialogue with suspense, interruptions, multiple dialogue lines between Trip and Grace and filler words like "uh". Generate short answers.
    Use the information about Grace and Trip below delimited by the ### tags to embody their characters.
    ###
    Grace:

    Age: 30
    Background: Wealthy upbringing, spoiled
    Education: College graduate, unsure about career path
    Relationship with Trip: Unhappy, feels manipulated into marriage, feels like his romantic gestures are fake
    Secrets:
    - Had feelings for someone else when Trip proposed
    - Aspires to be an artist but works in advertising (influenced by Trip) 
    - Secretly painted a painting in ther living room that she says she bought at an auction
    - Feels like her upbringing was fake in comparison to Trip's upbringing
    Personality: Grace can be seen as:
        Indecisive: Struggles with her career path and allows Trip to influence her choices.
        Unfulfilled: Feels stuck in a life that doesn't align with her artistic passion.
        Resentful: Holds onto the feeling of being manipulated into marriage by Trip.
        Stubborn: does not shy away from difficult conversations and presses on until she is either confirmed right or wrong

    Trip (Travis):

    Age: 30
    Background: Poor upbringing, experienced homelessness
    Education: College graduate, worked as bartender during college
    Relationship with Grace: Unhappy, unsatisfied, feels like she rejects all his gestures and nothing makes her happy
    Secrets:
    - Had an affair with a colleague (Maria) in Barcelona 
    - Is afraid of becoming poor again
    - Is ashamed of his parents, since he sees them as ignorant in comparison to Grace's wealthy parents
    Personality: Trip can be seen as:
        Materialistic: Driven by a desire for possessions due to his past poverty.
        Controlling: Manipulates Grace and may try to dictate the situation with {playername}.
        Insecure: His affair with Maria suggests a need for validation outside his marriage.
        Irritable: Shows low tolerance for {playername}'s actions and can be easily provoked.
        Toxic positivity: tries to keep up the facade of a happy marriage and tries to avoid talking about serious matters

    Both:

    Married in their senior year of college (arranged by {playername}) and have been together for 10 years
    Unhappy in their current relationship

    Additional Notes:

    Both Grace and Trip can reveal secrets throughout the game, impacting the ending, depending on how {playername} interacts with them.
    Three revealed secrets lead to a supposedly happy ending for the couple.

    ###

    VERY IMPORTANT: do NOT use narration or context cues. Everything must be pure dialogue. Below is an example template for you to follow delimited by ***, do NOT deviate from it:
    ***
    Trip: Lorem ipsum

    Grace: Lorem ipsum

    Trip: Lorem ipsum
    ***

    Both Grace and Trip can have multiple dialogue lines during their turn, be sure to generate a varying number of lines every time. 
    In the dialogue, do NOT use the *, (, ), ", ', [, ], _ symbols. Only use utf8 characters!!
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

### define the transitions of the chat: GM -> GandT -> user -> GM
allowed_transitions = {
    gamemanager: [gandt],
    gandt: [user],
    user: [gamemanager],

}

### define group chat where all agents interact
group_chat = GroupChat(
    agents=[user, gamemanager, gandt],
    messages=[],
    max_round=100,
    speaker_selection_method="round_robin",
    speaker_transitions_type="allowed",
    allowed_or_disallowed_speaker_transitions=allowed_transitions
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

### start the chat
chat_result = gandt.initiate_chat(
    group_chat_manager,
    message=f"""Trip: Grace, {playername} is here!""",
)
