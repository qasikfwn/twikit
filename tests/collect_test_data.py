"""Interact with the live Twitter api to collect real responses."""

import twikit
import asyncio
import httpx
import conftest


async def dump_reponse(response: httpx.Response) -> None:
    if response.url.path == '/':
        file = conftest.TEST_DATA / response.url.host / '_home'
    else:
        file = conftest.TEST_DATA / response.url.host / response.url.path.removeprefix('/')
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_bytes(await response.aread())


async def log_url(request: httpx.Request) -> None:
    print(request.url)


async def main() -> None:
    """Get an example response from each GQL endpoint"""

    client = twikit.Client(
        user_agent=conftest.USER_AGENT,
        event_hooks={'request': [log_url], 'response': [dump_reponse]},
    )

    client.http.cookies.clear()
    client.load_cookies(conftest.COOKIEJAR)

    await client.gql.user_by_screen_name(conftest.TEST_USER_1.screen_name)
    await client.gql.user_by_rest_id(conftest.TEST_USER_1.rest_id)
    await client.gql.tweet_result_by_rest_id(conftest.TEST_TWEET_2.rest_id)
    await client.gql.tweet_results_by_rest_ids(
        [conftest.TEST_TWEET_3.rest_id, conftest.TEST_TWEET_4.rest_id]
    )
    await client.gql.user_tweets(user_id=conftest.TEST_USER_2.rest_id, count=20, cursor=None)
    await client.gql.tweet_detail(tweet_id=conftest.TEST_TWEET_2.rest_id, cursor=None)


asyncio.run(main())
