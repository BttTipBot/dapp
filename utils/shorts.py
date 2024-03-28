

# Create two methods that takes the address and return a short string
def get_short_address(address, length=5):
    return address[:length] + "..." + address[-length:]



# Create two methods that takes the address and return a short string
def get_short_tx(tx, length=5):
    return tx[:length] + "..." + tx[-length:]