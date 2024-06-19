from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from django.contrib.auth.models import Group, User

from app.models import Game


class UserSerializer( HyperlinkedModelSerializer ):
  class Meta:
    model = User
    fields = [ 'url', 'username', 'email', 'groups' ]


class GroupSerializer( HyperlinkedModelSerializer ):
  class Meta:
    model = Group
    fields = [ 'url', 'name' ]


class GameSerializer( ModelSerializer ):
  class Meta:
    model = Game
    fields = [ 'id', 'word', 'state', 'current_state_of_word', 'max_incorrect_guesses', 'incorrect_guesses', 'remaining_incorrect_guesses' ]
