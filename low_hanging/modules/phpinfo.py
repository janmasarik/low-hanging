from low_hanging.base_worker import BaseWorker


class PhpInfo(BaseWorker):
    name = "phpinfo_exposed"
    references = ["https://hackerone.com/reports/165930"]
    def run(self):
        paths = ["phpinfo.php", "info.php"]  # remove info.php for lower false positives
        for path in paths:
            r = self.scrape(path)
            if "php version" in r.text.lower():
                return r.url