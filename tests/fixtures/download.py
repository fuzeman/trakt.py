from datetime import datetime
from urlparse import urlparse
import itertools
import json
import os
import requests
import sys
import time

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


def download(url):
    requested_at = None

    for choice in itertools.product(*parse_url(url)):
        requested_at = datetime.now()

        if not download_one(''.join(choice)):
            continue

        delay = 5 - (datetime.now() - requested_at).total_seconds()

        if delay > 0:
            print('Waiting %d second(s)' % (delay,))
            time.sleep(delay)


def download_one(url):
    # Parse URL
    url_parsed = urlparse(url)

    if not url_parsed.netloc or not url_parsed.path:
        print('[%s] Missing netloc or path' % (url,))
        return False

    # Build destination path
    destination = os.path.abspath(os.path.join(CURRENT_DIR, url_parsed.netloc) + url_parsed.path + '.json')

    if os.path.exists(destination):
        print('[%s] Fixture already exists at: %r' % (url, destination))
        return False

    # Ensure directory exists
    directory = os.path.dirname(destination)

    if not os.path.exists(directory):
        os.makedirs(directory)

    # Send request
    print('[%s] Request' % (url,))

    try:
        response = requests.get(url, timeout=12, headers={
            'Content-Type':      'application/json',
            'trakt-api-key':     '3a239f26f02da9b9ff2e2d9057150a7e01cf8f6f1f2f487fb9d9d39e9c59f5a3',
            'trakt-api-version': '2'
        })
    except Exception as ex:
        print('[%s] Request failed: %s' % (url, ex))
        return False

    # Parse JSON Body
    try:
        data = json.loads(response.content)
    except Exception as ex:
        print('[%s] Invalid body: %s' % (url, ex))
        return False

    # Save response body to file
    with open(destination, 'wb') as fp:
        json.dump(
            data, fp,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )

    print('[%s] Done' % (url,))
    return True


def parse_url(url):
    result = []

    current = ''
    pos = 0

    while pos < len(url):
        ch = url[pos]

        if ch == '{':
            # Append current fragment to `result`
            if current:
                result.append([current])
                current = ''

            # Find matching end token
            end = url.find('}', pos)

            # Append choice list to `result`
            result.append(url[pos + 1:end].split(','))

            # Update position
            pos = end + 1
            continue

        # Append character to current fragment
        current += ch
        pos += 1

    if current:
        result.append([current])

    return result


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit(1)

    download(sys.argv[1])
