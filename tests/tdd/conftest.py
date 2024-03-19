import pytest
from pytest_factoryboy import register

from tdd.factories import MemberFactory


register(MemberFactory)


@pytest.fixture(scope="function", autouse=True)
def tmp_media(tmpdir, settings):
    settings.MEDIA_ROOT = tmpdir.mkdir("media")