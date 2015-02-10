from github3 import GitHub
from git import Repo
from constants import REPOS_BASE_PATH
import os


gh = GitHub()
search_results = gh.search_repositories("dotfiles")

import itertools
for r in search_results:

    repo_path = REPOS_BASE_PATH + r.repository.full_name
    git_url = r.repository.clone_url
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)
        Repo.clone_from(git_url, repo_path)
        print "Cloning into %s" % repo_path

    else:
        print "Already have %s" % repo_path
