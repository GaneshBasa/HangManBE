from django.contrib.auth.models import Group, User
from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from random import choice
from math import ceil

from app.models import Game, Guess
from app.serializers import GroupSerializer, UserSerializer, GameSerializer

WORDS = [ 'Hangman', 'Python', 'Audacix', 'Bottle', 'Pen' ]


class UserViewSet( ModelViewSet ):
  # API endpoint that allows users to be viewed or edited
  queryset = User.objects.all().order_by( '-date_joined' )
  serializer_class = UserSerializer
  permission_classes = [ permissions.IsAuthenticated ]


class GroupViewSet( ModelViewSet ):
  # API endpoint that allows groups to be viewed or edited
  queryset = Group.objects.all().order_by( 'name' )
  serializer_class = GroupSerializer
  permission_classes = [ permissions.IsAuthenticated ]


class GameViewSet( ModelViewSet ):
  # API endpoint that allows games to be viewed or edited
  queryset = Game.objects.all()
  serializer_class = GameSerializer
  permission_classes = [ permissions.AllowAny ]


@api_view()
def new_game( request ):
  selected_word = choice( WORDS )
  max_incorrect_guesses = ceil( len( selected_word ) / 2 )
  game = Game.objects.create( word=selected_word, max_incorrect_guesses=max_incorrect_guesses )
  return Response( { 'id': game.id }, status=status.HTTP_201_CREATED )


@api_view()
def game_state( request, game_id ):
  try:
    game = Game.objects.get(pk=game_id)
  except Game.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  game.update_state()
  data = {
    'state': game.state,
    'current_word_state': game.current_state_of_word(),
    'incorrect_guesses': game.incorrect_guesses,
    'remaining_incorrect_guesses': game.remaining_incorrect_guesses()
  }
  return Response(data, status=status.HTTP_200_OK)


@api_view( [ 'POST' ] )
def guess( request, game_id ):
  try:
    game = Game.objects.get(pk=game_id)
  except Game.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  letter = request.data.get('letter').upper()
  if not letter.isalpha() or len(letter) != 1:
    return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)

  correct = letter in game.word
  if not correct:
    game.incorrect_guesses += 1

  Guess.objects.create(game=game, letter=letter, correct=correct)
  game.update_state()

  data = {
    'state': game.state,
    'current_word_state': game.current_state_of_word(),
    'incorrect_guesses': game.incorrect_guesses,
    'remaining_incorrect_guesses': game.remaining_incorrect_guesses(),
    'guess_correct': correct
  }

  return Response(data, status=status.HTTP_200_OK)
