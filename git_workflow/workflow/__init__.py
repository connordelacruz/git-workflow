"""The workflow scripts"""
from .branch import Branch
from .commit_template import CommitTemplate

#: Maps command names to WorkflowBase subclasses
commands = {
    Branch.command: Branch,
    CommitTemplate.command: CommitTemplate,
}


def add_command_subparsers(subparsers, generic_parent_parser):
    """Add subparsers for each workflow command.

    :param subparsers: Subparsers object
    :param generic_parent_parser: Instance of argparse.ArgumentParser used
        as a parent for top level parser
    """
    for commandClass in commands.values():
        commandClass.add_subparser(subparsers, generic_parent_parser)


def run_command(repo, parser):
    """Run a workflow command.

    :param repo: Repo object
    :param parser: ArgumentParser object
    """
    parsed_args = parser.parse_args()
    command_class = commands.get(parsed_args.command, False)
    if not command_class:
        # exit_code = 1 # TODO implement? or raise specific exception
        parser.print_help()
    else:
        command = command_class(repo, parser, parsed_args=parsed_args)
        command.run()
