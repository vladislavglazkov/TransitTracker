from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler
from telegram.ext import Updater, CommandHandler, CallbackContext, filters

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Message
from datetime import datetime, timedelta
import asyncio
import time
import json

from basichandlers import add_cancel, issue_info, default_handler
import namemanager
import statushandlers
from geopy.distance import geodesic


FAR_AWAY = 0
OUTER_VICINITY = 1
INNER_VICINITY = 2


def get_distance(d1, d2):
    return geodesic((d1["latitude"], d1["longitude"]),
                    (d2["latitude"], d2["longitude"])).meters


def get_status(meters):
    if (meters > 3000):
        return FAR_AWAY
    if (meters > 300):
        return OUTER_VICINITY
    return INNER_VICINITY


async def update_location(update: Update,
                          context: ContextTypes.DEFAULT_TYPE) -> None:
    loc = None
    if update.message is not None:
        loc = update.message.location
    elif update.edited_message is not None:
        loc = update.edited_message.location
    if not loc:
        return

    loc = {"latitude": loc.latitude, "longitude": loc.longitude}
    routes = json.loads(context.chat_data["routes"])
    sent_anything = False
    for route in routes:
        start = route["start"]

        cur_status = get_status(
            get_distance(
                namemanager.resolve_id(start),
                loc))
        print(cur_status)

        former_status = 0 if "status" not in route else route["status"]
        former_status_set = datetime.fromtimestamp(
            0) if "status_set" not in route else route["status_set"]

        if ('status' not in route):
            route["status"] = cur_status
            route["status_set"] = datetime.now().timestamp()
            continue

        if (former_status == 1 and cur_status == 2):
            diff = datetime.now() - datetime.fromtimestamp(former_status_set)
            if (diff > timedelta(minutes=10)):
                await issue_info(update, context, route["start"], route["end"])
                sent_anything = True

        if (cur_status != former_status):
            route["status"] = cur_status
            route["status_set"] = datetime.now().timestamp()
    if (sent_anything):
        await default_handler(update, context)
    context.chat_data["routes"] = json.dumps(routes)
