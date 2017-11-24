import itchat
from MediaReply import *

#防撤回
def replay_chat(msg,history_msg):
    if history_msg:
        itchat.send_msg("别撤回了，机智的我都看到了",msg['FromUserName'])
        if msg['Type'] =='Picture':
            send_media(history_msg,msg['FromUserName'],"img")
        elif msg['Type'] == 'Video':
            send_media(history_msg,msg['FromUserName'],"vid")
        elif msg['Type'] == 'Recording':
            send_media(history_msg,msg['FromUserName'],"fil")
