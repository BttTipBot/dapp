
from db.parameters import get_param
from constants.parameters import PARAMETER_WHITELIST_ADDRESS

# A function that reads PARAMETER_WHITELIST_ADDRESS and separates the token symbol and address : and the other tokens by |
def get_whitelist_addresses():
    whitelist_addresses = get_param(PARAMETER_WHITELIST_ADDRESS)
    tokens =  whitelist_addresses.split('|')

    whitelist_tokens= []
    for token in tokens:
        token_detail = token.split(':')
        if len(token_detail) == 2:
            whitelist_tokens.append({'symbol': '$' + token_detail[0].upper(), 'address': token_detail[1]})
    return whitelist_tokens

def get_whitelist_token_by_symbol(symbol):
    whitelist_address = get_param(PARAMETER_WHITELIST_ADDRESS)
    tokens =  whitelist_address.split('|')

    #if symbol has $ remove it
    if symbol[0] == '$':
        symbol = symbol[1:]

    if symbol.lower() == 'BTT'.lower():
        return {'symbol': 'BTT', 'address': 'BTT'}

    for token in tokens:
        token_detail = token.split(':')
        print("get_whitelist_token_by_symbol: token_detail", token_detail)

        if len(token_detail) == 2:
            if token_detail[0].lower() == symbol.lower():
                return {'symbol': '$' + token_detail[0].upper(), 'address': token_detail[1]} 
    return None

