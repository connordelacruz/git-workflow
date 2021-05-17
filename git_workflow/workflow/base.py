"""Base class for workflow scripts."""
from abc import ABC, abstractmethod
from cmd_utils import cmd
from git_workflow.utils.configs import Configs


class WorkflowBase(ABC):

    def __init__(self, repo, parser,
                 parsed_args=None, verbosity=1):
        """Constructor

        :param repo: git.Repo instance for the repository
        :param parser: ArgumentParser instance
        :param parsed_args: (Optional) Parsed args object
        :param verbosity: (Default: 1) Output verbosity level
        """
        self.repo = repo
        self.parser = parser
        self.parsed_args = parsed_args
        self.verbosity = verbosity
        self.configs = Configs(self.repo)

    #: Names of git configs used in this command
    configs_used = []

    @classmethod
    def _add_base_subparser(cls, subparsers, generic_parent_parser):
        """Common setup for initializing subparser.

        :param subparsers: Subparsers object
        :param generic_parent_parser: Instance of argparse.ArgumentParser used
            as a parent for top level parser

        :return: Subparser object
        """
        return subparsers.add_parser(
            cls.command, description=cls.description, help=cls.description,
            parents=[generic_parent_parser], add_help=False
        )

    # Abstract Properties and Methods

    @property
    @abstractmethod
    def command(self):
        """Subcommand name"""
        pass

    @property
    @abstractmethod
    def description(self):
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

    # Helper Methods

    def print(self, *lines, required_verbosity=1, **print_multiline_kwargs):
        """Print a message.

        :param lines: Lines to print
        :param required_verbosity: (Default: 1) Only print if verbosity is greater than
            or equal to this value

        :param **print_multiline_kwargs: Any keyword arguments to pass to
            cmd.print_multiline()
        """
        if self.verbosity >= required_verbosity:
            cmd.print_multiline(*lines, **print_multiline_kwargs)

    def print_error(self, *lines, required_verbosity=1):
        if self.verbosity >= required_verbosity:
            cmd.print_error(*lines)

    def print_warning(self, *lines, required_verbosity=1):
        if self.verbosity >= required_verbosity:
            cmd.print_warning(*lines)

    def print_success(self, *lines, required_verbosity=1):
        if self.verbosity >= required_verbosity:
            cmd.print_success(*lines)

    def print_info(self, *lines, required_verbosity=1):
        if self.verbosity >= required_verbosity:
            cmd.print_info(*lines)
