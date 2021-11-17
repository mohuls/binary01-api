from django.urls import path

from .views import *

urlpatterns = [
    path('binary01/', room, name='room'),
    path('login/', login, name="login"),
    path('signup/', signup, name="signup"),
    path('send-msg/', send_msg, name="send_msg"),
    path('get-msg/', get_msg, name="get_msg"),
    path('mining-data/', mining_data, name="mining_data"),
    path('get-mining-data/', get_mining_data, name="get_mining_data"),
    path('get-user-data/', get_user_data, name="get_user_data"),
    path('airdrop-add-token/', airdrop_add_token, name="airdrop_add_token"),
    
]
