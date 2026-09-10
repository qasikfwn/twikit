import httpx
import asyncio

import re


js_bundle_pat = re.compile(
    r'https://abs\.twimg\.com/responsive-web/client-web/main\.[a-f0-9]*?\.js'
)
endpoint_pat = re.compile(r'exports=\{queryId:\"([a-zA-Z0-9_]*?)\",operationName:\"([a-zA-Z]*?)\"')


async def main() -> None:
    client = httpx.AsyncClient()
    response = await client.get('https://x.com/home', follow_redirects=True)

    if response.is_error:
        print(f'Error {response.status_code}')
        return
    home_data = await response.aread()
    home = home_data.decode('utf-8')

    main_js_bundles = re.findall(js_bundle_pat, home)
    if len(main_js_bundles) == 0:
        print('No main.js bundles found')
        return
    main_js_bundle: str = main_js_bundles[0]

    response = await client.get(main_js_bundle, follow_redirects=True)
    if response.is_error:
        print(f'Error {response.status_code}')
        return
    main_js_data = await response.aread()
    main_js = main_js_data.decode('utf-8')

    matches = re.findall(endpoint_pat, main_js)
    for match in matches:
        print(f'{match[0]}/{match[1]}')


if __name__ == '__main__':
    asyncio.run(main())
