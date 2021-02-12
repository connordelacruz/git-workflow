import argparse
import os
import sys
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
    # Check installed git version
    # TODO allow limited functionality for lower git versions in future update?
    try:
        min_git_version_met = utils.repository.verify_git_version()
    except Exception as e:
        utils.cmd.print_error(e)
        return
    # Initialize Repo object
    repo = None
    try:
        repo = Repo(os.getcwd(), search_parent_directories=True)
    except InvalidGitRepositoryError as e:
        utils.cmd.print_error('No git repo found: {}'.format(e))
    except NoSuchPathError as e:
        utils.cmd.print_error('Invalid path: {}'.format(e))
    finally:
        if repo is None:
            return
    # Argument Parser
    parser = get_parser()
    # TODO exit code and try/except
    try:
        exit_code = workflow.run_command(repo, parser)
    except KeyboardInterrupt:
        print('')
        sys.exit(0)


if __name__ == '__main__':
    main()
