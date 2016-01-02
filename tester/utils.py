from urllib.parse import urlsplit


def get_base_url(uri):
    return "{0.scheme}://{0.netloc}".format(urlsplit(uri))
