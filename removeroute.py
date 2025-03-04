from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler
from telegram.ext import Updater, CommandHandler, CallbackContext, filters

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Message
import asyncio
import time
import json

from basichandlers import add_cancel, default_handler
import namemanager
import statushandlers
import mongoops


@statushandlers.handles_status
@mongoops.connect_mongo_table("routes")
async def start_route_removal(
        update: Update, context: CallbackContext, routes, apply) -> None:

    btns = []
    for route in routes:
        start_name = namemanager.resolve_id(route["start"])["title"]
        end_name = namemanager.resolve_id(route["end"])["title"]
        btn = InlineKeyboardButton(
            f"{start_name} - {end_name}",
            callback_data=json.dumps(
                {
                    "change_status": "finalize_route_removal",
                    "route": {"start": route["start"],
                              "end": route["end"]
                              }
                }))
        btns.append([btn])
    btns.append(add_cancel())

    await update.effective_chat.send_message("Which route would you like to remove: ", reply_markup=InlineKeyboardMarkup(btns))


@statushandlers.handles_status
@mongoops.connect_mongo_table("routes")
async def finalize_route_removal(
        update: Update, context: CallbackContext, routes, apply) -> None:
    data = json.loads(update.callback_query.data)
    await update.callback_query.answer(None)

    # for h in routes:
    #     print(h["start"], h["end"])

    # print("\n\n")
    # print(data["route"]["start"], data["route"]["end"])

    routes = list(filter(
        lambda x: not (x["start"] == data["route"]["start"]
                       and x["end"] == data["route"]["end"]),
        routes
    ))
    apply(routes)
    await default_handler(update, context)
