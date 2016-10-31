#!/c/python27/pythonw.exe
# encoding: utf-8
'''
cachebreaker -- add version arg to links to js,css in a html file

cachebreaker is a tool that add version code to links of js, css, image etc.

@author:     sunmoonone

@copyright:  2016 personal.com. All rights reserved.

@license:    license

@contact:    ubestim@gmail.com
'''

import sys
import time
import os
import os.path as ospath
import re

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2016-10-29'
__updated__ = '2016-10-29'

reg_link= re.compile('\"(.*(js|css)(\?.*)?)\"')
_ver_=""
_recurse_=False
_encoding_="utf8"
_include_=[]
_exclude_=[]

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg


def parse_file(path,arg=None):
    with open(path,'a+') as f:
        contents = f.read().decode(_encoding_);
        prod=  reg_link.sub(add_ver, contents)
        f.seek(0)
        f.truncate(0)
        f.write(prod.encode(_encoding_))

def add_ver(m):
    global _ver_
    link = m.group(1)
    pos= link.find('?')
    if pos > 0: 
        link = link[:pos]

    hit=0
    if _include_:
        for p in _include_:
            if link.endswith(p):
                hit=1
                break
    elif _exclude_:
        hit=1
        for p in _exclude_:
            if link.endswith(p):
                hit=0
                break
    else:
        hit=1
    
    if hit:
        return '"%s?v=%s"' % (link, _ver_)

    return m.group(0)

def walk(path,visit,arg=None):
    '''Calls the function visit with arguments (arg, dirname, item) for each item in the directory tree rooted at path (including path itself, if it is a directory).
    The argument dirname specifies the visited directory,
    the argument item is the current item in the directory (gotten from os.listdir(dirname)).

    if function visit returns false then `item` will not be visited
    if function visit returns true then walk is aborted
    '''
    print "processing ",path
    for f in os.listdir(path):
        if f.startswith("."):
            continue
        if ospath.isdir(ospath.join(path,f)):
            if _recurse_:
                if walk(ospath.join(path,f), visit, arg)==0:
                    return 0
        elif f.endswith(".html"):
            _ret = visit(ospath.join(path,f), arg)
        
def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by sunmoonone on %s.
  Copyright 2016 sunmoonone. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-v', '--version', action='version', version=program_version_message)
        parser.add_argument("-e", "--encoding",default="utf8", dest="encoding", help="charset encoding of file. Default: utf8")
        parser.add_argument("-r", "--recursive",default=False, action="store_true", dest="recursive", help="parse files recursively")
        parser.add_argument("--include", dest="include", help="file names separate by comma, only parse links specified by this option")
        parser.add_argument("--exclude", dest="exclude", help="file names separate by comma, skip links specified by this option")
        parser.add_argument(dest="dir", help="project directory", metavar="dir")
        parser.add_argument(dest="ver", help="version number. if ver is now then will use timestamp as the value of ver", metavar="ver")

        # Process arguments
        global _ver_,_encoding_,_include_,_exclude_,_recurse_
        args = parser.parse_args()
        
        if args.ver=="now":
            _ver_=str(int(time.time()))
        else:
            _ver_=args.ver
        _encoding_=args.encoding
        _recurse_=args.recursive
        
        if args.include:
            _include_=args.include.split(",")
        if args.exclude:
            _exclude_=args.exclude.split(",")
        
        if not args.dir or not ospath.isdir(args.dir):
            parser.error("dir should be a directory");
            return 1
        
        walk(ospath.abspath(args.dir), parse_file)
        print "done"
                
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, _e:
        raise
#         indent = len(program_name) * " "
#         sys.stderr.write(program_name + ": " + repr(e) + "\n")
#         sys.stderr.write(indent + "  for help use --help")
#         return 2

if __name__ == "__main__":
    sys.exit(main())