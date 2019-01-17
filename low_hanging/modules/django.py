from low_hanging.base_worker import BaseWorker


class DjangoDebug(BaseWorker):
    name = "django_debug"
    def run(self):
        path = self.random_string()
        r = self.scrape(path)
        if "DEBUG" in r.text:
            return r.url