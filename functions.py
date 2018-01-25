from telethon.tl.types import PeerChat, PeerUser, 
PeerChannel def effective_message(message):
    if type(message.message) == str:
        message.effective_message = message
    else:
        message.effective_message = message.message 
def effective_chat_id(update):
    if update.CONSTRUCTOR_ID == 0x914fbf11:
        return update.user_id, 
PeerUser(update.user_id)
    elif update.CONSTRUCTOR_ID == 0x16812688:
        return update.chat_id, 
PeerChat(update.chat_id)
    else:
        return update.message.to_id.channel_id, 
update.message.to_id
