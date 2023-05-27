import pytest

from tests.settings import LANGUAGE_CODE


@pytest.fixture(scope='session', autouse=True)
def faker_session_locale():
    return [LANGUAGE_CODE]


@pytest.fixture(scope='session')
def uploads_path():
    from lnreader.models import UPLOADS_PATH
    return UPLOADS_PATH
