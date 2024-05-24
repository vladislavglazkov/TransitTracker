from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler
from telegram.ext import Updater, CommandHandler, CallbackContext, filters

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Message
import asyncio
import time
import json
from basichandlers import answer_request, default_handler
import createroute
import namemanager
import statushandlers
import removeroute
import locationtracker


async def start(update: Update, context: CallbackContext):
    routes = []
    context.chat_data["routes"] = json.dumps(routes)
    context.chat_data["status"] = "default"
    await default_handler(update, context)

locmsg: Message = None


async def updloc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global loc
    print("updloc")


async def dispatcher(update: Update, context: CallbackContext) -> None:
    if (update.callback_query):
        await update.callback_query.answer(None)

        upd: dict = json.loads(update.callback_query.data)
        if ("change_status" in upd):
            context.chat_data["status"] = upd["change_status"]
    if ("status" not in context.chat_data):
        context.chat_data["status"] = "default"
    if ("routes" not in context.chat_data):
        context.chat_data["routes"] = json.dumps([])
    status = context.chat_data["status"]

    if statushandlers.get_handler(context.chat_data["status"]) is not None:
        await statushandlers.get_handler(context.chat_data["status"])(update, context)
    else:
        context.chat_data["status"] = "default"
        await default_handler(update, context)


namemanager.init()
app = ApplicationBuilder().token(
    "7056812856:AAHhDqLXV1KX1fuTpWDYAjUacLd1nPfEfpE").arbitrary_callback_data(True).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(
        filters=filters.LOCATION,
        callback=locationtracker.update_location))
app.add_handler(CallbackQueryHandler(dispatcher))
app.add_handler(MessageHandler(filters=None, callback=dispatcher))

# app.add_handler(MessageHandler(filters=None, callback=default_handler))


app.run_polling(allowed_updates=Update.ALL_TYPES)
