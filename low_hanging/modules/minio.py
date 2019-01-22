import logging
import contextlib

from urllib.parse import urljoin
from low_hanging.base_worker import BaseWorker

log = logging.getLogger()

class MinioDefaultCreds(BaseWorker):
    name = "minio_default_creds"
    references = ["https://github.com/argoproj/argo/blob/master/demo.md#5-install-an-artifact-repository",
                  "https://github.com/minio/minio/blob/master/docs/orchestration/docker-compose/docker-compose.yaml",
                  "https://github.com/minio/minio/blob/master/docs/config/README.md#credential"]

    def run(self):
        base_url = f"{self.domain}:{9000}"
        key_pairs = [("AKIAIOSFODNN7EXAMPLE", "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"),
                     ("minio", "minio123"),
                     ("admin", "password")]

        for access_key, secret_key in key_pairs:
            with contextlib.suppress(Exception):
                r = self.session.post(
                    urljoin(base_url, "/minio/webrpc"),
                    json={
                        "id": 1, "jsonrpc": "2.0",
                        "params": {"username": access_key, "password": secret_key},
                        "method": "Web.Login"
                    },
                    timeout=5
                )

                if r.json()['result'].get('token'):
                    return r.url
