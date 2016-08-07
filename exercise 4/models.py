"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

import random
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()


class Game(ndb.Model):
    """Game object"""
    game_over = ndb.BooleanProperty(required=True, default=False)
    current_bid_face = ndb.IntegerProperty()
    current_bid_number = ndb.IntegerProperty()
    user_one = ndb.KeyProperty(required=True, kind='User')
    user_two = ndb.KeyProperty(required=True, kind='User')
    user_turn = ndb.KeyProperty(required=True, kind='User')
    winner = ndb.KeyProperty(kind='User')
    """Player one's dice: dice_user_face"""
    dice_one_one = ndb.IntegerProperty(required=True)
    dice_one_two = ndb.IntegerProperty(required=True)
    dice_one_three = ndb.IntegerProperty(required=True)
    dice_one_four = ndb.IntegerProperty(required=True)
    dice_one_five = ndb.IntegerProperty(required=True)
    dice_one_six = ndb.IntegerProperty(required=True)
    """Player two's dice: dice_user_face"""
    dice_two_one = ndb.IntegerProperty(required=True)
    dice_two_two = ndb.IntegerProperty(required=True)
    dice_two_three = ndb.IntegerProperty(required=True)
    dice_two_four = ndb.IntegerProperty(required=True)
    dice_two_five = ndb.IntegerProperty(required=True)
    dice_two_six = ndb.IntegerProperty(required=True)

    @classmethod
    def new_game(user_one, user_two, dice):
        """Creates and returns a new game"""
        if dice < 1:
            raise ValueError('At least 1 die is needed to play.')
        user_one_dice = [random.randint(1,6) for i in range(dice)]
        user_one_dice_sorted = [0 for i in range(6)]
        for face in user_one_dice:
            user_one_dice_sorted[face-1]++
        user_two_dice = [random.randint(1,6) for i in range(dice)]
        user_two_dice_sorted = [0 for i in range(6)]
        for face in user_two_dice:
            user_two_dice_sorted[face-1]++
        game = Game(game_over=False,
                    current_bid_face=6,
                    current_bid_number=0,
                    user_one=user_one,
                    user_two=user_two,
                    user_turn=user_one,
                    dice_one_one=user_one_dice_sorted[0],
                    dice_one_two=user_one_dice_sorted[1],
                    dice_one_three=user_one_dice_sorted[2],
                    dice_one_four=user_one_dice_sorted[3],
                    dice_one_five=user_one_dice_sorted[4],
                    dice_one_six=user_one_dice_sorted[5],
                    dice_two_one=user_two_dice_sorted[0],
                    dice_two_two=user_two_dice_sorted[1],
                    dice_two_three=user_two_dice_sorted[2],
                    dice_two_four=user_two_dice_sorted[3],
                    dice_two_five=user_two_dice_sorted[4],
                    dice_two_six=user_two_dice_sorted[5])
        game.put()
        return game

    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.winner = self.winner.get().name
        form.user_one_name = self.user_one.get().name
        form.user_two_name = self.user_two.get().name
        form.user_turn = self.user_turn.get().name
        form.current_bid_face = self.key.form.current_bid_face()
        form.current_bid_number = self.key.form.current_bid_number()
        form.game_over = self.key.game_over()
        form.message = message
        return form

    def end_game(self, winner):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""
        self.game_over = True
        self.put()
        # Add the game to the score 'board'
        score = Score(user=self.user, date=date.today(), won=won,
                      guesses=self.attempts_allowed - self.attempts_remaining)
        score.put()


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    winner = messages.IntegerField(2)
    game_over = messages.BooleanField(3, required=True)
    message = messages.StringField(4, required=True)
    user_one = messages.StringField(5, required=True)
    user_two = messages.StringField(6, required=True)
    user_turn = messages.StringField(7, required=True)
    current_bid_face = messages.IntegerField(8)
    current_bid_number = messages.IntegerField(9)


class NewGameForm(messages.Message):
    """Used to create a new game"""
    user_one = messages.StringField(1, required=True)
    user_two = messages.StringField(2, required=True)
    dice = messages.IntegerField(3, default=5)


class RaiseBidForm(messages.Message):
    """Used to raise the bid in an existing game"""
    bid_face = messages.IntegerField(1, required=True)
    bid_number = messages.IntegerField(2, required=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
