#!D:\coding\python\django\kk-env\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'compile==1.0.3','console_scripts','compile'
__requires__ = 'compile==1.0.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('compile==1.0.3', 'console_scripts', 'compile')()
    )
