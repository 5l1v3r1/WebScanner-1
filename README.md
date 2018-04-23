# CS5331 - Assignment 3 - Web Scanner
## Dependencies
* scrapy
```sh
sudo pip install scrapy
```
* python requests module
```sh
sudo apt-get install python-pip
```

## Total scan
`MainScanner.py` runs the crawler, then scans for various vulnerability categories, outputting vulnerabilities in `./vulnerabilities/*.json` and POC exploit scripts to `./scripts/`

Usage:
```sh
python MainScanner.py
```

## Crawler
The crawler crawls all `<a>` tags as well as all submitted `<form>` tags, and record all `GET` requests with query parameters and requests from `<form>` tags

Usage:
```sh
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

## SQL Injection
Using `sqlmap`

## Server Side Code Injection
Getting php page's source code

## Directory Traversal
Stealing `/etc/passwd`

## Open Redirect
Force redirection to https://status.github.com/messages

## Command Injection
Injecting `uname -a`
