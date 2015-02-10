from constants import REPOS_BASE_PATH
import os

for root, dirnames, filenames in os.walk(REPOS_BASE_PATH):
    for filename in filenames:
        path = os.path.join(root, filename)
        if 'vimrc' not in filename or os.path.islink(path):
            print "Deleting %s" % path
            os.remove(path)
