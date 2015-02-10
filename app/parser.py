from constants import REPOS_BASE_PATH
import os
import redis
import re

store = redis.StrictRedis(host='localhost', port=6379, db=0)
store.delete('lines')

vimrc_paths = []
for root, dirnames, filenames in os.walk(REPOS_BASE_PATH):
    for filename in filenames:
        path = os.path.join(root, filename)
        vimrc_paths.append(path)


def norm(line):
    '''
    Redact non-lines and convert lines into their canonical form

    Very hacky solution, probably not feasible

    Eventually, it would be nice to use a linter to remove lines that are part of a multiline command

    It would also be nice to expand shortcuts to their canonical version
    '''

    # Strip comments
    line = re.sub(r'^\s*".*$', '', line)
    line = re.sub(r'^(Plugin|Plug|Vundle|Bundle|NeoBundle)', 'Plugin', line)

    # Strip whitespace
    line = line.strip()

    blacklist = [
        'else',
        'endif',
        'endfunction',
        '\}',
        '\ }',
        '\  }',
        '\   }',
        '\    }',
        'augroup END',
        'endfor',
        'return',
        "\ 'autoload' : {",
        '\]',
        '\ endif',
        'call smartinput#define_rule({',
        'aug end',
        'end',
        '\ ]',
    ]
    if line in blacklist:
        line = ''

    return line

vimrc_lines = {}
for vimrc_path in vimrc_paths:
    with open(vimrc_path, 'r') as vimrc:
        for line in vimrc:
            line = norm(line)
            if len(line):
                store.zincrby('lines', line)

for line, score in store.zrange('lines', 0, 1500, desc=True, withscores=True):
    print line
    #print "%s: %s" % (score, line)
