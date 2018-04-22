#!/usr/bin/env python

import os
import json

from scanners.CommandInjectionScanner import CommandInjectionScanner as CIS

targetsFile = 'targets' + '.json'

# Crawl
os.system('rm -f %s' % targetsFile)
ret = os.system('scrapy crawl main -o %s' % targetsFile)
if ret: exit(ret)

print 'Targets to scan for vulnerabilities:'
os.system('cat %s' % targetsFile)
print

# Scan
print 'Scan results:'
## 6. Command Injection
ciS = CIS(targetsFile)
ciV = ciS.scanVulnerabilities()

print ciV
if not os.path.exists('vulnerabilities/'):
    os.makedirs('vulnerabilities')
with open('vulnerabilities/commandinjection.json', 'w') as ciFile:
    json.dump(ciV, ciFile, indent=4, separators=(',', ': '))
    ciFile.write('\n')
print 'Written to vulnerabilities/commandinjection.json'
