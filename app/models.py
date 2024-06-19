from django.db.models import Model, BooleanField, CharField, PositiveSmallIntegerField, ForeignKey, CASCADE, TextChoices
from django.utils.translation import gettext_lazy as _


class GameState( TextChoices ):
  INPROGRESS = 'I', _( 'InProgress' )
  LOST = 'L', _( 'Lost' )
  WON = 'W', _( 'Won' )


class Game( Model ):
  word = CharField( max_length=10 )
  game_state = CharField( max_length=1, choices=GameState, default=GameState.INPROGRESS )
  guesses_incorrect = PositiveSmallIntegerField( default=0 )
  guesses_incorrect_max = PositiveSmallIntegerField()

  def __str__( self ):
    return f'Game {self.id} - {self.game_state}'

  def word_state( self ):
    guessed_letters = self.guesses.values_list( 'letter', flat=True )
    return ''.join([letter if letter in guessed_letters else '_' for letter in self.word])

  def remaining_incorrect_guesses( self ):
    return self.guesses_incorrect_max - self.guesses_incorrect

  def update_state( self ):
    if '_' not in self.word_state():
      self.game_state = GameState.WON
    elif self.remaining_incorrect_guesses() <= 0:
      self.game_state = GameState.LOST
    else:
      self.game_state = GameState.INPROGRESS
    self.save()


class Guess( Model ):
  game = ForeignKey( Game, related_name='guesses', on_delete=CASCADE )
  letter = CharField( max_length=1 )
  correct = BooleanField()

  def __str__( self ):
    return f'{self.letter} in Game {self.game.id} - {'Correct' if self.correct else 'Incorrect'}'
