import pymongo
from telegram import Update
from telegram.ext import ContextTypes
import functools


def init():
    global db
    client = pymongo.MongoClient()
    db = client.transittracker


def connect_mongo_table(name):
    def internal_connect(f):
        table = None
        if "db" in globals():
            table = db.get_collection(name)

        def get_id(update: Update):
            if (update.message):
                return update.message.chat_id
            if (update.edited_message):
                return update.edited_message.chat_id
            return update.effective_chat.id

        @functools.wraps(f)
        async def wrap(
                update: Update, context: ContextTypes.DEFAULT_TYPE, *args):
            print(f"Inside wrap for {wrap.__wrapped__.__name__}")
            res = table.find_one({"id": get_id(update)})
            data = []
            print(res)
            if (res is None):
                table.insert_one({"id": get_id(update), "data": []})
            else:
                data = res["data"]
            print(data)

            def apply(data):
                print("Applied")
                table.update_one({"id": get_id(update)}, {
                                 "$set": {"data": data}})

            print("Called wrap")
            print(data)
            await f(update, context, *args, data, apply)
        return wrap
    return internal_connect
