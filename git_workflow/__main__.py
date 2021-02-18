import argparse
import os
import sys
from git import Repo
from git.exc import InvalidGitRepositoryError, NoSuchPathError
from git_workflow import utils, workflow
from git_workflow.__about__ import __version__


def get_generic_parent_parser():
    """Returns a generic parent ArgumentParser with --help, --version, and
    --verbose args

    Note: parsers that have this as a parent should be initialized with
    add_help=False. This parser overrides the default help arg so it can be
    nested under the 'General' group in help message output

    :return: ArgumentParser to use as parent
    """
    parser = argparse.ArgumentParser(add_help=False)
    group = parser.add_argument_group('General')
    # Overriding the default -h arg so it can be nested under the 'General'
    # heading in help message. Parsers that have this as a parent should be
    # initialized with add_help=False
    group.add_argument('-h', '--help', action='help',
                       help='Show this help message and exit')
    group.add_argument('-V', '--version', action='version',
                       version='%(prog)s ' + __version__,
                       help='Show version number and exit')
    # TODO: Implement verbose
    # group.add_argument('-v', '--verbose', type=int, choices=range(0,3),
    #                    nargs='?', default=1, const=2,
    #                    help='Set verbosity level')
    return parser

def get_parser():
    """Returns ArgumentParser for main"""
    generic_parent_parser = get_generic_parent_parser()
    parser = argparse.ArgumentParser(parents=[generic_parent_parser],
                                     add_help=False)
    subparsers = parser.add_subparsers(title='Commands',
                                       description=f"Run '{parser.prog} <command> --help' for details",
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
