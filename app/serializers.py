from rest_framework.serializers import ModelSerializer, CharField, SlugRelatedField

from app.models import Game, Guess


class GuessSerializer( ModelSerializer ):
  class Meta:
    model = Guess
    fields = [ 'id', 'letter', 'correct' ]


class GameSerializer( ModelSerializer ):
  game_state = CharField( source='get_game_state_display' )

  guesses = SlugRelatedField( many=True, read_only=True, slug_field='letter' )

  class Meta:
    model = Game
    fields = [ 'id', 'game_state', 'word_state', 'guesses_incorrect', 'guesses_incorrect_remaining', 'guesses' ]
