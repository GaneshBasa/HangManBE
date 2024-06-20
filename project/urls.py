'''
URL configuration for project project.

The `urlpatterns` list routes URLs to  For more information please see:
  https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
  1. Add an import:  from my_app import views
  2. Add a URL to urlpatterns:  path('', home, name='home')
Class-based views
  1. Add an import:  from other_app.views import Home
  2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
  1. Import the include() function: from django.urls import include, path
  2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
'''
from django.urls import path

from app.views import greet, games_list, new_game, game_state, guess


urlpatterns = [
  path( '', greet ),
  path( 'games', games_list ),
  path( 'game/new', new_game ),
  path( 'game/<int:game_id>', game_state ),
  path( 'game/<int:game_id>/guess', guess )
]
