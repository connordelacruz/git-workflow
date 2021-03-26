from git import Head, Remote, GitCommandError
from git_workflow.utils import cmd
from .base import WorkflowBase
from .unset_template import UnsetTemplate


class FinishBranch(WorkflowBase):
    # TODO DOC

    command = 'finish'
    description = 'Finish a project branch.'
    # TODO configs?

    @classmethod
    def add_subparser(cls, subparsers, generic_parent_parser):
        finish_subparser = subparsers.add_parser(
            cls.command, description=cls.description, help=cls.description,
            parents=[generic_parent_parser], add_help=False
        )
        # TODO: branch, force/confirmation, no_pull? -D?
        # Specify branch
        positional_args = finish_subparser.add_argument_group(
            'Positional Arguments'
        )
        positional_args.add_argument(
            'branch', metavar='<branch>', nargs='?',
            help='Branch to finish (default: current)',
            default=None
        )

    def get_args(self):
        args = {}
        args['branch'] = (self.parsed_args.branch
                          if self.parsed_args.branch is not None else
                          self.repo.active_branch.name)
        # TODO use args/configs
        args['confirm'] = True
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
        # TODO extract this and StartBranch common code to utils?
        # Checkout base_branch
        base_branch = self.configs.BASE_BRANCH
        base_head = Head(self.repo, f'refs/heads/{base_branch}')
        if self.repo.active_branch != base_head:
            self.print(f'Switching to {base_branch}...')
            base_head.checkout()
        # Update
        if base_head.tracking_branch():
            self.print(f'Pulling updates to {base_branch}...')
            remote_name = base_head.tracking_branch().remote_name
            remote = Remote(self.repo, remote_name)
            base_commit = base_head.commit
            for fetch_info in remote.pull():
                if fetch_info.ref == base_head.tracking_branch():
                    if fetch_info.commit != base_commit:
                        self.print(f'Updated {base_branch} to {fetch_info.commit.hexsha}')
                    else:
                        self.print(f'{base_branch} already up to date.')
            self.print('')
        # Finish branch
        self.print(f'Attempting to delete {branch}...')
        try:
            self.repo.git.branch('-d', branch)
            self.print_success('Deletion successful.')
        except GitCommandError:
            self.print_warning(f'Unable to delete {branch}. You will need to delete it manually.')
