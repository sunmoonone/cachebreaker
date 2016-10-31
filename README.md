给html 页面里的 js，css链接添加版本号的小工具

```
$ ./cachebreaker -h
usage: cachebreaker [-h] [-v] [-e ENCODING] [-r] [--include INCLUDE]
                    [--exclude EXCLUDE]
                    dir ver

cachebreaker -- add version arg to links to js,css in a html file

  Created by sunmoonone on 2016-10-29.
  Copyright 2016 sunmoonone. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE

positional arguments:
  dir                   project directory
  ver                   version number. if ver is now then will use timestamp
                        as the value of ver

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -e ENCODING, --encoding ENCODING
                        charset encoding of file. Default: utf8
  -r, --recursive       parse files recursively
  --include INCLUDE     file names separate by comma, only parse links
                        specified
  --exclude EXCLUDE     file names separate by comma, skip links specified

```