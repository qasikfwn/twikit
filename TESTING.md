To refresh testing data:
1. Ensure `tests/.env` is up to date. `COOKIEJAR` should point to a json file containing cookies.
2. Delete `tests/cassettes/`
3. Run `uv run pytest --record-mode=once`. The tests will be run and live API responses will be recorded.
4. Run `uv run pytest` as many times as you please; no real network requests will be made.

To update endpoints:
1. Run `uv run tests/collect_endpoints.py` to fetch `https://x.com/home`, fetch the current `main.js` bundle, and print out the current endpoints.