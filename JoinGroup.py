# -*- coding: utf-8 -*-
from util import *
from itchat.content import *
import os
import itchat
from log import g_log_inst as logging

class GroupMessageForwarder():
    def __init__(self, chatroomDisplayNames, chatroomNames, isBidirectional=True):
        self.isInitialized = False
        self.chatroomDisplayNames = chatroomDisplayNames
        self.chatroomNames = chatroomNames
        self.isBidirectional = isBidirectional
        chatrooms = itchat.get_chatrooms()
        self.chatroomObjs = [ getChatroomByName(chatrooms, x) for x in chatroomNames ]
        if len([ x for x in self.chatroomObjs if x is None ]) != 0:
            logging.get().debug('Cannot find chatrooms for {0}'.format(chatroomNames))
            return
        self.chatroomIds = [ x['UserName'] for x in self.chatroomObjs ]
        self.nickNameLookup = NickNameLookup(self.chatroomObjs)
        self.fileFolder = 'ForwarderFiles'
        if not os.path.exists(self.fileFolder):
            os.mkdir(self.fileFolder)
        logging.info('Fetched user ids for the chatrooms {0}.'.format(chatroomNames))
        self.isInitialized = True

    def process(self, msg, type):
        if not self.isInitialized:
            logging.get().debug('The forwarder was not properly initialized. Please send a message in the groups you want to connect and try again.')
            return
        shallSendObj = self.shallSend(msg)
        if not shallSendObj['shallSend']:
            return
        if type == TEXT:
            fromText = '[{0}]'.format(self.chatroomDisplayNames[shallSendObj['fromChatroom']])
            destinationChatroomId = self.chatroomIds[not shallSendObj['fromChatroom']]
            content = '{0} {1}: {2}'.format(fromText, msg['ActualNickName'], msg['Content'])
            logging.get().debug(content)
            #itchat.send(content, destinationChatroomId)
            itchat.send(msg['Content'], destinationChatroomId)
        elif type == PICTURE:
            fn = msg['FileName']
            newfn = os.path.join(self.fileFolder, fn)
            msg['Text'](fn)
            os.rename(fn, newfn)
            type = {'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil')
            typeText = {'Picture': '图片', 'Video': '视频'}.get(msg['Type'], '文件')
            fromText = '[{0}]'.format(self.chatroomDisplayNames[shallSendObj['fromChatroom']])
            destinationChatroomId = self.chatroomIds[not shallSendObj['fromChatroom']]
            content = '{0} {1} 发送了{2}:'.format(fromText, self.nickNameLookup.lookupNickName(msg), typeText)
            #itchat.send(content, destinationChatroomId)
            itchat.send("你又发图哦~", destinationChatroomId)
            logging.get().debug(content)
            itchat.send('@{0}@{1}'.format(type, newfn), destinationChatroomId)
        elif type == SHARING:
            fromText = '[{0}]'.format(self.chatroomDisplayNames[shallSendObj['fromChatroom']])
            destinationChatroomId = self.chatroomIds[not shallSendObj['fromChatroom']]
            content1 ='{1} {2}'.format(msg['Text'], msg['Url'])
            content = '{0} {1} 分享了链接: {2} {3}'.format(fromText, self.nickNameLookup.lookupNickName(msg), msg['Text'], msg['Url'])
            logging.get().debug(content)
            itchat.send(content1, destinationChatroomId)
        else:
            logging.info('Unknown type encoutered.')
        pass

    def shallSend(self, msg):
        result = False
        for i in range(len(self.chatroomIds)):
            result = result or extractToUserName(msg) == self.chatroomIds[i] or extractFromUserName(msg) == self.chatroomIds[i]
            if result:
                return { 'shallSend': True, 'fromChatroom': i }
            if not self.isBidirectional:
                break
        return { 'shallSend': False }
