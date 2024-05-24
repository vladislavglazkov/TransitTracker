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


@statushandlers.handles_status
async def start_route_creation(
        update: Update, context: CallbackContext) -> None:
    context.chat_data["status"] = "confirm_start_point_name"
    await update.effective_chat.send_message("Enter start name", reply_markup=InlineKeyboardMarkup([add_cancel()]))


@statushandlers.handles_status
async def confirm_start_point_name(
        update: Update, context: CallbackContext) -> None:
    name = update.message.text.strip().lower()
    res = namemanager.resolve_name(name)
    if (len(res) == 0):
        await update.message.reply_text(
            "Not found. Repeat, please",
            reply_markup=InlineKeyboardMarkup([add_cancel()]))
        return
    if (len(res) > 20):
        await update.message.reply_text(
            "Too many matches. Repeat, please",
            reply_markup=InlineKeyboardMarkup([add_cancel()]))
        return

    btns = []
    for h in res:
        btn = InlineKeyboardButton(
            f"{h['title']}", callback_data=json.dumps({"start": h["id"]}))
        btns.append([btn])
    markup = InlineKeyboardMarkup([*btns, add_cancel()])
    await update.message.reply_text(
        "Please select the correct one",
        reply_markup=markup)
    context.chat_data["status"] = "request_end_point_name"


@statushandlers.handles_status
async def request_end_point_name(
        update: Update, context: CallbackContext) -> None:

    context.chat_data["new_route_start_id"] = json.loads(
        update.callback_query.data)["start"]
    context.chat_data["status"] = "confirm_end_point_name"
    await update.effective_chat.send_message("Enter end name", reply_markup=InlineKeyboardMarkup([add_cancel()]))


@statushandlers.handles_status
async def confirm_end_point_name(
        update: Update, context: CallbackContext) -> None:
    name = update.message.text.strip().lower()
    res = namemanager.resolve_name(name)
    if (len(res) == 0):
        await update.message.reply_text(
            "Not found. Repeat, please",
            reply_markup=InlineKeyboardMarkup([add_cancel()]))
        return
    if (len(res) > 20):
        await update.message.reply_text(
            "Too many matches. Repeat, please",
            reply_markup=InlineKeyboardMarkup([add_cancel()]))
        return
    btns = []
    for h in res:
        btn = InlineKeyboardButton(
            f"{h['title']}", callback_data=json.dumps({"end": h["id"]}))
        btns.append([btn])
    markup = InlineKeyboardMarkup([*btns, add_cancel()])
    await update.message.reply_text(
        "Please select the correct one",
        reply_markup=markup)
    context.chat_data["status"] = "finalize_route_creation"


@statushandlers.handles_status
async def finalize_route_creation(
        update: Update, context: CallbackContext) -> None:

    end_id = json.loads(update.callback_query.data)["end"]
    start_id = context.chat_data["new_route_start_id"]

    routes: list = json.loads(context.chat_data["routes"])
    routes.append({"start": start_id, "end": end_id})
    context.chat_data["routes"] = json.dumps(routes)
    await default_handler(update, context)
