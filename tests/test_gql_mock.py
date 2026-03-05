from tests import conftest


@conftest.router_twimg
@conftest.router_x
async def test_get_tweet_by_id() -> None:
    await conftest.get_tweet_by_id(cookies=conftest.DUMMY_COOKIES)


@conftest.router_twimg
@conftest.router_x
async def test_get_user_by_screen_name() -> None:
    await conftest.get_user_by_screen_name(cookies=conftest.DUMMY_COOKIES)


@conftest.router_twimg
@conftest.router_x
async def test_get_user_by_id() -> None:
    await conftest.get_user_by_id(cookies=conftest.DUMMY_COOKIES)
