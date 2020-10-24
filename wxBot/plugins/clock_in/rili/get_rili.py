from config.fun_api import *

def get_rili(date):
    results = SQL().select_card_text(date)
    return results

def get_jishi(id):
    results = SQL().select_card_holiday(id)
    return results

def get_lishi_jt(date):
    results = SQL().select_card_text_history(date)
    return results