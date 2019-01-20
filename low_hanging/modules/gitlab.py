from low_hanging.base_worker import BaseWorker


class GitlabExplore(BaseWorker):
    name = "gitlab_exposed"
    references = ["https://twitter.com/edoverflow/status/986214497965740032"]
    def run(self):
        paths = ["explore", "explore/projects"]
        for path in paths:
            r = self.scrape(path)
            if "gitlab" in r.text and "No projects found" not in r.text:
                return r.url