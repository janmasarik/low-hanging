import random
import string

from requests_html import HTMLSession
from urllib.parse import urljoin


class BaseWorker:
    name = "default"

    def __init__(self, domain, session=None):
        self.domain = domain
        self.session = session or HTMLSession()

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self):
        raise NotImplementedError

    def scrape(self, path, method="GET"):
        return self.session.request(method, urljoin(self.domain, path))

    @staticmethod
    def random_string(length=10):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
