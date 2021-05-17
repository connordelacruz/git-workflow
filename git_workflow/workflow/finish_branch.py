from git import GitCommandError
from cmd_utils import cmd
from git_workflow.utils.repository import checkout_branch
from .base import WorkflowBase
from .unset_template import UnsetTemplate


class FinishBranch(WorkflowBase):
    """\
    Finish a project branch.

    By default, this command will prompt for confirmation unless ``--force`` is
    specified. Once confirmed, this command will:

    - Unset the commit template of the project branch
    - Checkout the base branch and pull latest updates
    - Attempt to delete the project branch using ``git branch -d``, which may
      fail if the project branch has not been fully merged
    """

    command = 'finish'
    description = 'Finish a project branch.'
    configs_used = ['baseBranch', 'finishBranchConfirmationPrompt']

    @classmethod
    def add_subparser(cls, subparsers, generic_parent_parser):
        finish_subparser = cls._add_base_subparser(subparsers, generic_parent_parser)
        # TODO: no_pull? -D?
        # Specify branch
        positional_args = finish_subparser.add_argument_group(
            'Positional Arguments'
        )
        positional_args.add_argument(
            'branch', metavar='<branch>', nargs='?',
            help='Branch to finish (default: current)',
            default=None
        )
        # Confirmation prompt
        confirmation_args = finish_subparser.add_argument_group(
            'Confirmation Prompt Arguments',
            'Override workflow.finishBranchConfirmationPrompt config.'
        )
        confirmation_group = confirmation_args.add_mutually_exclusive_group()
        confirmation_group.add_argument(
            '-f', '--force', help='Skip confirmation prompt (if configured)',
            dest='confirm', action='store_false', default=None
        )
        confirmation_group.add_argument(
            '-c', '--confirmation', help='Prompt for confirmation before deleting',
            dest='confirm', action='store_true', default=None
        )

    def get_args(self):
        args = {}
        args['branch'] = (self.parsed_args.branch
                          if self.parsed_args.branch is not None else
                          self.repo.active_branch.name)
        # Default to config value unless otherwise specified
        args['confirm'] = (self.configs.FINISH_BRANCH_CONFIRMATION_PROMPT
                           if self.parsed_args.confirm is None else
                           self.parsed_args.confirm)
        return args

    def run(self):
        args = self.get_args()
        branch = args['branch']
        # Confirmation prompt
        if args['confirm']:
            confirmation = cmd.prompt(
                'Delete Branch? (y/n)',
                f'Delete branch {branch}?',
                default_val='n', validate_function=cmd.validate_yn
            )
            if not confirmation:
                return
        # Unset template
        unset_template_parsed_args = self.parser.parse_args([UnsetTemplate.command, branch, '--force'])
        unset_template = UnsetTemplate(self.repo, self.parser,
                                       parsed_args=unset_template_parsed_args,
                                       verbosity=self.verbosity)
        unset_template.run()
        # Checkout base_branch
        base_branch = self.configs.BASE_BRANCH
        base_head = checkout_branch(self.repo, base_branch)
        # Finish branch
        self.print(f'Attempting to delete {branch}...')
        try:
            self.repo.git.branch('-d', branch)
            self.print_success('Deletion successful.')
        except GitCommandError:
            self.print_warning(f'Unable to delete {branch}. You will need to delete it manually.')
