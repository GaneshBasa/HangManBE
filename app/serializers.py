from rest_framework.serializers import ModelSerializer

from app.models import Game


class GameSerializer( ModelSerializer ):
  class Meta:
    model = Game
    fields = [ 'id', 'word', 'state', 'current_state_of_word', 'max_incorrect_guesses', 'incorrect_guesses', 'remaining_incorrect_guesses' ]
