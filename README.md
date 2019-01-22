# low-hanging
`low-hanging` aims to be lightweight and extensible horizontal vulnerability scanner. 

Just pass list of domains/IPs and `low-hanging` will check for easily detectable vulnerabilities with low false positive rate.

Made to be easily extensible. Adding more checks is just few lines of code with features like JS rendering in your possession thanks to `requests-html`.

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

- Return url in case of detected vulnerability
- You don't have to handle exceptions, they'll just get swallowed
## Example Module
```python
from low_hanging.base_worker import BaseWorker


class DjangoDebug(BaseWorker):
    name = "django_debug"
    references = ["https://stackoverflow.com/questions/14470601/debug-true-django"]
    def run(self):
        path = self.random_string()
        r = self.scrape(path)  # wrapper for self.session.request(method, urljoin(self.domain, path), timeout=5)
        if "DEBUG" in r.text:
            return r.url  # If successful, return the URL for which the exploit is valid
```
