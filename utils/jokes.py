import random

MIN_AMOUNT_STANDARD = 1000 # Is substituted by the value of PARAMETER_MIN_AMOUNT_JOKE
MIN_AMOUNT_SILVER = 1000000
MIN_AMOUNT_GOLD = 1000000000


#name can be gold_[1-9], silver_[1-9] or standard_[1-9]
PATH_JOKE_ANIMATIONS = "assets/jokes/{name}.gif"


from constants.parameters import ( 
    PARAMETER_MIN_AMOUNT_JOKE,
    PARAMETER_TIP_STANDARD_DRAFT,
    PARAMETER_TIP_SILVER_DRAFT,
    PARAMETER_TIP_GOLD_DRAFT,
    PARAM_TIP_JOKE_FILENAME_STANDARD,
    PARAM_TIP_JOKE_FILENAME_SILVER,
    PARAM_TIP_JOKE_FILENAME_GOLD,
    PARAMETER_TIP_EMOJI_GOLD,
    PARAMETER_TIP_EMOJI_SILVER,
    PARAMETER_TIP_EMOJI_STANDARD

)
from db.parameters import get_param

def get_rand_joke_nr():
    # Return a number between 1 and 9
    return random.randint(1, 9)


def get_tip_param_by_amount(amount):
    min_joke_amount = get_param(PARAMETER_MIN_AMOUNT_JOKE)
    if amount >= MIN_AMOUNT_GOLD:
        return PARAMETER_TIP_GOLD_DRAFT
    elif amount >= MIN_AMOUNT_SILVER:
        return PARAMETER_TIP_SILVER_DRAFT
    else:
        return PARAMETER_TIP_STANDARD_DRAFT
    
def get_emoji_by_amount(amount):
    if amount >= MIN_AMOUNT_GOLD:
        return get_param(PARAMETER_TIP_EMOJI_GOLD)
    elif amount >= MIN_AMOUNT_SILVER:
        return get_param(PARAMETER_TIP_EMOJI_SILVER)
    else:
        return get_param(PARAMETER_TIP_EMOJI_STANDARD)

def get_name_gif_by_amount(joke_nr, amount):
    if amount >= MIN_AMOUNT_GOLD:
        return PARAM_TIP_JOKE_FILENAME_GOLD.format(joke_nr=joke_nr)
    elif amount >= MIN_AMOUNT_SILVER:
        return PARAM_TIP_JOKE_FILENAME_SILVER.format(joke_nr=joke_nr)
    else:
        return PARAM_TIP_JOKE_FILENAME_STANDARD.format(joke_nr=joke_nr)

def get_joke_text(amount, joke_nr):
    param_id = get_tip_param_by_amount(amount)
    text = get_param(f"{param_id}{joke_nr}")
    emoji = get_emoji_by_amount(amount)

    return f'{emoji} {text}'

def get_joke_animation(joke_nr, amount):
    name = get_name_gif_by_amount(joke_nr, amount)
    path = PATH_JOKE_ANIMATIONS.format(name=name)
    file = open(path, 'rb')
    return file


def get_tip_joke_text_and_animation(amount):
    joke_nr = get_rand_joke_nr()
    joke_text = get_joke_text(amount, joke_nr)
    animation = get_joke_animation(joke_nr, amount)
    return {'animation': animation, 'joke': joke_text}