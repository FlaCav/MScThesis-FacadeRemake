# MSc Thesis -- Facade Remake

This repo is a skeleton of my master's thesis project, where I replicated the game [Facade](https://www.playablstudios.com/facade) using GPT-4o, ElevenLabs, Audio2Face, Unreal Engine 5, and a Flask Python server. 

**The complete src folder can be found [here](https://e.pcloud.link/publink/show?code=XZEx6CZJjrCAft1rohTltQVr92cn81LPcY7).**

In this repo, the complete code for the server and the Audio2Face files can be found in the [metahuman-speechserver folder](./src/metahuman-speechserver/). The Unreal Engine project could not be uploaded to due the project size. Explanations on the code/UE project and how to run the game can be found in the [src README file](./src/README.md).

My master's thesis can be found in the [ETH Research Collection](https://www.research-collection.ethz.ch/handle/20.500.11850/695280). The abstract of the thesis can be found below.

## Thesis Abstract

Non-Player Characters (NPCs) play a crucial role in video games by adding depth to the
experience and guiding players through the story, but their interactions are usually limited to
preset dialogue trees. This approach has been the industry standard for many years without
significant developments, despite the major advances in Artificial Intelligence (AI) and their
application to other aspects of video game design. However, following recent breakthroughs in
the field of Natural Language Processing (NLP), small research projects, tech demos, and short
video games have begun experimenting with integrating Large Language Models (LLMs) into
dialogue generation for NPCs, offering new methods of interaction. This work explores the use
of multiple independent LLM instances to guide and create a story-driven conversation
between a player and multiple NPCs. A game demo, based on the video game Fac¸ade, was
developed as a proof of concept, and a user study was conducted to explore how players
perceive the conversations generated within the game. The results show that the large majority
of participants found the dialogue from our LLM version of the game more consistent, realistic,
engaging, interesting and interactive compared to the pre-scripted game version imitating the
original Fac¸ade game. Overall, the findings of this work show that player-NPC interactions
could be greatly enhanced by the use of LLMs and a prompting strategy that splits up the
responsibilities of story progression and dialogue generation. The contributions of this thesis
are a novel prompting strategy that facilitates interactive and responsive conversations with
game characters, a working game demo that implements the strategy, and a preliminary user
study into the perception of LLM-generated dialogues in video games.

