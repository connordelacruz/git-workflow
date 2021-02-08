"""Base class for workflow scripts."""
from abc import ABC, abstractmethod
from git_workflow.utils import cmd
from git_workflow.utils.config import Configs


class WorkflowBase(ABC):

    # TODO let self.parsed_args be None if not invoked from command line
    # TODO self.args_inputs; populated by a method based on if parsed_args is set or not; optional args_inputs param
    def __init__(self, repo, min_git_version_met, parsed_args, verbosity=1):
        """Constructor

        :param repo: git.Repo instance for the repository
        :param min_git_version_met: True if installed version of git meets
            minimum requirement for advanced features
        :param parsed_args: Parsed args
        :param verbosity: (Default: 1) Output verbosity level
        """
        self.repo = repo
        self.min_git_version_met = min_git_version_met
        self.parsed_args = parsed_args
        self.verbosity = verbosity
        self.configs = Configs(self.repo)

    def print(self, *lines, required_verbosity=1, formatting=None):
        """Print a message.

        :param lines: Lines to print
        :param required_verbosity: (Default: 1) Only print if verbosity is greater than
            or equal to this value
        :param formatting: (Optional) Set to a formatting constant from utils.cmd to
            format output
        """
        if self.verbosity >= required_verbosity:
            cmd.print_multiline(*lines, formatting=formatting)

    @property
    @abstractmethod
    def command():
        """Subcommand name"""
        pass

    @property
    @abstractmethod
    def description():
        """Subcommand description"""
        pass

    @classmethod
    @abstractmethod
    def add_subparser(cls, subparsers, generic_parent_parser):
        """Add subparser for this command to an argument parser

        :param subparsers: Subparsers object
        :param generic_parent_parser: Instance of argparse.ArgumentParser used
            as a parent for top level parser
        """
        pass

    @abstractmethod
    def run(self):
        """Execute the script"""
        pass
