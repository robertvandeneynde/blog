#!/usr/bin/env python3

import subprocess
import textwrap
import os
import os.path
import re

class OutFile:
    def __init__(self, filename, supargs=''):
        self.filename = filename
        self.supargs = supargs
    
    def __enter__(self):
        if os.path.isfile(self.filename):
            os.chmod(self.filename, 0o644)
        self.f = open(self.filename, 'w' + self.supargs if 'w' not in self.supargs else self.supargs)
        return self.f
    
    def __exit__(self, type, value, traceback):
        os.chmod(self.filename, 0o444)
        self.f.__exit__(type, value, traceback)

def by_markdown(string):
    to_md = textwrap.dedent(string)
    p = subprocess.Popen('/home/robert/nonpython/markdown.pl', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    p.stdin.write(to_md.encode('utf-8'))
    p.stdin.close()
    return p.stdout.read().decode('utf-8')

FR = re.compile(r'(.*)\.md\.html')
RE = re.compile(r'\{\% markdown \%}(.*?)\{\% endmarkdown \%\}', re.DOTALL)

for filename in os.listdir('.'):
    if FR.match(filename):
        try:
            with open(filename) as f:
                content = f.read()
                
            with OutFile("{}.html".format(FR.match(filename).group(1))) as out:
                out.write(RE.sub(lambda m:by_markdown(m.group(1)), content))
        except Exception as e:
            print("Error in {}: {}".format(filename, e))

