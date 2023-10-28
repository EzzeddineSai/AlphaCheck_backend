import requests

from flask import Flask, request, session
from flask_socketio import SocketIO
import time
import random
from gameclasses import *
import time
from config import *

#import logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, cors_allowed_origins='*', async_mode = 'eventlet')

@socketio.on('disconnect')
def handle_disconnection():
    return

def AI(game_state, legal_moves):
    move_resp = requests.post('https://alpha-check-model-0f35a09b177f.herokuapp.com/',json={'game state': game_state,'legal moves': legal_moves})
    move = move_resp.json()
    move_tuple = ((move[0][0],move[0][1]),(move[1][0],move[1][1]))
    print("AI chose move", move_tuple)
    game_master(move_tuple)

def game_master(move):
    last_played_piece = (move[0][0]+move[1][0],move[0][1]+move[1][1])
    session['game state object'].transition(move)
    game_state = session['game state object'].return_game_state()
    legal_moves = find_legal_moves(game_state['board'],
                                    game_state['player turn'],
                                    game_state['sequence piece'])
    print("player turn is for:",session['game state object'].player_turn)
    print(legal_moves)
    if session['game state object'].game_length == MAX_GAME_LEN:
        message = 'game length exceeded. Its a draw.'
        socketio.emit('update and play',{'game state': game_state,
                                'game ongoing': False,
                                'legal moves': legal_moves,
                                'last played piece': last_played_piece,
                                'message' : message
                                })
    elif len(legal_moves) == 0:
        print("game over")
        if session['game state object'].player_turn  !=  session['game state object'].human_player_color:
            message = 'you won'
        else:
            message = 'you lost'
        socketio.emit('update and play',{'game state': game_state,
                                'game ongoing': False,
                                'legal moves': legal_moves,
                                'last played piece': last_played_piece,
                                'message' : message
                                })
    else:
        if session['game state object'].player_turn  !=  session['game state object'].human_player_color:
            message = """AlphaCheck's turn"""
        else:
            message = 'your turn'


        if session['game state object'].player_turn  ==  session['game state object'].human_player_color:
            socketio.emit('update and play',{'game state': game_state,
                                'game ongoing': True,
                                'legal moves': legal_moves,
                                'last played piece': last_played_piece,
                                'message' : message
                                })
        else:
            socketio.emit('update and await',{'game state': game_state,
                                'game ongoing': True,
                                'legal moves': legal_moves,
                                'last played piece': last_played_piece,
                                'message' : message
                                })
            
@socketio.on('move chosen') # convert back to tuple
def handle_move_chosen(move):
    print("human move chosen:", move)
    move_tuple = ((move[0][0],move[0][1]),(move[1][0],move[1][1]))
    game_master(move_tuple)

@socketio.on('awaiting AI turn') # if human isn't the first player
def handle_awaiting_AI_turn():
    game_state = session['game state object'].return_game_state()
    legal_moves = find_legal_moves(game_state['board'],
                                    game_state['player turn'],
                                    game_state['sequence piece'])
    AI(game_state, legal_moves)
    time.sleep(0.5)


@socketio.on('awaiting AI start') # if human isn't the first player
def handle_awaiting_AI_start():
    game_state = session['game state object'].return_game_state()
    legal_moves = find_legal_moves(game_state['board'],
                                    game_state['player turn'],
                                    game_state['sequence piece'])
    AI(game_state, legal_moves)
    time.sleep(0.5)

@socketio.on('connect')
def handle_connection():
    print("\n\n\n","NEW GAME. request id:",request.sid, "\n\n\n")
    player_color = random.choice([-1,1])
    session['game state object'] = GameState(human_player_color=player_color)
    game_state = session['game state object'].return_game_state()

    if player_color == 1:
        message = 'Your turn'
    else:
        message = """AlphaCheck's turn"""

    socketio.emit('start game', {'player color': player_color, 'client data': {'game state': game_state,
                                 'game ongoing': True,
                                 'legal moves': find_legal_moves(game_state['board'],
                                    game_state['player turn'],
                                    game_state['sequence piece']),
                                 'message' : message
                                 }})