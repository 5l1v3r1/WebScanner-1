#!/usr/bin/env python

import os
import json

targetsFile = 'targets' + '.json'

# Crawl if haven't done so
if os.path.exists(targetsFile):
    print '%s found, crawling skipped' % targetsFile
else:
    ret = os.system('scrapy crawl main -o %s' % targetsFile)
    if ret: exit(ret)

print 'Targets to scan for vulnerabilities:'
os.system('cat %s' % targetsFile)
print

# Scan
print 'Scanning for vulnerabilities...'
if not os.path.exists('vulnerabilities/'):
    os.makedirs('vulnerabilities')
if not os.path.exists('scripts/'):
    os.makedirs('scripts')

## 6. Command Injection
from scanners.CommandInjectionScanner import CommandInjectionScanner as CIS

ciS = CIS(targetsFile)
ciV = ciS.scanVulnerabilities()

print 'Scan results:'
print ciV
with open('vulnerabilities/commandinjection.json', 'w') as ciFile:
    json.dump(ciV, ciFile, indent=4, separators=(',', ': '))
    ciFile.write('\n')
print 'Written to vulnerabilities/commandinjection.json'

i = 0
for domain in ciV['results']:
    for vulnerability in ciV['results'][domain]:
        script = ciS.generateExploit(domain, vulnerability)
        with open('scripts/commandinjection-%02d.sh' % i, 'w') as scriptFile:
            scriptFile.write(script)
        os.chmod('scripts/commandinjection-%02d.sh' % i, 0755)
        i += 1
print 'Generated scripts/commandinjection-*.sh'
