from django.db.models import Model, BooleanField, CharField, PositiveSmallIntegerField, ForeignKey, CASCADE, TextChoices
from django.utils.translation import gettext_lazy as _

class Game( Model ):
  class GameState( TextChoices ):
    INPROGRESS = 'I', _( 'InProgress' )
    LOST = 'L', _( 'Lost' )
    WON = 'W', _( 'Won' )

  word = CharField( max_length=10 )
  state = CharField( max_length=1, choices=GameState, default=GameState.INPROGRESS )
  incorrect_guesses = PositiveSmallIntegerField( default=0 )
  max_incorrect_guesses = PositiveSmallIntegerField()

  def __str__(self):
    return f'Game {self.id} - {self.state}'

  def current_state_of_word(self):
    guessed_letters = self.guesses.values_list('letter', flat=True)
    return ''.join([letter if letter in guessed_letters else '_' for letter in self.word])

  def remaining_incorrect_guesses(self):
    return self.max_incorrect_guesses - self.incorrect_guesses

  def update_state(self):
    if '_' not in self.current_state_of_word():
      self.state = 'Won'
    elif self.remaining_incorrect_guesses() <= 0:
      self.state = 'Lost'
    else:
      self.state = 'InProgress'
    self.save()


class Guess( Model ):
  game = ForeignKey(Game, related_name='guesses', on_delete=CASCADE)
  letter = CharField(max_length=1)
  correct = BooleanField()

  def __str__(self):
    return f'{self.letter} in Game {self.game.id} - {"Correct" if self.correct else "Incorrect"}'
