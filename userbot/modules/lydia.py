# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
# credit goes to @snapdragon and @devpatel_73 for making it work on this userbot.
#
# Original author of the UniBorg module 'lydia' @Zero_cool7870 (Jaskaran)
#
"""
Userbot module to use an AI To respond to people
"""
import asyncio

from coffeehouse.lydia import LydiaAI
from coffeehouse.api import API
from userbot import LYDIA_API_KEY
from userbot import CMD_HELP
from userbot.events import register

# Non-SQL Mode
ACC_LYDIA = {}
SESSION_ID = {}

if LYDIA_API_KEY:
    lydiaAI = LydiaAI(API(LYDIA_API_KEY))

    
@register(outgoing=True, pattern="^.repcf$")
async def repcf(event):
    if event.fwd_from:
        return
    await event.edit("Processing...")
    try:
        session = lydiaAI.create_session()
        reply = await event.get_reply_message()
        msg = reply.text
        text_rep = session.think_thought(msg)
        await event.edit("**Lydia says**: {0}".format(text_rep))
    except Exception as e:
        await event.edit(str(e))

        
@register(outgoing=True, pattern="^.addcf$")
async def addcf(event):
    if event.fwd_from:
        return
    await event.edit("Running on SQL mode for now...")
    await asyncio.sleep(4)
    await event.edit("Processing...")
    reply_msg = await event.get_reply_message()
    if reply_msg:
        session = lydiaAI.create_session()
        ACC_LYDIA.update({str(event.chat_id) + " " + str(reply_msg.from_id): session})
        await event.edit("Lydia successfully enabled for user: {} in chat: {}".format(str(reply_msg.from_id), str(event.chat_id)))
    else:
        await event.edit("Reply to a user to activate Lydia AI on them")

        
@register(outgoing=True, pattern="^.remcf$")
async def remcf(event):
    if event.fwd_from:
        return
    await event.edit("Running on SQL mode for now...")
    await asyncio.sleep(4)
    await event.edit("Processing...")
    reply_msg = await event.get_reply_message()
    try:
        del ACC_LYDIA[str(event.chat_id) + " " + str(reply_msg.from_id)]
        await event.edit("Lydia successfully disabled for user: {} in chat: {}".format(str(reply_msg.from_id), str(event.chat_id)))
    except KeyError:
        await event.edit("This person does not have Lydia activated on him/her.")

        
@register(incoming=True, disable_edited=True)
async def user(event):
    try:
        session = ACC_LYDIA[str(event.chat_id) + " " + str(event.from_id)]
        msg = event.text
        async with event.client.action(event.chat_id, "typing"):
            text_rep = session.think_thought(msg)
            wait_time = 0
            for i in range(len(text_rep)):
                wait_time = wait_time + 0.1
            await asyncio.sleep(wait_time)
            await event.reply(text_rep)
    except KeyError:
        return

    
CMD_HELP.update({
    "lydia":
    ".addcf <username/reply>\
\nUsage: add's lydia auto chat request in the chat.\
\n\n.remcf <username/reply>\
\nUsage: remove's lydia auto chat request in the chat.\
\n\n.repcf <username/reply>\
\nUsage: starts lydia repling to perticular person in the chat."
})
