#!/usr/bin/env python
import getpass
import os
import sys
from jira.client import JIRA
from simplecrypt import decrypt

js = 'https://??.atlassian.net'
if __name__ == '__main__':
    number = int(sys.argv[1])
    t = 'SS-%d' % number
    enp = "sc\x00\x02[\xd3\x1a\x0bOlO\x8bJ\xfb\xa4\xff\xa8{\x02\x88\x81\xaflW\xc7\xc5\xcf(\xed!\xebr\xca\x88\xf0\xd7w \xad\xc1*}?X%\x0f\x96\x98\xc0\x97\xef\x16CH\xea&z\xcd\xdbp\xc0F\x91\xdcN\x8b\xef\x8e\xc2\xda\x0bT\x9d\xf3\x91\xf5\xdb\xc2y*\xdd\xbc\x05.)\x02+\xf5t\x88\xe1#h\x0b\x87Y\xe1\xd3&\xf7M\xa8\xfc|\xe4H\x11\xd3\x9d\xe2%\xfa\xb2O\x95n\x06#\x96J`JjB~M\xd8\x97u\xfb\xba\x83\xcf\xb7\xc3'<\x14N\xf4\x0c\xd4\xfe\xb2lZ\x9a\xb5N\\HP\x7f\xeb\xdd\xdaT"
    pwd = getpass.getpass('password: ')
    u, p = decrypt(open('/Users/kennyzhang/Downloads/__sp1').read().strip(), decrypt(pwd, enp)).split(':')
    j = JIRA(options={'server': js}, basic_auth=(u, p))
    cmd = 'git branch ' + t + '-' + j.issue(t).fields.summary.replace(' ', '-')
    print 'cmd: ', cmd
    if raw_input('Y?').upper() == 'Y':
        print os.popen(cmd).read()
