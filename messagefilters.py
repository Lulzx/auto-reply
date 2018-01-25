#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# A library that provides a Python interface to the 
Telegram Bot API
# Copyright (C) 2015-2017
# Leandro Toledo de Souza 
<devs@python-telegram-bot.org>
#
# This program is free software: you can 
redistribute it and/or modify
# it under the terms of the GNU Lesser Public 
License as published by
# the Free Software Foundation, either version 3 of 
the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it 
will be useful,
# but WITHOUT ANY WARRANTY; without even the implied 
warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR 
PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser 
Public License
# along with this program.  If not, see 
[http://www.gnu.org/licenses/]. from 
telethon.tl.types import MessageMediaDocument, \
    MessageMediaContact, MessageMediaGeo, 
MessageMediaVenue, \
    UpdateDeleteChannelMessages def 
effective_message(message):
    if type(message.message) == str:
        message.effective_message = message
    else:
        message.effective_message = message.message 
class BaseFilter(object):
    """Base class for all Message Filters.
    Subclassing from this class filters to be 
combined using bitwise operators:
    And:
    #    >>> (Filters.text & 
Filters.entity(MENTION))
    Or:
    #    >>> (Filters.audio | Filters.video)
    Not:
    #    >>> ~ Filters.command
    Also works with more than two filters:
    #    >>> (Filters.text & (Filters.entity(URL) | 
Filters.entity(TEXT_LINK)))
    #    >>> Filters.text & (~ Filters.forwarded)
    If you want to create your own filters create a 
class inheriting from this class and implement
    a `filter` method that returns a boolean: `True` 
if the message should be handled, `False`
    otherwise. Note that the filters work only as 
class instances, not actual class objects
    (so remember to initialize your filter classes).
    By default the filters name (what will get 
printed when converted to a string for display)
    will be the class name. If you want to overwrite 
this assign a better name to the `name`
    class variable.
    Attributes:
        name (:obj:`str`): Name for this filter. 
Defaults to the type of filter.
    """
    name = None
    def __call__(self, message):
        return self.filter(message)
    def __and__(self, other):
        return MergedFilter(self, and_filter=other)
    def __or__(self, other):
        return MergedFilter(self, or_filter=other)
    def __invert__(self):
        return InvertedFilter(self)
    def __repr__(self):
        # We do this here instead of in a __init__ 
so filter don't have to call __init__ or super()
        if self.name is None:
            self.name = self.__class__.__name__
        return self.name
    def filter(self, message):
        """This method must be overwritten.
        Args:
            message (:class:`telegram.Message`): The 
message that is tested.
        Returns:
            :obj:`bool`
        """
        raise NotImplementedError class 
InvertedFilter(BaseFilter):
    """Represents a filter that has been inverted.
    Args:
        f: The filter to invert.
    """
    def __init__(self, f):
        self.f = f
    def filter(self, message):
        return not self.f(message)
    def __repr__(self):
        return '<inverted {}>'.format(self.f) class 
MergedFilter(BaseFilter):
    """Represents a filter consisting of two other 
filters.
    Args:
        base_filter: Filter 1 of the merged filter
        and_filter: Optional filter to "and" with 
base_filter. Mutually exclusive with or_filter.
        or_filter: Optional filter to "or" with 
base_filter. Mutually exclusive with and_filter.
    """
    def __init__(
        self,
        base_filter,
        and_filter=None,
        or_filter=None,
        ):
        self.base_filter = base_filter
        self.and_filter = and_filter
        self.or_filter = or_filter
    def filter(self, message):
        if self.and_filter:
            return self.base_filter(message) \
                and self.and_filter(message)
        elif self.or_filter:
            return self.base_filter(message) or 
self.or_filter(message)
    def __repr__(self):
        return '<{} {} {}>'.format(self.base_filter, 
('and'
                                    if 
self.and_filter else 'or'),
                                   self.and_filter 
or self.or_filter) class Filters(object):
    """Predefined filters for use as the `filter` 
argument of :class:`telegram.ext.MessageHandler`.
    Examples:
        Use ``MessageHandler(Filters.video, 
callback_method)`` to filter all video
        messages. Use 
``MessageHandler(Filters.contact, callback_method)`` 
for all contacts. etc.
    """
    class _All(BaseFilter):
        name = 'Filters.all'
        def filter(self, message):
            return True
    all = _All()
    class _Message(BaseFilter):
        name = 'Filters.message'
        def filter(self, message):
            r = bool(hasattr(message, 'message'))
            if r:
                effective_message(message)
            return r
    message = _Message()
    class _Text(BaseFilter):
        name = 'Filters.text'
        def filter(self, message):
            if Filters.message(message):
                if 
hasattr(message.effective_message, 'message'):
                    return 
bool(message.effective_message.message)
            return False
    text = _Text()
    class _Command(BaseFilter):
        name = 'Filters.command'
        def filter(self, message):
            if Filters.text(message):
                return 
message.effective_message.message.startswith('/')
            return False
    command = _Command()
    class _Reply(BaseFilter):
        name = 'Filters.reply'
        def filter(self, message):
            return 
bool(message.effective_message.reply_to_msg_id)
    reply = _Reply()
    class _Media(BaseFilter):
        name = 'Filters.media'
        def filter(self, message):
            if Filters.message(message):
                return 
hasattr(message.effective_message, 'media')
            return False
    media = _Media()
    class _Audio(BaseFilter):
        name = 'Filters.media'
        def filter(self, message):
            if Filters.media(message):
                return 
hasattr(message.effective_message.media, 'audio')
            return False
    audio = _Audio()
    class _Document(BaseFilter):
        name = 'Filters.document'
        def filter(self, message):
            if Filters.media(message):
                return 
isinstance(message.effective_message.media,
                                  
MessageMediaDocument)
            return False
    document = _Document()
    class _Photo(BaseFilter):
        name = 'Filters.photo'
        def filter(self, message):
            if Filters.media(message):
                return 
hasattr(message.effective_message.media, 'photo')
    photo = _Photo()
    class _MessageMediaDocument(BaseFilter):
        name = 'Filters.messagemediadocument'
        def filter(self, message):
            if Filters.media(message):
                return 
isinstance(message.effective_message.media,
                                  
MessageMediaDocument)
            return False
    messagemediadocument = _MessageMediaDocument()
    class _Sticker(BaseFilter):
        name = 'Filters.sticker'
        def filter(self, message):
            if 
Filters.messagemediadocument(message):
                return 
bool(message.effective_message.media.mime_type
                            == 'image/webp')
            return False
    sticker = _Sticker()
    class _Video(BaseFilter):
        name = 'Filters.video'
        def filter(self, message):
            if 
Filters.messagemediadocument(message):
                return 
bool(message.effective_message.media.mime_type
                            == 'video/mp4')
            return False
    video = _Video()
    class _Voice(BaseFilter):
        name = 'Filters.voice'
        def filter(self, message):
            if 
Filters.messagemediadocument(message):
                return 
bool(message.effective_message.media.mime_type
                            == 'audio/ogg')
            return False
    voice = _Voice()
    class _Contact(BaseFilter):
        name = 'Filters.contact'
        def filter(self, message):
            if 
Filters.messagemediadocument(message):
                return 
isinstance(message.effective_message.media,
                                  
MessageMediaContact)
            return False
    contact = _Contact()
    class _Location(BaseFilter):
        name = 'Filters.location'
        def filter(self, message):
            if Filters.media(message):
                return 
isinstance(message.effective_message.media,
                                  MessageMediaGeo)
            return False
    location = _Location()
    class _Venue(BaseFilter):
        name = 'Filters.venue'
        def filter(self, message):
            if Filters.media(message):
                return 
isinstance(message.effective_message.media,
                                  MessageMediaVenue)
            return False
    venue = _Venue()
    class _DeletedMessage(BaseFilter):
        name = 'Filters.deletedmessage'
        def filter(self, message):
            return message.CONSTRUCTOR_ID in 
[0xc37521c9, 0xa20db0e5]
    deletedmessage = _DeletedMessage()
    class _StatusUpdate(BaseFilter):
        """Subset for messages containing a status 
update.
        Examples:
            Use these filters like: 
``Filters.status_update.new_chat_member`` etc. Or 
use just
            ``Filters.status_update`` for all status 
update messages.
        """
        class _UpdateUserStatus(BaseFilter):
            name = 
'Filters.status_update.updateuserstatus'
            def filter(self, message):
                return hasattr(message, 'status')
        updateuserstatus = _UpdateUserStatus()
        class _OnlineUpdate(BaseFilter):
            name = 'Filters.status_update.online'
            def filter(self, message):
                if 
Filters.status_update.updateuserstatus(message):
                    return 
message.status.SUBCLASS_OF_ID == 0x5b0b743e
        online = _OnlineUpdate()
    class _ChatAction(BaseFilter):
        class _NewChatMembers(BaseFilter):
            name = 
'Filters.status_update.new_chat_members'
            def filter(self, message):
                if Filters.chataction(message):
                    return 
message.message.action.CONSTRUCTOR_ID \
                        == 0x488a7337
        new_chat_members = _NewChatMembers()
        class _LeftChatMember(BaseFilter):
            name = 
'Filters.status_update.left_chat_member'
            def filter(self, message):
                return 
bool(message.left_chat_member)
        left_chat_member = _LeftChatMember()
        class _NewChatTitle(BaseFilter):
            name = 
'Filters.status_update.new_chat_title'
            def filter(self, message):
                return bool(message.new_chat_title)
        new_chat_title = _NewChatTitle()
        class _NewChatPhoto(BaseFilter):
            name = 
'Filters.status_update.new_chat_photo'
            def filter(self, message):
                return bool(message.new_chat_photo)
        new_chat_photo = _NewChatPhoto()
        class _DeleteChatPhoto(BaseFilter):
            name = 
'Filters.status_update.delete_chat_photo'
            def filter(self, message):
                return 
bool(message.delete_chat_photo)
        delete_chat_photo = _DeleteChatPhoto()
        class _ChatCreated(BaseFilter):
            name = 
'Filters.status_update.chat_created'
            def filter(self, message):
                return 
bool(message.group_chat_created
                            or 
message.supergroup_chat_created
                            or 
message.channel_chat_created)
        chat_created = _ChatCreated()
        class _Migrate(BaseFilter):
            name = 'Filters.status_update.migrate'
            def filter(self, message):
                return 
bool(message.migrate_from_chat_id
                            or 
message.migrate_to_chat_id)
        migrate = _Migrate()
        class _PinnedMessage(BaseFilter):
            name = 
'Filters.status_update.pinned_message'
            def filter(self, message):
                return bool(message.pinned_message)
        pinned_message = _PinnedMessage()
        name = 'Filters.status_update'
        def filter(self, message):
            if Filters.message(message):
                return hasattr(message.message, 
'action')
            return False
    chataction = _ChatAction()
    class _Forwarded(BaseFilter):
        name = 'Filters.forwarded'
        def filter(self, message):
            return bool(message.forward_date)
    forwarded = _Forwarded()
    class _Game(BaseFilter):
        name = 'Filters.game'
        def filter(self, message):
            return bool(message.game)
    game = _Game()
