from tests import conftest
import pytest


@pytest.mark.vcr
async def test_get_tweet_by_id() -> None:
    await conftest.get_tweet_by_id()


@pytest.mark.vcr
async def test_get_user_by_screen_name() -> None:
    await conftest.get_user_by_screen_name()


@pytest.mark.vcr
async def test_get_user_by_id() -> None:
    await conftest.get_user_by_id()


@pytest.mark.vcr
async def test_get_user_videos() -> None:
    await conftest.get_user_videos()


@pytest.mark.vcr
async def test_get_user_photos() -> None:
    await conftest.get_user_photos()
