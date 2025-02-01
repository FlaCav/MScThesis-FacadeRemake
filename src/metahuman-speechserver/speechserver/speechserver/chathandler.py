import wexpect
import time
from speechserver import argparser

child = None

def spawnchat():
    global child
    print("chathandler: spawning app")
    child = wexpect.spawn('cmd.exe')
    child.expect('>', timeout=5000)
    print(child.before)

def startchat():
    global child
    if child is None: print("is none")
    print("chathandler: starting chat")
    if argparser.get_args().game_version == "pre":
        child.sendline('python ./speechserver/autogen_chat_pre.py')
    else:
        child.sendline('python ./speechserver/autogen_chat.py')
    child.expect("Provide feedback to chat_manager. Press enter to skip and use auto-reply, or type 'exit' to end the conversation: ", timeout=5000)
    print(child.before)

def sendinput(input):
    global child
    print("chathandler: sending input")
    child.sendline(input)
    child.expect("Provide feedback to chat_manager. Press enter to skip and use auto-reply, or type 'exit' to end the conversation: ", timeout=5000)
    print(child.before)

def closechat():
    global child
    child.sendline("exit")
    child.expect('>', timeout=5000)
    child.sendline("exit")
    child.close()
    child = None
    print('exited')

def getchat():
    global child
    return child