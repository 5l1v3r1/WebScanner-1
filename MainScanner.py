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
if not os.path.exists('vulnerabilities/'):
    os.makedirs('vulnerabilities')
if not os.path.exists('scripts/'):
    os.makedirs('scripts')
print 'Scan results:'
## 6. Command Injection
ciS = CIS(targetsFile)
ciV = ciS.scanVulnerabilities()

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
