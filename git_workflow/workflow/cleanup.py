from git_workflow.utils import cmd
from .base import WorkflowBase
from .unset_template import UnsetTemplate

class Cleanup(WorkflowBase):
    """TODO"""

    command = 'cleanup'
    description = 'Tidy up workflow-related files and configs.'
    # TODO configs_used = []

    @classmethod
    def add_subparser(cls, subparsers, generic_parent_parser):
        cleanup_subparser = subparsers.add_parser(
            cls.command, description=cls.description, help=cls.description,
            parents=[generic_parent_parser], add_help=False
        )
        # TODO confirmation, --include-current-branch, --orphans-only

    def run(self):
        pass