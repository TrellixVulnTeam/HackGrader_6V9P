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

You can run the client with `python client.py`
