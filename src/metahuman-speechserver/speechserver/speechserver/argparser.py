import os
import sys
import argparse

def add_args():
    global argparser
    argparser = argparse.ArgumentParser(description='Speech Server')
    argparser.add_argument(
        '--host',
        action='store',
        dest='host',
        help='Server host',
        default='0.0.0.0'
    )
    argparser.add_argument(
        '--port',
        action='store',
        dest='port',
        help='Server port',
        type=int,
        default=50051
    )
    argparser.add_argument(
        '--logger',
        action='store',
        dest='logger',
        help='sets a logger',
        default=''
    )
    argparser.add_argument(
        '--loglevel',
        action='store',
        dest='loglevel',
        help='set log level',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        default='info'
    )
    argparser.add_argument(
        '-d',
        '--device_index',
        action='store',
        dest='device_index',
        help='device index',
        type=int,
        default=0
    )
    argparser.add_argument(
        '-g',
        '--game-version',
        action='store',
        dest='game_version',
        help='version of game',
        type=str,
        default="llm"
    )

    argparser.add_argument(
        '-uid',
        '--user-id',
        action='store',
        dest='user_id',
        help='id of the user playing the game',
        type=str,
        default="0000"
    )

add_args()
args = argparser.parse_args()

def get_args():
    global args
    return args