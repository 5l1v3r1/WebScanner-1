Modified from https://github.com/ak1t4/open-redirect-scanner/blob/master/redirect.py

Usage (Against Benchmark VM's Open Redirect):
./lol.sh

Payloads are different methods to ensure it redirects.

TODO:
- Take in GET and POST param values (static GET param at the moment for benchmark vm)
- Support for POST param
- Implement check to ensure it is redirected to the correct page
- Once ONE payload is successful, repeat payload. If successful again, stop and generate exploit with that payload.
- Generate JSON.