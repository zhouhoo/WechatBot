import itchat
from fuzzywuzzy import process
from config import AUTO,AI_SHUTUP,ROBOT_BLACK_LIST,RULES
from util import aiSwitch
from log import g_log_inst as logger

def rule_reply(msg,to_who):
    if not to_who:
        return True

    if 'isAt' in msg.keys() and msg['isAt']:

        id=random.randrange(0,len(AUTO))
        itchat.send(AUTO[id],to_who)
        return True
    r=process.extract(msg['Content'],RULES.keys(),limit=1)

    if r[0][1]>95:
        itchat.send_msg(RULES[r[0][0]],to_who)
        return True

    return False

def send_msg(msg,to_who, from_user=True):

    logger.get().debug("{}:{}".format(to_who,msg['Text'].encode("utf-8")))

    if from_user :
        aiSwitch(msg['Content'])
        if not AI_SHUTUP :
            itchat.send(msg['Text'], toUserName=to_who)
    else:

        if all([word not in msg['Content'] for word in ROBOT_BLACK_LIST]):
            itchat.send(msg['Text'], toUserName=to_who)