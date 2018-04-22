
# STATUS

WORKING:
- Injecting to a single endpoint (URL)
- Supply parameters and their values
- Perform redirection successfully on Benchmark VM
- Print out result in JSON (timestamp.json), generate exploit script (timestamp.sh)
-- Sample files available.

TODO:
- Implement supplying of cookie file
- ***INTEGRATE WITH MAIN SCANNER (ESPECIALLY ON PARAMETER-VALUE PAIR)

==============================================

### WARNING: requests MUST be installed.
Looks like running sudo apt-get install python-pip will install requests automatically.

Redirect script for CS5331 Purposes

### Command:
```sh 
python redirect.py <targetURL> <paramfile> <payloadfile> (cookiefile) 
```
### Example: 
```sh 
python redirect.py http://target.com/openredirect/openredirect.php param.txt payload.txt cookie.txt 
```

```<targetURL>```: Contains the URL you wish to target. Example: http://target.com/openredirect/openredirect.php

```<paramfile>```: Contains the parameters. MUST HAVE FILE PRESENT.
Sample File: G = GET, P = POST, added before actual param names.
Gsid=234512213443
Gredirect
Program will always run in GET mode unless POST params are detected.

```<payloadfile>```: Contains the payload needed to redirect to https://status.github.com. MUST HAVE FILE PRESENT.

```(cookiefile)``` OPTIONAL: If cookie file is present, will attempt to load the cookies into the request. The format is as such:
Sample File:
enwiki_session|17ab96bd8ffbe8ca58a78657a918558

### Sample:
```sh
cs5331@benchmark:~/Desktop/VB/redirect$ python redirect.py http://target.com/openredirect/openredirect.php param.txt payload.txt 
NOTE: FIRST TWO PAYLOADS ARE GUARANTEED TO FAIL FOR TESTING PURPOSES.

Trying with payload: //3H6k7lIAiqjfNeN@example.com@status.github.com/messages/ .... Failed.
Trying with payload: //XY>.7d8T\205pZM@example.com@status.github.com/messages/ .... Failed.
Trying with payload: https://status.github.com/messages/%2e%2e%2f .... Success.

23042018-033801.json generated.
23042018-033801.sh generated.
```