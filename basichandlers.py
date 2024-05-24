import pytz
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler
from telegram.ext import Updater, CommandHandler, CallbackContext, filters

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Message
import asyncio
import time
import json
import namemanager
import yandexops
from datetime import datetime


async def default_handler(update: Update,
                          context: ContextTypes.DEFAULT_TYPE) -> None:
    new_route = InlineKeyboardButton(
        "Subscribe to new route",
        callback_data=json.dumps({"change_status": "start_route_creation"}))

    routes = json.loads(context.chat_data["routes"])

    routebtns = []
    for route in routes:
        start_name = namemanager.resolve_id(route["start"])["title"]
        end_name = namemanager.resolve_id(route["end"])["title"]
        str = f"{start_name} - {end_name}"
        routebtns.append(
            InlineKeyboardButton(
                str, callback_data=json.dumps({
                    "change_status": "answer_request", "route": {"start": route["start"], "end": route["end"]}})))

    btns = InlineKeyboardMarkup.from_row([*routebtns, new_route])

    await update.effective_chat.send_message("Select action", reply_markup=btns)


async def answer_request(update: Update,
                         context: ContextTypes.DEFAULT_TYPE) -> None:
    data = json.loads(update.callback_query.data)
    start = data["route"]["start"]
    end = data["route"]["end"]

    context.chat_data["status"] = "default"
    segments: list = list(filter(
        lambda h: h["departure"] >= datetime.now(pytz.utc),
        yandexops.find_routes(
            start,
            end)))
    segments.sort(key=lambda x: x["departure"])
    segments = segments[:2]
    resstr = ""
    if (len(segments) == 0):
        resstr = "Unfortunately, no routes had been found for the near future"

    else:
        def print_route(h):
            return f'{h["title"]} {h["number"]} at {h["departure"]}'

        resstr += (f"""
Next train:
    {print_route(segments[0])}

""")

        if (len(segments) >= 2):
            resstr += (f"""
After that:
    {print_route(segments[1])}
""")

    await update.effective_chat.send_message(resstr)
    await default_handler(update, context)


def add_cancel():
    return [InlineKeyboardButton("Cancel", callback_data=json.dumps({
        "change_status": "default"}))]
