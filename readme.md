# Crypto Data Tracker
#### Video Demo:  <https://www.youtube.com/watch?v=1zZc96iwJZg>


## Description:

First off, my goal with this bot was to gather all of the data that I could find that was badly displayed on the internet, then I wanted to filter and sort that information, and finally I wanted to get it displayed nice and simple in just one place.

The bot was built with the 
Telegram, News, Goingecko and Blockcypher API, 
and with the 
Telebot, Time, Os, Requests and Json libraries for Python

The way this project was implemented was that I gathered data from a database by doing an API call, then I filtered and sorted the data using Python, and finally I logged the process and displayed the data on the Telegram chat using the Telebot library.

The bot has 3 main responses for all of the commands depending on the case:

Firstlly, we've got when the command is used correctly
Secondly, we've got when the command is not using the parameters accordingly
And Finally, we've got when the user inputs the wrong amount of arguments

## Commands:

/info - Displays information about a coin, usage: /info <coin-here>

/news - Displays news about a coin, usage: /news <coin-here> <language>

/language - Displays all available languages, usage: /language

/blockchainaddr - Displays all information about an address/wallet, usage: /blochchainaddr <address> <coin-here>

/blockchaintx - Displays all information about a transaction, usage: /blochchaintx <transaction> <coin-here>

/bchcoins - Displays all information about the networks available for the /blockchain... command, usage: /bchcoins

/btcindex - Displays the Bitcoin Greed&Fear Index, usage: /btcindex <daysback (1 = Today)>


### NOTE: if the coin/network that you are trying to use has two words (eg: ethereum classic) replace the space with a semicolon (eg: ethereum-classic)


## Files: 

Main.py: It's where the main program its located

Blockchain.py: It's a shortcut to use the /blockchain…. Commands using the blockcipher library

Coins.py: It's basically just a for loop that lists all the coins on the Coingecko API

Gnf.py: It's a shortcut to use the /btcindex command using the requests and json lirbraries

News.py: It's a shortcut to use the /news command using the requests and json lirbraries

Spacing.py: It's another shortcut to save space and save time writing code on main.py

