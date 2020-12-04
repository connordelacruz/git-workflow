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
    subparsers = parser.add_subparsers(title='Commands',
                                       description="Run '{} <command> --help' for details".format(parser.prog),
                                       dest='command', metavar='<command>')
    workflow.add_command_subparsers(subparsers, generic_parent_parser)
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
    # TODO exit code and try/except
    exit_code = workflow.run_command(repo, min_git_version_met, parser)


if __name__ == '__main__':
    main()
