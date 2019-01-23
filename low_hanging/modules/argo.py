from low_hanging.base_worker import BaseWorker


class ArgoNoAuth(BaseWorker):
    name = "argo_no_auth"
    references = ["https://github.com/argoproj/argo/blob/master/demo.md#method-1-kubectl-port-forward"]
    def run(self):
        r = self.scrape("workflows", port=8001)
        if r.html.find('title')[0].text == "Argo":
            return r.url
