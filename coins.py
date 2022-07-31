import os
from click import command 
import telebot
from pycoingecko import CoinGeckoAPI


coin_client = CoinGeckoAPI()
API_KEY = os.environ.get('API_KEY')
bot = telebot.TeleBot("5587433203:AAEvScGpJH8VuCzwB0jaD6peNTru-P67X6k")


coins = []
data = coin_client.get_coins_list()

count_list = []
# for  i in range(100000):
#     coins.append(data[i]['id'])

for i in data:
    coins.append(i['id'])
    
# x = len((data['name']))

# for i in range x:
#     coins.append()

