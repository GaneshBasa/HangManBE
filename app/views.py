from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from random import choice
from math import ceil

from app.models import GameState, Game, Guess
from app.serializers import GameSerializer

WORDS = [ 'Hangman', 'Python', 'Audacix', 'Bottle', 'Pen' ]


@api_view()
def greet( request ):
  return Response({ 'message': 'Hello from Django HangMan App BackEnd' })


@api_view()
def games_list( request ):
  games = Game.objects.all()
  serialized_games = GameSerializer( games, many=True ).data
  return Response( serialized_games )


@api_view()
def new_game( request ):
  selected_word = choice( WORDS ).upper()
  guesses_incorrect_max = ceil( len( selected_word ) / 2 )
  
  game = Game.objects.create( word=selected_word, guesses_incorrect_max=guesses_incorrect_max )

  return Response( { 'id': game.id }, status=status.HTTP_201_CREATED )


@api_view()
def game_state( request, game_id ):
  try:
    game = Game.objects.get( pk=game_id )
  except Game.DoesNotExist:
    return Response( status=status.HTTP_404_NOT_FOUND )

  serialized_game = GameSerializer( game ).data
  
  return Response( serialized_game )


@api_view( [ 'POST' ] )
def guess( request, game_id ):
  try:
    game = Game.objects.get( pk=game_id )
  except Game.DoesNotExist:
    return Response( status=status.HTTP_404_NOT_FOUND )
  
  if game.game_state != GameState.INPROGRESS:
    return Response( { 'error': f'Game State - { game.get_game_state_display() }' }, status=status.HTTP_400_BAD_REQUEST )

  if letter := request.data.get( 'letter' ):
    letter = letter.upper()
  else:
    return Response( { 'error': 'Missing Letter' }, status=status.HTTP_400_BAD_REQUEST )

  if not letter.isalpha() or len(letter) != 1:
    return Response( { 'error': 'Invalid Letter' }, status=status.HTTP_400_BAD_REQUEST )

  serialized_game = GameSerializer( game ).data

  if letter in serialized_game.get('guesses'):
    return Response( { 'error': 'Repeated Letter' }, status=status.HTTP_400_BAD_REQUEST )

  correct = letter in game.word
  if not correct:
    game.guesses_incorrect += 1
  
  Guess.objects.create( game=game, letter=letter, correct=correct )

  game.update_state()

  serialized_game = GameSerializer( game ).data

  serialized_game.update({ 'correct': correct })

  return Response( serialized_game )
