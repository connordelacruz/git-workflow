"""The workflow scripts"""
from .start_branch import StartBranch
from .set_template import SetTemplate
from .unset_template import UnsetTemplate
from .finish_branch import FinishBranch
from .cleanup import Cleanup

#: Maps command names to WorkflowBase subclasses
commands = {
    StartBranch.command: StartBranch,
    FinishBranch.command: FinishBranch,
    SetTemplate.command: SetTemplate,
    UnsetTemplate.command: UnsetTemplate,
    Cleanup.command: Cleanup,
}


def add_command_subparsers(subparsers, generic_parent_parser):
    """Add subparsers for each workflow command.

    :param subparsers: Subparsers object
    :param generic_parent_parser: Instance of argparse.ArgumentParser used
        as a parent for top level parser
    """
    for commandClass in commands.values():
        commandClass.add_subparser(subparsers, generic_parent_parser)


def run_command(repo, parser, parsed_args=None):
    """Run a workflow command.

    :param repo: Repo object
    :param parser: ArgumentParser object
    :param parsed_args: (Optional) Result of parser.parse_args() if already
        called
    """
    if parsed_args is None:
        parsed_args = parser.parse_args()
    command_class = commands.get(parsed_args.command, False)
    if not command_class:
        # exit_code = 1 # TODO implement? or raise specific exception
        parser.print_help()
    else:
        command = command_class(repo, parser, parsed_args=parsed_args)
        command.run()
