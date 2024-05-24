import pytest
import yandexops
from datetime import datetime
from unittest.mock import AsyncMock, patch
import namemanager
import locationtracker
import basichandlers
import pytest_asyncio


@pytest.fixture
def setup_namemanager():
    namemanager.init()


class A:
    pass


close_location_to_second = A()


@pytest.mark.asyncio
async def test_1_to_2_slow(setup_namemanager):
    routes = [{
        "start": 's9601261',
        "end": 's9601728',
        "status": 0,
        "status_set": 1716570256.743725
    },
        {
        "start": 's9601728',
        "end": 's9601666',
        "status": 1,
        "status_set": 1716570256.746998
    }]

    def apply(route):
        routes = route.copy()

    close_location_to_second.message = A()
    close_location_to_second.message.location = A()
    close_location_to_second.message.chat_id = "abc"

    close_location_to_second.message.location.latitude = 55.726866
    close_location_to_second.message.location.longitude = 37.450563
    close_location_to_second.effective_chat = A()

    context = A()
    context.chat_data = dict()

    count = 0

    async def ctr(*args, **kwargs):
        nonlocal count
        count += 1
    close_location_to_second.effective_chat.send_message = ctr

    with patch("basichandlers.issue_info", new_callable=AsyncMock) as mock_issue_info:
        mock_issue_info.side_effect = None
        mock_issue_info.return_value = None
        await locationtracker.update_location.__wrapped__(
            close_location_to_second, context, routes, apply)
        assert (count == 2)


@pytest.mark.asyncio
async def test_1_to_2_fast(setup_namemanager):
    routes = [{
        "start": 's9601261',
        "end": 's9601728',
        "status": 0,
        "status_set": 1716570256.743725
    },
        {
        "start": 's9601728',
        "end": 's9601666',
        "status": 1,
        "status_set": datetime.now().timestamp() - 120
    }]

    def apply(route):
        routes = route.copy()

    close_location_to_second.message = A()
    close_location_to_second.message.location = A()
    close_location_to_second.message.chat_id = "abc"

    close_location_to_second.message.location.latitude = 55.726866
    close_location_to_second.message.location.longitude = 37.450563
    close_location_to_second.effective_chat = A()

    context = A()
    context.chat_data = dict()

    count = 0

    async def ctr(*args, **kwargs):
        nonlocal count
        count += 1
    close_location_to_second.effective_chat.send_message = ctr

    with patch("basichandlers.issue_info", new_callable=AsyncMock) as mock_issue_info:
        mock_issue_info.side_effect = None
        mock_issue_info.return_value = None
        await locationtracker.update_location.__wrapped__(
            close_location_to_second, context, routes, apply)
        assert (count == 0)


@pytest.mark.asyncio
async def test_0_to_2_slow(setup_namemanager):
    routes = [{
        "start": 's9601261',
        "end": 's9601728',
        "status": 0,
        "status_set": 1716570256.743725
    },
        {
        "start": 's9601728',
        "end": 's9601666',
        "status": 0,
        "status_set": 1716570256
    }]

    def apply(route):
        routes = route.copy()

    close_location_to_second.message = A()
    close_location_to_second.message.location = A()
    close_location_to_second.message.chat_id = "abc"

    close_location_to_second.message.location.latitude = 55.726866
    close_location_to_second.message.location.longitude = 37.450563
    close_location_to_second.effective_chat = A()

    context = A()
    context.chat_data = dict()

    count = 0

    async def ctr(*args, **kwargs):
        nonlocal count
        count += 1
    close_location_to_second.effective_chat.send_message = ctr

    with patch("basichandlers.issue_info", new_callable=AsyncMock) as mock_issue_info:
        mock_issue_info.side_effect = None
        mock_issue_info.return_value = None
        await locationtracker.update_location.__wrapped__(
            close_location_to_second, context, routes, apply)
        assert (count == 0)
