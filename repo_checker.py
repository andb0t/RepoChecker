"""This script checks github repositories for actvity."""
import json
from collections import OrderedDict
from datetime import datetime, timedelta
import urllib.request

import tabulate


urls = [
    "https://api.github.com/repos/andb0t/MLlab",
    "https://api.github.com/repos/smicallef/spiderfoot",
    "https://api.github.com/repos/nicolasbeauvais/laravel-botscout"
    # "https://gitlab.com/api/v4/projects/gitlab-org%2Fci-cd%2Fdocker-machine"
]

responses = []
for url in urls:
    response = urllib.request.urlopen(url)
    data = response.read()
    responses.append(json.loads(data))

headers = OrderedDict({
    "updated": {"github": "updated_at", "gitlab": "updated_at"},
    "watchers": {"github": "watchers", "gitlab": "watchers"},
    "subscribers": {"github": "subscribers_count", "gitlab": "subscribers_count"},
    "open_issues": {"github": "open_issues", "gitlab": "open_issues"},
    "forks": {"github": "forks", "gitlab": "forks"}
})

table = []
for url, response in zip(urls, responses):
    entry = [url]
    for header in headers.values():
        if 'github' in url:
            key = header['github']
        elif 'gitlab' in url:
            key = header['gitlab']
        else:
            raise NotImplementedError('unknown git hosting service')
        text = response[key]
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
print(tabulate.tabulate(table, ['URL', *list(headers.keys())], tablefmt="grid"))
