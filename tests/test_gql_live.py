import pytest
from tests import conftest


@pytest.mark.skip(reason='TODO: Need real credentials')
async def test_get_user_by_screen_name_live() -> None:
    await conftest.get_user_by_screen_name(cookies='')


@pytest.mark.skip(reason='TODO: Need real credentials')
async def test_get_user_by_id_live() -> None:
    await conftest.get_user_by_id(cookies='')
