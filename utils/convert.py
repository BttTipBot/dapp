import re

def convert_to_int(amount):
    # Remove any characters other than digits, 'k', 'm', or 'b'
    amount = re.sub(r'[^0-9kmbKMB.]', '', amount)

    # Check for k, m, or b
    if 'k' in amount.lower():
        return int(float(amount.replace('k', '').replace('K', '')) * 1000)
    elif 'm' in amount.lower():
        return int(float(amount.replace('m', '').replace('M', '')) * 1000000)
    elif 'b' in amount.lower():
        return int(float(amount.replace('b', '').replace('B', '')) * 1000000000)
    else:
        return int(float(amount))  # Convert to float first to remove decimals, then convert to int

def is_int(amount):
    # Any number of digits followed by an optional decimal point and an optional 'k', 'm', or 'b' is valid integer

    if re.match(r'^\d+(\.\d+)?[kKmMbB]?$', amount):
        return True
    else:
        return False
