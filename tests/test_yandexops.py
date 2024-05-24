import pytest
import yandexops
from datetime import datetime
from unittest.mock import patch
import namemanager
import locationtracker


@pytest.fixture
def setup_namemanager():
    namemanager.init()


def test_basic():
    depart = "s9601261"
    arrive = "s9601830"
    date = datetime.fromisoformat("2024-05-15")
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = date
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(
            *args, **kwargs)

        res = yandexops.find_routes(
            depart, arrive)
        res.sort(key=lambda x: x["departure"])
        testres = res[0]
        print(testres)
        assert (str(res[0]["number"]) == "6307")
