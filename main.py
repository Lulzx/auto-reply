#!/usr/bin/python
# -*- coding: utf-8 -*-
from telethon import TelegramClient from 
telethon.tl.types import UpdateShortMessage import 
config import time import messagefilters import 
functions client = TelegramClient(config.session_id, 
config.api_id,
                        config.api_hash, 
update_workers=4) client.connect() if not 
client.is_user_authorized():
    client.sign_in(config.phone)
    client.sign_in(code=input('Code:')) print 
len(client.get_dialogs()) def printupdate(update):
    print update
    if messagefilters.Filters.command(update) and 
isinstance(update,
            UpdateShortMessage):
        text = update.effective_message.message
        if text == '/start':
            print '/start command used'
            try:
                print 
functions.effective_chat_id(update)
                
client.send_message(functions.effective_chat_id(update)[1],
                                    'message')
            except Exception, e:
                print e 
client.add_update_handler(printupdate)
time.sleep(1000000)
