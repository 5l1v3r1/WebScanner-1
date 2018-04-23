import os
from urllib import urlretrieve
from zipfile import ZipFile
from shutil import rmtree
from glob import glob
from subprocess import check_output
from csv import DictReader
from urlparse import urlparse
from copy import deepcopy

from Scanner import Scanner

class SQLInjectionScanner(Scanner):
    className = "SQL Injection"

    def __init__(self, *args, **kwargs):
        super(SQLInjectionScanner, self).__init__(*args, **kwargs)
        OLDPWD = os.getcwd()
        os.chdir(__package__)
        if not os.path.exists('sqlmap'):
            urlretrieve('https://github.com/sqlmapproject/sqlmap/zipball/master', 'sqlmap.zip')
            os.mkdir('sqlmap')
            with ZipFile('sqlmap.zip','r') as zip_ref:
                zip_ref.extractall("sqlmap")
            os.remove('sqlmap.zip')
        os.chdir(OLDPWD)

    def scanVulnerabilities(self):
        OLDPWD = os.getcwd()
        os.chdir(__package__)

        if os.path.exists('sqlmap/output') and os.path.isdir('sqlmap/output'):
            rmtree('sqlmap/output')
        if os.path.exists('sqlmap/urls'):
            os.remove('sqlmap/urls')

        with open('sqlmap/urls', 'w') as urlfile:
            for target in self.targets:
                urlfile.write(target['action'] + "\n")

        command = 'python ' + glob('sqlmap/sqlmapproject-sqlmap-*')[0] + '/sqlmap.py' + \
        ' -m sqlmap/urls --batch --forms --answers=\"involving it=n\" --technique BEUS -o --output-dir=sqlmap/output'
        out = check_output(command, shell=True)

        results = {}
        results['class'] = self.className
        results['results'] = {}
        result_files = glob('sqlmap/output/results*')
        if not result_files:
            return results

        with open(result_files[0]) as csvfile:
            reader = DictReader(csvfile)
            idx = 0
            for row in reader:
                uri = urlparse(row['Target URL'])
                domain = uri.netloc
                if uri.port:
                    domain = domain[:domain.rfind(':')]
                logfile = open('sqlmap/output/' + domain + '/log', 'r')
                log = logfile.read()
                logfile.close()
                domain = uri.scheme + '://' + domain
                if row['Place']:
                    entry = {}
                    entry['endpoint'] = uri.path
                    entry['method'] = row['Place']
                    start = log.find(row['Parameter'] + '=', idx) + len(row['Parameter']) + 1
                    end = log.find('\n', start)
                    entry['params'] = {row['Parameter'] : log[start:end].strip()}
                    if domain not in results['results']:
                        results['results'][domain] = [entry]
                    else :
                        results['results'][domain].append(entry)

                    if log.find(row['Parameter'] + '=', end) != -1 and log.find(row['Parameter'] + '=', end) < log.find('---', end):
                        start = log.find(row['Parameter'] + '=', end) + len(row['Parameter']) + 1
                        end = log.find('\n', start)
                        entry_copy = deepcopy(entry)
                        entry_copy['params'] = {row['Parameter'] : log[start:end].strip()}
                        results['results'][domain].append(entry_copy)

                    idx = end

        os.chdir(OLDPWD)
        return results
