import concurrent.futures
import click
import click_log
import json
import logging
import requests

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from requests_html import HTMLSession
from tqdm import tqdm

from low_hanging.modules import DjangoDebug, PhpInfo, PortainerAdmin, GitlabExplore, MinioDefaultCreds, ArgoNoAuth

log = logging.getLogger()
click_log.basic_config(log)

requests.packages.urllib3.disable_warnings()

def gather(domains, threads):
    enabled_modules = [DjangoDebug, PhpInfo, PortainerAdmin, GitlabExplore, MinioDefaultCreds, ArgoNoAuth]
    session = HTMLSession()
    session.verify = False
    results = defaultdict(list)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for worker in tqdm(enabled_modules, desc="modules"):

            future_to_name = {executor.submit(worker(url, session)): worker.name for url in domains}
            for future in tqdm(concurrent.futures.as_completed(future_to_name), total=len(future_to_name), unit=" requests"):
                worker_name = future_to_name[future]
                try:
                    result = future.result()
                    if not result:
                        continue

                    results[worker_name].append(result)
                except Exception as e:
                    log.debug("{}\nWorker {} failed!".format(e,worker_name))

    return results

@click.command()
@click.option('-i', '--input', 'input_filename', help='Path to file with list of domains/IPs separated by newline.')
@click.option('-o', '--output', 'output_file', help='Output files to file in json format.')
@click.option('-t', '--threads', default=50, help='Number of threads with which you want to run.')
@click_log.simple_verbosity_option(log)
def main(input_filename, threads, output_file):
    domains = []
    with open(input_filename) as domains_file:
        for host in domains_file.read().splitlines():
            domains.extend([f"http://{host}", f"https://{host}"])

    results = gather(domains, threads)
    click.echo(json.dumps(results, indent=4, sort_keys=True))

    if output_file:
        with open(output_file, "w") as f:
            json.dump(results, f, sort_keys=True)


if __name__ == '__main__':
    main()