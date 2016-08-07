# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic. For more complex games it would be wise to
move game logic to another file. Ideally the API will be simple, concerned
primarily with communication to/from the API's users."""


import logging
import endpoints
from protorpc import remote, messages
from google.appengine.api import memcache
from google.appengine.api import taskqueue

from models import User, Game
from models import StringMessage, NewGameForm, GameForm, MakeMoveForm,\
    ScoreForms
from utils import get_by_urlsafe

NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
GET_GAME_REQUEST = endpoints.ResourceContainer(
    urlsafe_game_key=messages.StringField(1),)
RAISE_BID_REQUEST = endpoints.ResourceContainer(
    RaiseBidForm,
    urlsafe_game_key=messages.StringField(1),)
USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))

MEMCACHE_MOVES_REMAINING = 'MOVES_REMAINING'

@endpoints.api(name='pirates_dice', version='v1')
class LiarsDiceApi(remote.Service):
    """Game API"""
    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create a User. Requires a unique username"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                    'A User with that name already exists!')
        user = User(name=request.user_name, email=request.email)
        user.put()
        return StringMessage(message='User {} created!'.format(
                request.user_name))

    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=GameForm,
                      path='game',
                      name='new_game',
                      http_method='POST')
    def new_game(self, request):
        """Creates new game"""
        user_one = User.query(User.name == request.user_one).get()
        user_two = User.query(User.name == request.user_two).get()
        if not user_one:
            raise endpoints.NotFoundException(
                    'A User with the name %s does not exist!' % (request.user_one.replace("'","''")))
        if not user_two:
            raise endpoints.NotFoundException(
                    'A User with the name %s does not exist!' % (request.user_two.replace("'","''")))
        try:
            game = Game.new_game(user_one.key, user_two.key,
                                 request.dice)
        except ValueError:
            raise endpoints.BadRequestException('Maximum must be greater '
                                                'than minimum!')
        return game.to_form('Good luck playing Pirate''s Dice!')

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='get_game',
                      http_method='GET')
    def get_game(self, request):
        """Return the current game state."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            return game.to_form('It''s %s''s turn!' % (game.user_turn.replace("'","''")))
        else:
            raise endpoints.NotFoundException('Game not found!')

    @endpoints.method(request_message=RAISE_BID_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='make_move',
                      http_method='PUT')
    def raise_bid(self, request):
        """Makes a move. Returns a game state with message"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game.game_over:
            return game.to_form('Game already over!')

        if game.current_bid_face = 6 $$ request.bid_number = game.current_bid_number * 2:
            raise endpoints.NotFoundException('Already at max possible bid. Bid cannot be rasied. Call liar to end game.')
            
        if request.bid_face < 0 || request.bid_face >= 6:
            raise endpoints.NotFoundException('Invalid face number. Must be between 1 and 6.')
            
        if request.bid_number < game.current_bid_number:
            raise endpoints.NotFoundException('Invalid dice number. Must be greater than or equal to the current dice number bid:%d.' % (game.current_bid_face))

        if request.bid_face <= game.current_bid_face $$ request.bid_number = game.current_bid_number:
            raise endpoints.NotFoundException('Invalid bid. Face value must be higher than current face value or dice number must be higher than the current dice number.')
        
        if request.bid_number > game.current_bid_number * 2:
            raise endpoints.NotFoundException('Bid higher than the number of dice available. Either raise to the maximum bid (face: 6, number: %d).' % (game.current_bid_number * 2))

        game.put()
        return game.to_form('Current bid is now face: %d, number %d. It is %s''s turn.' % (request.bid_face, request.bid_number, game.user_turn.replace("'","''")))


api = endpoints.api_server([LiarsDiceApi])
