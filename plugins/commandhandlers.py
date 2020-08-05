from pyrogram import Client, Filters, InlineKeyboardButton, InlineKeyboardMarkup
from plugins.payment import LinkGen, deletelink
import asyncio
import json
import os


@Client.on_message(Filters.command(["start"]))
async def start(client, message):
    await client.send_message(
        chat_id=message.chat.id,
        text="Choose The Amount of Account",
        reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Button 1', callback_data='1')],
                [InlineKeyboardButton(text='Button 2', callback_data='2')],
                [InlineKeyboardButton(text='Button 3', callback_data='3')],
                [InlineKeyboardButton(text='Exit', callback_data='exit')],
        ]),
        reply_to_message_id=message.message_id
        )


@Client.on_message(Filters.command(["status"]))
async def status(client, message):
    with open("links.json", "r") as read_file:
        data = json.load(read_file)
        link = None
        for items in data["users"]:
            if items["id"] == message.chat.id:
                link = items["link"]
                linkid = items["linkid"]
                break
        if link is not None:
            await message.reply_text(
                text=f"{link}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text='redeem', callback_data='redeem')],
                    [InlineKeyboardButton(text='delete', callback_data=f'del-{linkid}')],
                    [InlineKeyboardButton(text='exit', callback_data='exit')],
                ])
            )
        elif link is None:
            await message.reply_text(
                text="Soory there is no transaction pending"
            )


@Client.on_callback_query()
async def cb_(client, callback_query):
    cb_data = callback_query.data
    msg = callback_query.message
    if cb_data == '1':
        await client.answer_callback_query(
            text="You Pressed Button 1",
            callback_query_id=callback_query.id,
        )
        await msg.edit("Generating Url....")
        try:
            url, expiry, linkid = LinkGen(
                "dealer-bot-moviewalla",
                "a small description",
                "50.0"
            )
            with open("links.json", "r") as read_file:
                data = json.load(read_file)
                data["users"].append(
                    {"id": msg.chat.id, 'link': "placeholder", 'linkid': "anotherpl"}
                    )
                with open("links.json", "w") as write_file:
                    write_file.writelines(json.dumps(data, indent=2))
        except ModuleNotFoundError:
            await msg.edit("Server Unavilable")
    elif cb_data == '2':
        await client.answer_callback_query(
            text="You Pressed Button 2",
            callback_query_id=callback_query.id,
        )
    elif cb_data == '3':
        await client.answer_callback_query(
            text="You Pressed Button 3",
            callback_query_id=callback_query.id,
        )
    elif cb_data == 'exit':
        await msg.delete()
    else:
        await client.answer_callback_query(
            text="Processing your request please wait",
            callback_query_id=callback_query.id,
        )
        if 'del' in cb_data:
            await msg.edit('processing...')
            _, linkid = cb_data.split("-", 1)
            print(linkid)
            with open("links.json", "r") as read_file:
                data = json.load(read_file)
                data["users"].remove(
                    {"id": msg.chat.id, 'link': msg.text, 'linkid': linkid}
                    )
                with open("links.json", "w") as write_file:
                    write_file.writelines(json.dumps(data, indent=2))
            # deletelink(linkid)
            await msg.edit("Successfully deleted your transaction")
