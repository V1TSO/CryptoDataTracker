import blockcypher

def satoshi_to_btc(satoshi):
    """
    Converts a Satoshi value to BTC.
    """
    return satoshi / 100000000

def bk_details(address, coin):
    """
    Returns the details of a blockchain address.
    """
    return blockcypher.get_address_details(address, coin_symbol=coin)

def bk_transaction_details(tx_hash, coin):
    """
    Returns the details of a blockchain transaction.
    """
    return blockcypher.get_transaction_details(tx_hash, coin_symbol=coin)


#print(satoshi_to_btc(bk_details("1HMrorU5wR14kB5NVxHa1EcKdCoxswfBie", 'btc').get('balance')))
# print(bk_transaction_details('7876b6ca87947753f6605eaa0632a7ae253507125b80b2a4ce24f0899d4ec689', 'btc'))

