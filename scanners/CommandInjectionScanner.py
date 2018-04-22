from Scanner import Scanner

class CommandInjectionScanner(Scanner):
    className = 'Command Injection'
    payloads = [';%s', '%%26%s', '%%26%%26%s', '||%s',
            '`%s`', '`%s >/proc/$$/fd/1`']
    testPayload = 'printenv'
    testSignature = 'PATH'
    realPayload = 'uname -a'
