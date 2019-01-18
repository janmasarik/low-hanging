from low_hanging.base_worker import BaseWorker


class DjangoDebug(BaseWorker):
    name = "django_debug"
    references = ["https://stackoverflow.com/questions/14470601/debug-true-django"]
    def run(self):
        path = self.random_string()
        r = self.scrape(path)
        if "DEBUG" in r.text:
            return r.url