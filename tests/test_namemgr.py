import namemanager
import pytest


@pytest.fixture
def setup_namemanager():
    namemanager.init()


def test_existing(setup_namemanager):

    res = namemanager.resolve_name("новодачная")
    assert (len(res) != 0)
    assert ("Новодачная" in namemanager.resolve_id(res[0]["id"])["title"])


def test_nonexisting(setup_namemanager):
    res = namemanager.resolve_name("новодачнейшая")
    assert (len(res) == 0)
