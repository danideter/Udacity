import sys
import random

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, inspect

Base = declarative_base()

# Will add users table in app engine project


class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    password = Column(String(80), nullable=False)
    players = Column(Integer, nullable=False)
    wild = Column(Integer, nullable=False)
    bid_player = Column(Integer, nullable=False)
    bid_face = Column(Integer, nullable=False)
    bid_number = Column(Integer, nullable=False)


class Player(Base):
    __tablename__ = 'player'
    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship(Game)
    id = Column(Integer, primary_key=True)
    player_number = Column(Integer, nullable=False)


class Dice(Base):
    __tablename__ = 'dice'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.id'))
    player = relationship(Player)
    face = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)


engine = create_engine('sqlite:///liarsdice.db')


def createDB():
    """Use to initiate database file"""
    Base.metadata.create_all(engine)


def connect():
    """Used in multiple methods to make a database connection"""
    Base.metadata.bind = engine
    return sessionmaker(bind=engine, autoflush=True)()


def startGame(password, players, dice_per_player, dice_sides, wild):
    """startGame(password, players, dice_per_player, dice_sides, wild)
        start a game of liar's dice.
        args:
            password: the password to access the game *does not do anything yet
            players: the number of players in the game. Must be greater than or
                equal to 1.
            dice_per_plaer: the number of dice per player. Typically 5 for a
                3-4 player game.
            dice_sides: the number of sides (or faces) on a die. Typically 6
            wild: Which side of the dice is considered wild. If no wild wanted,
            enter 0."""
    """Example of CREATE in sqlAlchemy"""
    session = connect()
    game = Game(password=password, players=players, wild=wild,
                bid_player=1, bid_face=0, bid_number=1)
    session.add(game)
    session.commit()
    for player_number in range(0, players):
        player = Player(game_id=game.id, game=game,
                        player_number=player_number+1)
        session.add(player)
        session.commit()
        dice_array = [0]*dice_sides
        for die in range(0, dice_per_player):
            roll = random.randrange(0, dice_sides, 1)
            dice_array[roll] += 1
        for face, total in enumerate(dice_array):
            if total != 0:
                session.add(Dice(player_id=player.id, player=player,
                                 face=face+1, total=total))
                session.commit()
    print ("Game started! Your id is " + str(game.id) +
           " and your password is " +
           str(game.password) + ". Please keep these safe!")
    engine.dispose()


def getGame(game_id):
    """gives general info about a game such as what the bid is and who the last
        bidder was.
        args:
            game_id: the id of the game to inspect. Given when the game is
            started with startGame()"""
    """Example of READ in sqlAlchemy"""
    session = connect()
    game = session.query(Game).filter_by(id=game_id).first()
    print "Properties for game " + str(game.id) + ":"
    for column in Game.__table__.columns:
        print str(column.key) + ": " + str(game.__dict__[column.key])
    engine.dispose()


def getDice(game_id, player_number):
    """gets a player's dice in a particular game
        args:
            game_id: the id of the game to inspect. Given when the game is
                started with startGame()
            player_number: the turn order of the plater in the game"""
    """Example of JOIN in sqlAlchemy"""
    session = connect()
    dice = (session.query(Dice)
            .join(Player)
            .join(Game)
            .filter(Game.id == game_id)
            .filter(Player.player_number == player_number)
            .all())
    print ("Dice for player " + str(player_number) + " in game " +
           str(game_id) + ".")
    for die in dice:
        print "face: " + str(die.face) + "      total: " + str(die.total)
    engine.dispose()
    return dice


def raiseBid(game_id, die_face, die_total):
    """For this varient of liars dice, either the face value must increase with
    the total resetting to 1, or the face value can remain the same with the
    total increasing. Since this is a test example, there are no checks in
    place to make sure the raise bid isn't more then possible.
    On the other hand, that might be interesting for players not noticing that
    a bid isn't phyically capable of happening.
        args:
            game_id: the id of the game to inspect. Given when the game is
                started with startGame()
            die_face: the face on the die to raise the bid to.
            die_total: the number of dice to raise the bid to."""
    """Example of UPDATE in sqlAlchemy"""
    session = connect()
    game = session.query(Game).filter_by(id=game_id).first()
    # Check if raised bid is valid
    valid = True
    if die_face < game.bid_face:
        valid = False
        print ("Invalid bid: New bid face must be greater than or equal to"
               "previious bid face.")
    if die_face == game.bid_face and die_total <= game.bid_number:
        valid = False
        print "Invalid bid: If not raising bid face, must raise bid number"
    if die_total < 1:
        valid = False
        print "Invalid bid: Die number must be greater than or equal to one"
    if valid:
        game.bid_face = die_face
        game.bid_number = die_total
        # Update player info
        if game.bid_player == game.players:
            game.bid_player = 1
        else:
            game.bid_player += 1
        session.add(game)
        session.commit()
        game = session.query(Game).filter_by(id=game_id).first()
        print ("Raised bid for game " + str(game.id) + ".\nThe bid is now " +
               str(game.bid_number) + " dice with a face of " +
               str(game.bid_face) + " showing. ")
        if game.wild > 0:
            print str(game.wild) + "'s are wild."
        print "It is player " + str(game.bid_player) + "'s turn."
    engine.dispose()


def callLiar(game_id):
    """call the last player a liar. This ends the game.
        args:
            game_id: the id of the game to inspect. Given when the game is
                started with startGame()"""
    """For fun :). Call previous player a liar to end game"""
    session = connect()
    game = session.query(Game).filter_by(id=game_id).first()
    # Initialize dice count
    dice_total = 0
    for player in range(1, game.players + 1):
        dice = getDice(game_id, player)
        for die in dice:
            if die.face == game.bid_face or die.face == game.wild:
                dice_total += die.total

    previous_player = game.bid_player - 1
    if previous_player == 0:
        previous_player = game.players

    # Print what bid was
    print ("Player " + str(previous_player) + " said there were " +
           str(game.bid_number) + " dice with a face of " +
           str(game.bid_face) + " showing. The actual total was " +
           str(dice_total) + ".")

    if dice_total < game.bid_number:
        print ("Player " + str(previous_player) + " lied! Player " +
               str(game.bid_player) + " wins!")
    else:
        print ("Player " + str(previous_player) + " told the truth! Player " +
               str(previous_player) + " wins!")
    engine.dispose()


def deleteGame(game_id):
    """delete a game, never to see it again.
        args:
            game_id: the id of the game to inspect. Given when the game is
                started with startGame()"""
    session = connect()
    game = session.query(Game).filter_by(id=game_id).first()
    print "Deleting game " + str(game.id) + "..."
    # Delete related items in dice table
    dice = (session.query(Dice)
            .join(Player)
            .join(Game)
            .filter(Game.id == game_id)
            .all())
    for die in dice:
        session.delete(die)
        session.commit()
    # Delete related items in player table
    players = (session.query(Player)
               .join(Game)
               .filter(Game.id == game_id)
               .all())
    for player in players:
        session.delete(player)
        session.commit()
    # Finalley delete game
    session.delete(game)
    session.commit()
    engine.dispose()
    print "Game deleted."
