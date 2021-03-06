#!/usr/bin/env python

import os
from sys import stdout
import json

targetsFile = 'targets' + '.json'

# Crawl if haven't done so
if os.path.exists(targetsFile):
    print '%s found, crawling skipped' % targetsFile
else:
    ret = os.system('scrapy crawl main -o %s' % targetsFile)
    if ret: exit(ret)

print '# Targets to scan for vulnerabilities:'
stdout.flush()
os.system('cat %s' % targetsFile)
print

# Scan
print '# Scanning for vulnerabilities...'
stdout.flush()
os.system('rm -rf vulnerabilities/')
os.makedirs('vulnerabilities')
os.system('rm -rf scripts/')
os.makedirs('scripts')

from scanners import Scanners
scanners = { scanner: Scanners[scanner](targetsFile) for scanner in Scanners }

for className in scanners:
    scanner = scanners[className]
    print '\n## Scanning for', scanner.className, 'vulnerabilities...'
    stdout.flush()

    vulnerabilities = scanner.scanVulnerabilities()
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
