import os
from click import command 
import telebot
from pycoingecko import CoinGeckoAPI
from coins import coins
from newsapi import NewsApiClient
import time
from blockchain import *
from gnf import *
from spacing import *

newsapi = NewsApiClient(api_key='5753feb0897a4ff5a322ccd4289acede')
coin_client = CoinGeckoAPI()
API_KEY = os.environ.get('API_KEY')
bot = telebot.TeleBot("5587433203:AAEvScGpJH8VuCzwB0jaD6peNTru-P67X6k")
languages = ["ar","de","en","es","fr","he","it","nl","no","pt","ru","sv","ud","zh"]
blockchaincoins = ['btc', 'btc-testnet', 'ltc', 'doge', 'dash', 'bcy']
max_days = ["1","2","3","4","5","6","7","8","9","10"]

@bot.message_handler(commands=['commands'])
def commands(message):
    bot.send_message(message.chat.id, "Available commands:\n\n/info - Displays information about a coin, usage: /info <coin-here>\n\n/news - Displays news about a coin, usage: /news <coin-here> <language>\n\n/language - Displays all available languages, usage: /language\n\n/blockchainaddr - Displays all informaition about a bitcoin address/wallet, usage: /blochchainaddr <address> <coin-here>\n\n/blockchaintx - Displays all informaition about a bitcoin transaction, usage: /blochchaintx <transaction> <coin-here>\n\n/bchcoins - Displays all information about the networks available for the /blockchain... command, usage: /bchcoins\n\n/btcindex - Displays the Bitcoin Greed&Fear Index, usage: /btcindex <daysback (1 = Today)>")
    print("Commands sent")  
    spacing()


@bot.message_handler(commands=['btcindex'])
def btcindex(message):
    if len(message.text.strip().split()) == 2:
        if message.text.split()[1] in max_days:
            daysback = int(message.text.split()[1])
            gnf = greed_and_fear(daysback)
            for i in range(daysback):
                if i == 0:
                    bot.send_message(message.chat.id, f"[Day {i} (Today)]\n\nValue: {gnf[0][i]}\n\nValue Classification: {gnf[1][i]}\n\nTimestamp: {gnf[2][i]}\n")
                    print(f"[Day {i} (Today)]\n\nValue: {gnf[0][i]}\n\nValue Classification: {gnf[1][i]}\n\nTimestamp: {gnf[2][i]}\n")
                    spacing()

                else:
                    bot.send_message(message.chat.id, f"[Day -{i}]\n\nValue: {gnf[0][i]}\n\nValue Classification: {gnf[1][i]}\n\nTimestamp: {gnf[2][i]}\n")
                    print(f"[Day -{i}]\n\nValue: {gnf[0][i]}\n\nValue Classification: {gnf[1][i]}\n\nTimestamp: {gnf[2][i]}")
                    spacing()
        else:
            bot.send_message(message.chat.id, "Please enter a number between 1 and 10")
            print("Please enter a number between 1 and 10")
            spacing()

    else:
        bot.send_message(message.chat.id, "Please enter a number of days to look back.")
        print("Please enter a number of days to look back.")
        spacing()




@bot.message_handler(commands=['blockchainaddr'])
def blockchainwl(message):
    if len(message.text.strip().split()) == 3:
        address = message.text.strip(' ').split()[1]
        coin = message.text.strip(' ').split()[2]
        if coin in blockchaincoins:
            address = bk_details(address, coin)['address']
            total_received = satoshi_to_btc(bk_details(address, coin)['total_received'])
            total_sent = satoshi_to_btc(bk_details(address, coin)['total_sent'])
            balance = satoshi_to_btc(bk_details(address, coin)['balance'])
            unconfirmed_balance = satoshi_to_btc(bk_details(address, coin)['unconfirmed_balance'])
            final_balance = satoshi_to_btc(bk_details(address, coin)['final_balance'])
            tx_count = bk_details(address, coin)['n_tx']
            confirmed_time = bk_details(address, coin)['txrefs'][0]['confirmed']
            url = bk_details(address, coin)['tx_url']
            bot.send_message(message.chat.id, "Address: " + address + "\n" + "\n" + "Coin: " + coin + "\n" + "\n" + "Total Received: " + str(total_received) + "\n" + "\n" + "Total Sent: " + str(total_sent) + "\n" + "\n" + "Confirmed Balance: " + str(balance) + "\n" + "\n" + "Unconfirmed Balance: " + str(unconfirmed_balance) + "\n" + "\n" + "Final Balance: " + str(final_balance) + "\n" + "\n" + "Number of Transactions: " + str(tx_count) + "\n" + "\n" + "Last Tx Time: " + str(confirmed_time)[:19] + " (GMT+1)" + "\n" + "\n" + f"Last {coin} Transactions: " + url + "\n" + "\n" + "Blockchain Address: " + "https://blockchain.info/address/" + address)
            print("Address: " + address + "\n" + "\n" + "Coin: " + coin + "\n" + "\n" + "Total Received: " + str(total_received) + "\n" + "\n" + "Total Sent: " + str(total_sent) + "\n" + "\n" + "Confirmed Balance: " + str(balance) + "\n" + "\n" + "Unconfirmed Balance: " + str(unconfirmed_balance) + "\n" + "\n" + "Final Balance: " + str(final_balance) + "\n" + "\n" + "Number of Transactions: " + str(tx_count) + "\n" + "\n" + "Last Tx Time: " + str(confirmed_time)[:19] + " (GMT+1)"  + "\n" + "\n" + f"Last {coin} Transactions: " + url + "\n" + "\n" + "Blockchain Address: " + "https://blockchain.info/address/" + address)
            spacing()
        else:
            bot.reply_to(message, "Coin not supported, please use one of the following: /bchcoins")
            print("Coin not supported, please use one of the following: /bchcoins")
            spacing()
    else:
        bot.reply_to(message, "Usage: /blockchainaddr <address> <coin>, avalable coins: /bchcoins")
        print("Usage: /blockchainaddr <address> <coin>, avalable coins: /bchcoins")
        spacing()

@bot.message_handler(commands=['blockchaintx'])
def blockchaintx(message):
    if len(message.text.strip().split()) == 3:
        tx_hash = message.text.strip(' ').split()[1]
        coin = message.text.strip(' ').split()[2]
        if coin in blockchaincoins:
            block_hash = bk_transaction_details(tx_hash, coin)['block_hash']
            adresses = bk_transaction_details(tx_hash, coin)['addresses']
            total = satoshi_to_btc(bk_transaction_details(tx_hash, coin)['total'])
            fees = satoshi_to_btc(bk_transaction_details(tx_hash, coin)['fees'])
            total_received = total - fees
            preference = bk_transaction_details(tx_hash, coin)['preference']
            confirmations = bk_transaction_details(tx_hash, coin)['confirmations']
            confidance = bk_transaction_details(tx_hash, coin)['confidence']
            bot.send_message(message.chat.id, "Transaction Hash: " + tx_hash + "\n" + "\n" + "Coin: " + coin + "\n" + "\n" + "Block Hash: " + block_hash + "\n" + "\n" + "Addresses: " + str(adresses) + "\n" + "\n" + "Total: " + str(total) + "\n" + "\n" + "Fees: " + str(fees) + "\n" + "\n" + "Total Received: " + str(total_received) + "\n" + "\n" + "Preference: " + str(preference) + "\n" + "\n" + "Confirmations: " + str(confirmations) + "\n" + "\n" + "Confidence: " + str(confidance) + "\n" + "\n")
            print("Transaction Hash: " + tx_hash + "\n" + "\n" + "Coin: " + coin + "\n" + "\n" + "Block Hash: " + block_hash + "\n" + "\n" + "Addresses: " + str(adresses) + "\n" + "\n" + "Total: " + str(total) + "\n" + "\n" + "Fees: " + str(fees) + "\n" + "\n" + "Total Received: " + str(total_received) + "\n" + "\n" + "Preference: " + str(preference) + "\n" + "\n" + "Confirmations: " + str(confirmations) + "\n" + "\n" + "Confidence: " + str(confidance) + "\n" + "\n")
            spacing()
        else:
            bot.reply_to(message, "Coin not supported, please use one of the following: /bchcoins")
            print("Coin not supported, please use one of the following: /bchcoins")
            spacing()
    else:
        bot.reply_to(message, "Usage: /blockchaintx <tx_hash> <coin>, avalable coins: /bchcoins")
        print("Usage: /blockchaintx <tx_hash> <coin>, avalable coins: /bchcoins")
        spacing()

     
@bot.message_handler(commands=['bchcoins'])
def bchcoins(message):
    bot.reply_to(message, "Available coins: " + str(blockchaincoins))
    print("Available coins: " + str(blockchaincoins))
    spacing()





@bot.message_handler(commands=['info'])
def info(message):
    if len(message.text.strip().split()) == 2:
        coin = message.text.strip(' ').split()[1]
        print(f"The user requested info about {coin}:")
        print()
        if coin in coins:
            info = coin_client.get_coin_by_id(id=coin,localization='false', tickers='true', market_data='true', community_data='false', developer_data='false', sparkline='false')
            if info:
                current_homepage = info['links']['homepage'][0]
                current_blockchain = info['links']['blockchain_site'][0]
                current_forum = info['links']['official_forum_url'][0]
                current_subreddit = info['links']['subreddit_url']
                current_genesis = info['genesis_date']
                current_mc_rank = info['market_cap_rank']
                current_ath = info['market_data']['ath']['usd']
                current_ath = "${:,.2f}".format(current_ath)
                current_ath_change = round(info['market_data']['ath_change_percentage']['usd'], 2)
                current_ath_date = info['market_data']['ath_date']['usd'][:10]
                current_atl = info['market_data']['atl']['usd']
                current_atl = "${:,.2f}".format(current_atl)
                current_atl_change = round(info['market_data']['atl_change_percentage']['usd'], 2)
                current_atl_date = info['market_data']['atl_date']['usd'][:10]
                current_price = info['market_data']['current_price']['usd']
                current_price = "${:,.2f}".format(current_price)
                current_mcap = info['market_data']['market_cap']['usd']
                current_mcap = "${:,.2f}".format(current_mcap)
                current_24h = info['market_data']['high_24h']['usd']
                current_24h = "${:,.2f}".format(current_24h)
                current_24l = info['market_data']['low_24h']['usd']
                current_24l = "${:,.2f}".format(current_24l)
                current_totalsupply = info['market_data']['total_supply']
                current_totalsupply = "{:,.2f}".format(current_totalsupply)
                current_circsupply = info['market_data']['circulating_supply']
                current_circsupply = "{:,.2f}".format(current_circsupply)
                current_maxsupply = info['market_data']['max_supply']
                current_maxsupply = "{:,.2f}".format(current_maxsupply)
                bot.reply_to(message, f"Homepage: {current_homepage}\n\nBlockchain: {current_blockchain}\n\nForum: {current_forum}\n\nSubreddit: {current_subreddit}\n\nGenesis: {current_genesis}\n\nMarket cap rank: {current_mc_rank}\n\nAll time high: {current_ath}\n\nAll time high change: {current_ath_change}%\n\nAll time high date: {current_ath_date}\n\nAll time low: {current_atl}\n\nAll time low change: {current_atl_change}%\n\nAll time low date: {current_atl_date}\n\nPrice: {current_price}\n\n24h High: {current_24h}\n\n24 Low: {current_24l}\n\nMarket cap: {current_mcap}\n\nCirculating supply: {current_circsupply}\n\nTotal supply: {current_totalsupply}\n\nMax supply: {current_maxsupply}")

        else:
            bot.reply_to(message, text=f'Error, {coin} was not found, if the coin has two words use "-" instead of space')
            print(f'Error, {coin} was not found, if the coin has two words use "-" instead of space')
            spacing()
    else:
        bot.reply_to(message, text='Error, please use /info <coin>')
        print('Error, please use /info <coin>')
        print(f"Number of args: {len(message.text.strip().split())}")
        spacing()
@bot.message_handler(commands=['news'])
def news(message):
    if len(message.text.strip().split()) == 3:
        coin = message.text.strip(' ').split()[1]
        language = message.text.strip(' ').split()[2]
        print(f"The user requested news about {coin}:")
        print()
        if coin in coins and language in languages:
            top_headlines = newsapi.get_everything(q=coin, language=language, sort_by='relevancy', page_size=10)
            if top_headlines['totalResults'] > 3  and top_headlines['articles']:
                for i in range(0,3):
                    bot.reply_to(message, text=f"[{i+1}]\n\nTitle: {top_headlines['articles'][i]['title']}\n\nDescription: {top_headlines['articles'][i]['description']}\n\nURL: {top_headlines['articles'][i]['url']}\n\nPublished: {top_headlines['articles'][i]['publishedAt'][:10]}\n\n")
                    print()
                    print(f"Title: {top_headlines['articles'][i]['title']}")
                    print(f"Description: {top_headlines['articles'][i]['description']}")
                    print(f"URL: {top_headlines['articles'][i]['url']}")
                    print(f"Published in: {top_headlines['articles'][i]['publishedAt'][:10]}")
                    spacing()
                    if i == 2:
                        bot.reply_to(message, text="This function is still in alpha development, currently it only works well with top Market Cap coins.")
                        print("This function is still in alpha development, currently it only works well with top Market Cap coins.")
                        spacing()

            else:
                bot.reply_to(message, text=f'Error, {coin} has no articles')
                print(f'Error, {coin} has no articles')
                spacing()
        else:
            bot.reply_to(message, text=f'Error, {coin} was not found or language is not supported, if the coin has two words use "-" instead of space and if the language is not supported use /language')
            print(f'Error, {coin} was not found, if the coin has two words use "-" instead of space and if the language is not supported use /language')
            spacing()
    else:
        bot.reply_to(message, text='Error, please use /news <coin> <language>, for languages available use /languages')
        print('Error, please use /news <coin>')
        print(f"Number of args: {len(message.text.strip().split())}")
        spacing()

@bot.message_handler(commands=['language'])
def language(message):
    bot.reply_to(message, text='Possible language options: ar-de-en-es-fr-he-it-nl-no-pt-ru-sv-ud-zh.')
    print('Possible language options: ar-de-en-es-fr-he-it-nl-no-pt-ru-sv-ud-zh.')
    spacing()



if __name__ == '__main__':
    print('Initializing bot...')
    time.sleep(0.5)
    print('Bot is running...')
    time.sleep(0.5)
    print('waiting for commands...')
    time.sleep(0.5)
    print('available commands: /info <coin>')
    print('Press Ctrl+C to stop')
    print('Logs:')
    spacing()
    bot.polling()