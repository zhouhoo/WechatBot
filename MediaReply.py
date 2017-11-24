import itchat
import os
from config import FOLDER


def send_media(msg,to_who,types):
    filename=os.path.join(FOLDER, msg['FileName'])
    msg['Text'](filename)
    itchat.send('@%s@%s' % (types, filename),to_who)
    os.remove(filename)
