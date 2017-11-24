# -*- coding: utf-8 -*-

from itchat.content import *

from HaveFun import *
from MediaReply import *
from TextReply import *
from config import *
from util import *
from log import g_log_inst as logger
# Component initialization
itchat.auto_login(True)
xiaoice = itchat.search_mps(name='小冰')[0]['UserName']
last_msg = None
who_send = None


# Core message loops
@itchat.msg_register([NOTE], isGroupChat=True)
def replyNote(msg):
    groupName = msg['User']['NickName']
    print(msg)
    if groupName not in TARGETS:
        return
    if re.search(r"\<\!\[CDATA\[.*撤回了一条消息\]\]\>", msg['Content']):
        replay_chat(msg, last_msg)


@itchat.msg_register([TEXT], isGroupChat=True, isFriendChat=True)
def replyText(msg):
    groupName = msg['User']['NickName']
    global who_send
    who_send = msg['FromUserName']

    if groupName not in TARGETS or be_silence():
        save_chat(who_send, msg['Text'])
        return

    global last_msg
    last_msg = msg

    if not rule_reply(msg, who_send):
        send_msg(msg, xiaoice)


@itchat.msg_register([PICTURE], isGroupChat=True)
def replyPic(msg):
    groupName = msg['User']['NickName']
    global who_send
    who_send = msg['FromUserName']

    if groupName not in TARGETS or be_silence():
        return

    global last_msg
    last_msg = msg
    send_media(msg, xiaoice, "img")


@itchat.msg_register([RECORDING], isGroupChat=True)
def replyVoice(msg):
    groupName = msg['User']['NickName']
    global who_send
    who_send = msg['FromUserName']

    if groupName not in TARGETS or be_silence():
        return

    global last_msg
    last_msg = msg
    send_media(msg, xiaoice, "fil")


@itchat.msg_register([VIDEO], isGroupChat=True)
def replyVideo(msg):
    groupName = msg['User']['NickName']
    global who_send
    who_send = msg['FromUserName']

    if groupName not in TARGETS or be_silence():
        return
    global last_msg
    last_msg = msg
    send_media(msg, xiaoice, "vid")


@itchat.msg_register([TEXT], isMpChat=True)
def get_text(msg):
    global who_send
    if msg['User']['NickName'] != AGENT:
        return

    send_msg(msg, who_send, False)


@itchat.msg_register([PICTURE], isMpChat=True)
def get_pic(msg):
    global who_send
    if msg['User']['NickName'] != AGENT:
        return
    send_media(msg, who_send, "img")


@itchat.msg_register([RECORDING], isMpChat=True)
def get_voice(msg):
    global who_send
    if msg['User']['NickName'] != AGENT:
        return
    send_media(msg, who_send, "fil")


if __name__ == '__main__':
    logger.start('./log/test.log', __name__, 'DEBUG')
    itchat.run()
