import requests
import time
from datetime import datetime, timedelta
import json
import pytz

token = "f3193d18-c065-431e-9c52-226c281cafe8"


def find_routes_for_day(start: str, end: str, date: datetime) -> list:
    req = f"https://api.rasp.yandex.net/v3.0/search/?apikey={token}&format=json&from={start}&to={end}&lang=ru_RU&date={date}&limit={100}"
    res = requests.get(req)

    data = json.loads(res.content)
    segments: list = data["segments"] if "segments" in data else []
    cur = 100
    while (cur < data["pagination"]["total"]):
        req = f"https://api.rasp.yandex.net/v3.0/search/?apikey={token}&format=json&from={start}&to={end}&lang=ru_RU&date={date.strftime('%Y-%m-%d')}&limit={100}&offset={cur}"
        res = requests.get(req)
        segments.extend(json.loads(res.content)[
                        "segments"] if "segments" in data else [])
        cur += 100
    return segments


def find_routes(start: str, end: str) -> list:
    current_date = datetime.now()

    segments = find_routes_for_day(start, end, current_date)
    if (len(segments) < 2):
        tomorrow_date = datetime.now() + timedelta(days=1)
        segments.extend(find_routes_for_day(start, end, tomorrow_date))

    return [{"id": h["thread"]["uid"], "title": h["thread"]["title"],
             "number": h["thread"]["number"], "departure": datetime.fromisoformat(h["departure"])} for h in segments]
    # for h in segments:
    #     print(f'{h["thread"]["title"]} {h["thread"]["number"]} at {h["departure"]}')
    # print(len(segments))
