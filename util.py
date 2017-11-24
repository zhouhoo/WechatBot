# -*- coding: utf-8 -*-
"""
Some utility functions
"""
import re
import random
from  log import g_log_inst
from config import SHUT_KEY,ACTIVE_KEY
def save_chat(who_send,msg):
    g_log_inst.get().debug("{}:{}".format(who_send,msg.encode("utf-8")))

def be_silence():
    if random.random()<=0.7:
        return True
    else:
        return False

def aiSwitch(msg):
    if SHUT_KEY in msg:
        AI_SHUTUP = 1
    elif ACTIVE_KEY in msg:
        AI_SHUTUP =0