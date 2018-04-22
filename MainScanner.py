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
os.system('rm -rf vulnerabilities/')
os.makedirs('vulnerabilities')
os.system('rm -rf scripts/')
os.makedirs('scripts')

## 3. Directory Traversal
from scanners.DirectoryTraversalScanner import DirectoryTraversalScanner as DTS
## 6. Command Injection
from scanners.CommandInjectionScanner import CommandInjectionScanner as CIS

scanners = {
    'directorytraversal': DTS(targetsFile),
    'commandinjection': CIS(targetsFile)
}
for className in scanners:
    scanner = scanners[className]
    vulnerabilities = scanner.scanVulnerabilities()

    print 'Scan results:'
    print vulnerabilities
    with open('vulnerabilities/%s.json' % className, 'w') as vulnerabilityFile:
        json.dump(vulnerabilities, vulnerabilityFile,
                indent=4, separators=(',', ': '))
        vulnerabilityFile.write('\n')
    print 'Written to vulnerabilities/%s.json' % className

    i = 0
    for domain in vulnerabilities['results']:
        for vulnerability in vulnerabilities['results'][domain]:
            script = scanner.generateExploit(domain, vulnerability)
            with open('scripts/%s-%02d.sh' % (className, i), 'w') as scriptFile:
                scriptFile.write(script)
            os.chmod('scripts/%s-%02d.sh' % (className, i), 0755)
            i += 1
    print 'Generated scripts/%s-*.sh' % className
