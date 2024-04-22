
from db.parameters import create_or_update_param
from constants.parameters import (
    PARAMETER_WELCOME_BONUS,
    PARAMETER_MINIMUM_FEES,
    PARAMETER_MINIMUM_WITHDRAW_BTT,
    PARAMETER_TIP_FEE_BTT,
    PARAMETER_RAIN_FEE_BTT,
    PARAMETER_AIRDROP_FEE_BTT,
    PARAMETER_MIN_AMOUNT_JOKE,
    PARAMETER_WHITELIST_ADDRESS,
    PARAMETER_TIP_STANDARD_MESSAGE_1,
    PARAMETER_TIP_STANDARD_MESSAGE_2,
    PARAMETER_TIP_STANDARD_MESSAGE_3,
    PARAMETER_TIP_STANDARD_MESSAGE_4,
    PARAMETER_TIP_STANDARD_MESSAGE_5,
    PARAMETER_TIP_STANDARD_MESSAGE_6,
    PARAMETER_TIP_STANDARD_MESSAGE_7,
    PARAMETER_TIP_STANDARD_MESSAGE_8,
    PARAMETER_TIP_STANDARD_MESSAGE_9,
    PARAMETER_TIP_SILVER_MESSAGE_1,
    PARAMETER_TIP_SILVER_MESSAGE_2,
    PARAMETER_TIP_SILVER_MESSAGE_3,
    PARAMETER_TIP_SILVER_MESSAGE_4,
    PARAMETER_TIP_SILVER_MESSAGE_5,
    PARAMETER_TIP_SILVER_MESSAGE_6,
    PARAMETER_TIP_SILVER_MESSAGE_7,
    PARAMETER_TIP_SILVER_MESSAGE_8,
    PARAMETER_TIP_SILVER_MESSAGE_9,
    PARAMETER_TIP_GOLD_MESSAGE_1,
    PARAMETER_TIP_GOLD_MESSAGE_2,
    PARAMETER_TIP_GOLD_MESSAGE_3,
    PARAMETER_TIP_GOLD_MESSAGE_4,
    PARAMETER_TIP_GOLD_MESSAGE_5,
    PARAMETER_TIP_GOLD_MESSAGE_6,
    PARAMETER_TIP_GOLD_MESSAGE_7,
    PARAMETER_TIP_GOLD_MESSAGE_8,
    PARAMETER_TIP_GOLD_MESSAGE_9,
    PARAMETER_TIP_EMOJI_GOLD,
    PARAMETER_TIP_EMOJI_SILVER,
    PARAMETER_TIP_EMOJI_STANDARD,

)

# Define the parameter ID and value
all_params = [
    {"param_id": PARAMETER_WELCOME_BONUS, "value": 300},
    {"param_id": PARAMETER_MINIMUM_FEES, "value": 100},
    {"param_id": PARAMETER_MINIMUM_WITHDRAW_BTT, "value": 100000},
    {"param_id": PARAMETER_TIP_FEE_BTT, "value": 5},
    {"param_id": PARAMETER_RAIN_FEE_BTT, "value": 100},
    {"param_id": PARAMETER_AIRDROP_FEE_BTT, "value": 100},
    {"param_id": PARAMETER_MIN_AMOUNT_JOKE, "value": 1000},
    {"param_id": PARAMETER_TIP_EMOJI_STANDARD, "value": "🥴"},
    {"param_id": PARAMETER_TIP_EMOJI_SILVER, "value": "🥈"},
    {"param_id": PARAMETER_TIP_EMOJI_GOLD, "value": "🥇"},
    {"param_id": PARAMETER_WHITELIST_ADDRESS, "value": "htx:0x31161bc5DaC078dbae525a4fd3b362Fd440658b8|"},
    {"param_id": PARAMETER_TIP_STANDARD_MESSAGE_1, "value": "Mmm... Tips. The bacon of the currency world!"},
    {"param_id": PARAMETER_TIP_STANDARD_MESSAGE_2, "value": "Woo-hoo! With this tip, I can finally buy that inflatable donut for the pool!"},
    {"param_id": PARAMETER_TIP_STANDARD_MESSAGE_3, "value": "Ah, the sweet sound of tips... like music to my doughnut-loving ears."},
    {"param_id": PARAMETER_TIP_STANDARD_MESSAGE_4, "value": "If tips were donuts, I'd be Homer Simpson, the billionaire."},
    {"param_id": PARAMETER_TIP_STANDARD_MESSAGE_5, "value": "Thank you, thank you! I promise not to spend this tip all in one donut shop... but no guarantees."},
    {"param_id": PARAMETER_TIP_STANDARD_MESSAGE_6, "value": "With great tips come great responsibilities... like buying more beer!"},
    {"param_id": PARAMETER_TIP_STANDARD_MESSAGE_7, "value": "Tip me once, shame on you. Tip me twice, woo-hoo! I'm getting rich!"},
    {"param_id": PARAMETER_TIP_STANDARD_MESSAGE_8, "value": "Who needs a piggy bank when you've got a tip jar? Mmm... bacon."},
    {"param_id": PARAMETER_TIP_STANDARD_MESSAGE_9, "value": "You know you're living the dream when tips rain down like sprinkles on a donut."},
    {"param_id": PARAMETER_TIP_SILVER_MESSAGE_1, "value": "They say money can't buy happiness, but have you ever seen me sad with a pocket full of tips?"},
    {"param_id": PARAMETER_TIP_SILVER_MESSAGE_2, "value": "I'm not saying tips are magical, but I did just make a wish upon this one."},
    {"param_id": PARAMETER_TIP_SILVER_MESSAGE_3, "value": "To tip or not to tip? That is not even a question. Always tip!"},
    {"param_id": PARAMETER_TIP_SILVER_MESSAGE_4, "value": "Tips are like hugs from strangers... but better, because they're money!"},
    {"param_id": PARAMETER_TIP_SILVER_MESSAGE_5, "value": "I tip, therefore I am... a genius at spending money"},
    {"param_id": PARAMETER_TIP_SILVER_MESSAGE_6, "value": "I like big tips and I cannot lie! You other brothers can't deny!"},
    {"param_id": PARAMETER_TIP_SILVER_MESSAGE_7, "value": "Tips: the original motivator for getting out of bed in the morning."},
    {"param_id": PARAMETER_TIP_SILVER_MESSAGE_8, "value": "I'm not saying tips are the meaning of life, but they sure make it sweeter... like frosting on a donut."},
    {"param_id": PARAMETER_TIP_SILVER_MESSAGE_9, "value": "If life gives you lemons, trade them for tips!"},
    {"param_id": PARAMETER_TIP_GOLD_MESSAGE_1, "value": "Tips are like donuts: the more, the merrier!"},
    {"param_id": PARAMETER_TIP_GOLD_MESSAGE_2, "value": "Why settle for a gold watch when you can retire with a jar full of tips?"},
    {"param_id": PARAMETER_TIP_GOLD_MESSAGE_3, "value": "Woo-hoo! With this tip, I could finally buy my own nuclear power plant... or at least a lifetime supply of Duff beer!"},
    {"param_id": PARAMETER_TIP_GOLD_MESSAGE_4, "value": "I never thought I'd see the day when tips were measured in doughnut trucks instead of dollars!"},
    {"param_id": PARAMETER_TIP_GOLD_MESSAGE_5, "value": "This tip is so big, it's like winning the lottery, but without the taxes... I hope."},
    {"param_id": PARAMETER_TIP_GOLD_MESSAGE_6, "value": "If tips were calories, I'd be in a sugar coma right now!"},
    {"param_id": PARAMETER_TIP_GOLD_MESSAGE_7, "value": "With this tip, I could afford to build my own theme park... Homerland! It's like Disneyland, but with more donuts."},
    {"param_id": PARAMETER_TIP_GOLD_MESSAGE_8, "value": "I always knew my magnetic charm would attract tips, but I never imagined they'd be this huge!"},
    {"param_id": PARAMETER_TIP_GOLD_MESSAGE_9, "value": "They say money can't buy happiness, but I'm pretty sure this tip just proved them wrong... at least until it's spent on more donuts!"},
]

def setup_parameters():
    # Loop through the parameters and create or update them
    for param in all_params:
        create_or_update_param(param['param_id'], param['value'])


def setup_db():
    # Setup the parameters
    setup_parameters()
    print("Database setup complete.")