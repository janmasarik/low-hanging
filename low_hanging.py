import concurrent.futures
import click
import json
import logging

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from requests_html import HTMLSession
from tqdm import tqdm

from low_hanging.modules import DjangoDebug, PhpInfo, PortainerAdmin, GitlabExplore


log = logging.getLogger()

def gather(domains, threads, timeout=5):
    enabled_modules = [DjangoDebug, PhpInfo, PortainerAdmin, GitlabExplore]
    session = HTMLSession()
    session.timeout = timeout
    results = defaultdict(list)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for worker in tqdm(enabled_modules):

            future_to_name = {executor.submit(worker(url, session)): worker.name for url in domains}
            for future in concurrent.futures.as_completed(future_to_name):
                worker_name = future_to_name[future]
                try:
                    result = future.result()
                    if not result:
                        continue

                    results[worker_name].append(result)
                except Exception as e:
                    click.echo("{}\nWorker {} failed!".format(e,worker_name), err=True)

    return results

@click.command()
@click.option('-d', '--domains', 'domains_filename', help='Path to file with list of domains separated by newline.')
@click.option('-t', '--threads', default=50, help='Number of threads with which you want to run.')
@click.option('-o', '--output', 'output_file', help='Output files to file in json format.')
def main(domains_filename, threads, output_file):
    with open(domains_filename) as domains_file:
        domains = domains_file.read().splitlines()

    results = gather(domains, threads)
    click.echo(json.dumps(results))

    if output_file:
        with open(output_file, "w") as f:
            json.dump(results, f)


if __name__ == '__main__':
    main()