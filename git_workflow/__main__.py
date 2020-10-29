import os
from git import Repo
from git.exc import InvalidGitRepositoryError, NoSuchPathError

from . import utils


def main():
    repo = None
    try:
        repo = Repo(os.getcwd(), search_parent_directories=True)
    except InvalidGitRepositoryError as e:
        print('No git repo found: {}'.format(e))
    except NoSuchPathError as e:
        print('Invalid path: {}'.format(e))
    finally:
        if repo is None:
            return

    min_git_version_met = utils.repo.verify_git_version()
    # TODO DEBUGGING
    print(repo)
    print(min_git_version_met)

if __name__ == '__main__':
    main()
