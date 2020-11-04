import argparse
import os

from git import Repo
from git.exc import InvalidGitRepositoryError, NoSuchPathError

from git_workflow import utils, workflow

def get_parser():
    """Returns ArgumentParser for main"""
    generic_parent_parser = utils.argparse.get_generic_parent_parser()
    parser = argparse.ArgumentParser(parents=[generic_parent_parser],
                                     add_help=False)
    # TODO Add subparsers for each workflow command
    return parser


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

    # Argument Parser
    parser = get_parser()
    args = parser.parse_args()

    # TODO Subcommand argument parsing
    command = workflow.Branch(repo, min_git_version_met)
    command.run()


if __name__ == '__main__':
    main()
