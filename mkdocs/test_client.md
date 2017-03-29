# Test Client

This is a simple Python test client for testing the grader.

In order to use it, copy `example_settings.py` to `settings.py` and `example_nonce.json` to `nonce.json`.

For `settings.py` you should have:

1. API Key/Secret, generated from a grader instance
2. Some grader URLs to point to.

For `nonce.json` you can leave it like that:

```json
{
}
```

# How to use test_client
1. Run Celery. `$ celery -A hacktester worker -B -E --loglevel=info`
2. Run local server in another terminal. `$ python3 manage.py runserver`
3. In another terminal. `$ cd /test_client && python3 client.py`
4. If you want to test only specific language you have to open the `client.py` and comment the other functions.
5. If you want to test different behaviour which is not covered you can create new functions following these steps:
    * Create `your_awesome_function()` where describe the data to be passed to the grader
    * `make_request(your_awesome_function())` in `main()`
    * Create the files you need in `/fixtures` directory
    * Follow steps 1. 2. 3. & 4.