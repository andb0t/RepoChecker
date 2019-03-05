"""This script checks github repositories for actvity."""
import json
from datetime import datetime, timedelta
import urllib.request

import tabulate


urls = [
    "https://api.github.com/repos/andb0t/MLlab",
    "https://api.github.com/repos/smicallef/spiderfoot",
    "https://api.github.com/repos/nicolasbeauvais/laravel-botscout"
]

responses = []
for url in urls:
    response = urllib.request.urlopen(url)
    data = response.read()
    responses.append(json.loads(data))

headers = [
    "updated_at",
    "watchers",
    "subscribers_count",
    "open_issues",
    "forks"
]

table = []
for url, response in zip(urls, responses):
    entry = [url]
    for header in headers:
        text = response[header]
        try:
            time = datetime.strptime(text, '%Y-%m-%dT%H:%M:%SZ')
            # text = time.strftime('%d.%m.%Y')
            diff_days = (datetime.now() - time).days
            text = '%s days ago' % diff_days
        except TypeError:
            pass
        entry.append(text)
    table.append(entry)

table = sorted(table, key=lambda x: x[0], reverse=True)

# print(responses[0].keys())
print(tabulate.tabulate(table, ['URL', *headers], tablefmt="grid"))
