from dataclasses import dataclass
from pathlib import Path
import dotenv

import twikit

TESTS = Path('tests')

TEST_DATA = TESTS / 'test_data'
X_FILES = TEST_DATA / 'x.com'
TWIMG_FILES = TEST_DATA / 'abs.twimg.com'

ENV_FILE = TESTS / '.env'


TWITTER_DOMAIN = twikit.constants.DOMAIN
ABS_TWIMG_DOMAIN = 'abs.twimg.com'

TWITTER_URL = f'https://{TWITTER_DOMAIN}/'
ABS_TWIMG_URL = f'https://{ABS_TWIMG_DOMAIN}/'

config = dotenv.dotenv_values(ENV_FILE, verbose=True)
COOKIEJAR = config.get('COOKIEJAR', None)
if not COOKIEJAR:
    raise ValueError('COOKIEJAR is None')
USER_AGENT = config.get('USER_AGENT', None)
if not USER_AGENT:
    raise ValueError('USER_AGENT is None')


@dataclass
class TestUser:
    rest_id: str
    screen_name: str


@dataclass
class TestTweet:
    user: TestUser
    rest_id: str
    text: str


TEST_USER_1 = TestUser('44196397', 'elonmusk')
TEST_USER_2 = TestUser('18927441', 'IGN')
TEST_USER_3 = TestUser('2367911', 'MTV')

TEST_TWEET_1 = TestTweet(TEST_USER_1, '2029384571788407254', 'Grok can watch videos for you')
TEST_TWEET_2 = TestTweet(
    TEST_USER_2,
    '2027957271913705526',
    'Resident Evil Requiem director Koshi Nakanishi has revealed that Capcom was initially unsure whether Switch 2 would be powerful enough to run its new survival horror blockbuster. https://t.co/FDOGcSsfvp https://t.co/0CPWf6fqXC',
)
TEST_TWEET_3 = TestTweet(TEST_USER_3, '2027866402929918312', 'aaa')
TEST_TWEET_4 = TestTweet(TEST_USER_3, '2027760707362500970', 'aaa')


def get_client() -> twikit.Client:
    """Build a twikit Client with the given cookies file."""
    client = twikit.Client(user_agent=USER_AGENT)
    client.http.cookies.clear()
    client.load_cookies(COOKIEJAR)
    return client


async def get_tweet_by_id() -> None:
    client = get_client()
    tweet = await client.get_tweet_by_id(TEST_TWEET_2.rest_id)
    assert tweet.id == TEST_TWEET_2.rest_id
    assert tweet.text == TEST_TWEET_2.text
    assert tweet.user.id == TEST_TWEET_2.user.rest_id


async def get_user_by_screen_name() -> None:
    client = get_client()
    user = await client.get_user_by_screen_name(TEST_USER_1.screen_name)
    assert user.screen_name == TEST_USER_1.screen_name
    assert user.id == TEST_USER_1.rest_id


async def get_user_by_id() -> None:
    client = get_client()
    user = await client.get_user_by_id(TEST_USER_1.rest_id)
    assert user.screen_name == TEST_USER_1.screen_name
    assert user.id == TEST_USER_1.rest_id


async def get_user_videos() -> None:
    seen_tweets: set[str] = set()

    def read_tweets(tweets: list[twikit.Tweet]):
        assert len(tweets) > 1
        for tweet in tweets:
            assert tweet.id not in seen_tweets
            seen_tweets.add(tweet.id)
            assert len(tweet.media) > 0
            for media in tweet.media:
                assert media.type == 'video'

    client = get_client()
    # first page
    video_tweets = await client.get_user_tweets(TEST_USER_3.rest_id, 'Videos', count=20)
    read_tweets(list(video_tweets))
    # second page
    video_tweets = await video_tweets.next()
    read_tweets(list(video_tweets))


async def get_user_photos() -> None:
    seen_tweets: set[str] = set()

    def read_tweets(tweets: list[twikit.Tweet]):
        assert len(tweets) > 1
        for tweet in tweets:
            assert tweet.id not in seen_tweets
            seen_tweets.add(tweet.id)
            assert len(tweet.media) > 0
            for media in tweet.media:
                assert media.type == 'photo'

    client = get_client()
    # first page
    photo_tweets = await client.get_user_tweets(TEST_USER_3.rest_id, 'Photos', count=20)
    read_tweets(list(photo_tweets))
    # second page
    photo_tweets = await photo_tweets.next()
    read_tweets(list(photo_tweets))
