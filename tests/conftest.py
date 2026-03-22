from pathlib import Path
import dotenv
import twikit
import httpx
import respx
from respx.patterns import M
from dataclasses import dataclass


TESTS = Path('tests')

TEST_DATA = TESTS / 'test_data'
DUMMY_COOKIES = str(TESTS / 'dummy_cookies.txt')  # actually JSON
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


def make_routes(router: respx.Router, dir: Path, host: str) -> None:
    """Create a route for each file in the directory."""
    for file in dir.rglob('*'):
        if file.is_dir():
            continue
        rel_file = file.relative_to(dir)

        # special case where path is "/"
        if rel_file.name == '_home':
            path = '/'
        else:
            path = rel_file.as_posix()

        response = httpx.Response(200, content=file.read_bytes())
        pat = M(host=host, path=path)
        router.route(pat, name=file.name).mock(return_value=response)


router_x = respx.mock(base_url=TWITTER_URL, assert_all_mocked=True, assert_all_called=False)
router_twimg = respx.mock(base_url=ABS_TWIMG_URL, assert_all_mocked=True, assert_all_called=False)

make_routes(router_twimg, TWIMG_FILES, ABS_TWIMG_DOMAIN)
make_routes(router_x, X_FILES, TWITTER_DOMAIN)


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


def get_client(cookies_path: str) -> twikit.Client:
    """Build a twikit Client with the given cookies file."""
    client = twikit.Client()
    client.http.cookies.clear()
    client.load_cookies(cookies_path)
    return client


async def get_tweet_by_id(cookies: str) -> None:
    client = get_client(cookies)
    tweet = await client.get_tweet_by_id(TEST_TWEET_2.rest_id)
    assert tweet.id == TEST_TWEET_2.rest_id
    assert tweet.text == TEST_TWEET_2.text
    assert tweet.user.id == TEST_TWEET_2.user.rest_id
    assert router_x['TweetDetail'].called
    assert router_x['TweetDetail'].call_count == 1


async def get_user_by_screen_name(cookies: str) -> None:
    client = get_client(cookies)
    user = await client.get_user_by_screen_name(TEST_USER_1.screen_name)
    assert user.screen_name == TEST_USER_1.screen_name
    assert user.id == TEST_USER_1.rest_id
    assert router_x['UserByScreenName'].called
    assert router_x['UserByScreenName'].call_count == 1


async def get_user_by_id(cookies: str) -> None:
    client = get_client(cookies)
    user = await client.get_user_by_id(TEST_USER_1.rest_id)
    assert user.screen_name == TEST_USER_1.screen_name
    assert user.id == TEST_USER_1.rest_id
    assert router_x['UserByRestId'].called
    assert router_x['UserByRestId'].call_count == 1
