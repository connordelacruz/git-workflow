import os
from git import Repo
from git.exc import InvalidGitRepositoryError, NoSuchPathError

from git_workflow import utils, workflow


def main():
    # Initialize Repo object
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
    # Is the minimum git version met for advanced features?
    min_git_version_met = utils.repo.verify_git_version()
    # TODO Subcommand argument parsing
    command = workflow.Branch(repo, min_git_version_met)
    command.run()


if __name__ == '__main__':
    main()
