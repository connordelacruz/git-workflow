"""The workflow scripts"""
from .branch import Branch

#: Maps command names to WorkflowBase subclasses
commands = {
    Branch.command: Branch,
}

def run_command(repo, min_git_version_met, parser):
    """Run a workflow command

    :param repo: Repo object
    :param min_git_version_met: True if installed git version meets
        requirements for advanced features
    :param parser: ArgumentParser object

    :return: Exit code from command execution
    """
    exit_code = 0
    args = parser.parse_args()
    command_class = commands.get(args.command, False)
    if not command_class:
        exit_code = 1
        parser.print_help()
    else:
        command = command_class(repo, min_git_version_met, args)
        command.run() # TODO return exit_code? Or just raise exception?
    return exit_code

