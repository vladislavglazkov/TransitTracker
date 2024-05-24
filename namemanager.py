import json

data = []
stations = []


def init():
    global data
    global stations
    text = ""
    with open("stations.json", 'r') as f:
        text = f.read()
    data = json.loads(text)

    for country in data["countries"]:
        for region in country["regions"]:
            for settlement in region["settlements"]:
                for station in settlement["stations"]:
                    title: str = station["title"]

                    stations.append(station)


def resolve_id(id):
    for station in stations:
        if (id == station["codes"]["yandex_code"]):
            return station


def resolve_name(title):
    ans = []
    for station in stations:

        if (title in station["title"].lower()):
            ans.append(
                {"id": station["codes"]["yandex_code"], "title": station["title"]})
    return ans
