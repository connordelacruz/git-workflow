"""Base class for workflow scripts."""
from abc import ABC, abstractmethod

from git_workflow.utils import cmd


class WorkflowBase(ABC):

    def __init__(self, repo, min_git_version_met, verbosity=1):
        self.repo = repo
        self.min_git_version_met = min_git_version_met
        self.verbosity = verbosity

    def print(self, *lines, required_verbosity=1, formatting=None):
        """Print a message.

        :param *lines: Lines to print
        :param required_verbosity: (Default: 1) Only print if verbosity is greater than
            or equal to this value
        :param fmt: (Optional) Set to a formatting constant from utils.cmd to
            format output
        """
        if self.verbosity >= required_verbosity:
            cmd.print_multiline(*lines, formatting=formatting)

    @abstractmethod
    def run(self):
        pass
