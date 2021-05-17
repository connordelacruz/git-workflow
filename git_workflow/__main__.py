# PYTHON_ARGCOMPLETE_OK
import argcomplete
from git_workflow.utils.parser import get_parser
# Initialize parser before remaining imports for improved tab speed
parser = get_parser()
argcomplete.autocomplete(parser)
import os
import sys
from cmd_utils import cmd
from git import Repo
from git.exc import InvalidGitRepositoryError, NoSuchPathError
from git_workflow.utils import repository
from git_workflow.workflow import run_command


def main():
    # Argument Parser
    parsed_args = parser.parse_args()
    # Check installed git version
    try:
        repository.verify_git_version()
    except Exception as e:
        cmd.print_error(e)
        return
    # Initialize Repo object
    repo = None
    try:
        repo = Repo(os.getcwd(), search_parent_directories=True)
    except InvalidGitRepositoryError as e:
        cmd.print_error('No git repo found: {}'.format(e))
    except NoSuchPathError as e:
        cmd.print_error('Invalid path: {}'.format(e))
    finally:
        if repo is None:
            return
    try:
        run_command(repo, parser, parsed_args=parsed_args)
    except KeyboardInterrupt:
        print('')
        sys.exit(0)
    except Exception as e:
        cmd.print_error(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
