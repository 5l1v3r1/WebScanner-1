# CS331 - Assignment 3 - Web Scanner
## Crawler
The crawler crawls all `<a>` tags as well as all submitted `<form>` tags, and record all `GET` requests with query parameters and requests from `<form>` tags

Usage:
```sh
sudo pip install scrapy
scrapy crawl main -o targets.json
```
Sample output `targets.json`:
```json
[
{"action": "http://target.com/commandinjection/commandinjection.php", "inputs": [{"name": "host"}], "method": "POST"},
{"action": "http://target.com/sqli/sqli.php", "inputs": [{"name": "username"}], "method": "POST"},
{"action": "http://target.com/csrf/csrf.php", "inputs": [{"name": "secret"}, {"name": "csrftoken"}], "method": "POST"},
{"action": "http://target.com/serverside/serverside.php", "inputs": [{"name": "page"}], "method": "GET"},
{"action": "http://target.com/directorytraversal/directorytraversal.php", "inputs": [{"name": "ascii"}], "method": "GET"}
]
```

## Open Redirect
