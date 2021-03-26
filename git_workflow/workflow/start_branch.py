import datetime
import re
from git import Head, Remote
from git_workflow.utils import cmd
from .base import WorkflowBase
from .set_template import SetTemplate


class StartBranch(WorkflowBase):
    """\
    Create a new branch with the following name format:

    ::

        [<client>-]<brief-description>-<yyyymmdd>-<initials>

    Where:

    - ``<client>`` - (Optional) Client's name
    - ``<brief-description>`` - Description of the work
    - ``<yyyymmdd>`` - Today's date
    - ``<initials>`` - Engineer's initials

    Script will prompt for details and format appropriately (i.e. no
    spaces/underscores, all lowercase).
    """

    command = 'start'
    description = 'Create a new branch.'
    configs_used = ['initials', 'baseBranch', 'badBranchNamePatterns']

    @classmethod
    def add_subparser(cls, subparsers, generic_parent_parser):
        branch_subparser = subparsers.add_parser(
            cls.command, description=cls.description, help=cls.description,
            parents=[generic_parent_parser], add_help=False
        )
        # Branch Name
        branch_name_args = branch_subparser.add_argument_group(
            'Branch Name Arguments'
        )
        client_group = branch_name_args.add_mutually_exclusive_group()
        client_group.add_argument(
            '-c', '--client', metavar='<client>', help='Specify client name'
        )
        client_group.add_argument(
            '-C', '--no-client', help='No client name (skips prompt)',
            action='store_true', default=False
        )
        branch_name_args.add_argument(
            '-d', '--description', metavar='<description>', help='Specify branch description'
        )
        branch_name_args.add_argument(
            '-i', '--initials', metavar='<initials>', help='Specify developer initials'
        )
        branch_name_args.add_argument(
            '-s', '--skip-bad-name-check', help='Skip check for bad branch names',
            action='store_true', default=False
        )
        # Commit Template
        commit_template_args = branch_subparser.add_argument_group(
            'Commit Template Arguments'
        )
        ticket_group = commit_template_args.add_mutually_exclusive_group()
        ticket_group.add_argument(
            '-t', '--ticket', metavar='<ticket#>', help='Specify ticket number (will create commit template)'
        )
        ticket_group.add_argument(
            '-T', '--no-ticket', help="Skip ticket number prompt, don't create commit template (overrides -t)",
            action='store_true', default=False
        ) # https://youtu.be/iHSPf6x1Fdo
        # Branching
        branching_args = branch_subparser.add_argument_group(
            'Branching Arguments'
        )
        base_branch_group = branching_args.add_mutually_exclusive_group()
        base_branch_group.add_argument(
            '-b', '--base-branch', metavar='<branch>', help='Specify branch to use as base for new branch (default: master)'
        )
        base_branch_group.add_argument(
            '-B', '--branch-from-current', help='Use currently checked out branch as base (overrides -b)',
            action='store_true', default=False
        )
        base_branch_group.add_argument(
            '-P', '--no-pull', help='Skip pulling changes to base branch.',
            action='store_true', default=False
        )

    def get_args(self):
        """Parse command line arguments and prompt for any missing values.

        :return: A dictionary with the following keys:
            client, description, initials, ticket, timestamp, base_branch,
            skip_bad_name_check
        """
        args = {}
        client = None
        if not self.parsed_args.no_client:
            client = cmd.prompt(
                'Client',
                '(Optional) Enter the name of the affected client.',
                initial_input=self.parsed_args.client,
                validate_function=cmd.validate_optional_prompt,
                format_function=self.format_branch_name,
            )
        # Append hyphen if client is not empty
        if client:
            client += '-'
        else:
            client = ''
        args['client'] = client

        description = cmd.prompt(
            'Description',
            'Enter a brief description for the branch.',
            invalid_msg='Description must not be blank.',
            initial_input=self.parsed_args.description,
            format_function=self.format_branch_name,
        )
        description += '-'
        args['description'] = description

        initials = cmd.prompt(
            'Initials',
            'Enter your initials.',
            invalid_msg='Must enter initials.',
            initial_input=self.parsed_args.initials or self.configs.INITIALS,
            format_function=self.format_branch_name,
        )
        args['initials'] = initials

        ticket = None
        if not self.parsed_args.no_ticket:
            ticket = cmd.prompt(
                'Ticket Number',
                '(Optional) Enter ticket number to use in commit messages.',
                "Leave blank if you don't want to use a commit template.",
                initial_input=self.parsed_args.ticket,
                validate_function=cmd.validate_optional_prompt,
            )
        args['ticket'] = ticket

        timestamp = datetime.datetime.now().strftime('%Y%m%d-')
        args['timestamp'] = timestamp

        base_branch = self.parsed_args.base_branch or self.configs.BASE_BRANCH
        if self.parsed_args.branch_from_current:
            base_branch = self.repo.active_branch.name
        args['base_branch'] = base_branch

        args['no_pull'] = self.parsed_args.no_pull

        args['skip_bad_name_check'] = self.parsed_args.skip_bad_name_check

        return args

    def run(self):
        args = self.get_args()
        branch_name = args['client'] + args['description'] + args['timestamp'] + args['initials']
        if self.configs.BAD_BRANCH_NAME_PATTERNS:
            if args['skip_bad_name_check']:
                self.print_warning('workflow.badBranchNamePatterns is configured, but -s argument was specified.',
                                   'Skipping bad branch name check.')
            else:
                # Will raise exception if name doesn't check out
                self.check_branch_name(branch_name)
        # Checkout base_branch
        base_branch = args['base_branch']
        # TODO support tags with 'refs/tags/'; maybe --release/-r arg
        base_head = Head(self.repo, f'refs/heads/{base_branch}')
        if self.repo.active_branch != base_head:
            base_head.checkout()
        # Update
        if not args['no_pull'] and base_head.tracking_branch():
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
        # Checkout new branch
        self.print(f'Creating new branch {branch_name}...')
        new_active_branch = base_head.checkout(b=branch_name)
        if new_active_branch.name == branch_name:
            self.print_success('Branch created.', '')
        else:
            pass # TODO should we get here? checkout() should raise exception
        # If specified, call commit-template
        if args['ticket']:
            self.print('Checking ticket number format...')
            set_template_parsed_args = self.parser.parse_args([SetTemplate.command, args['ticket']])
            set_template = SetTemplate(self.repo, self.parser,
                                       parsed_args=set_template_parsed_args,
                                       verbosity=self.verbosity)
            set_template.run()

    # Helper Methods

    def format_branch_name(self, val):
        """Convert text to lowercase and replace spaces and underscores with
        hyphens.

        :param val: Text to format

        :return: Formatted text
        """
        return re.sub('[ _]+', '-', val.lower())

    def check_branch_name(self, branch_name):
        """Checks for configured bad patterns in branch name. Raises exception
        if one is found.

        :param branch_name: Name to check
        """
        for bad_pattern in self.configs.BAD_BRANCH_NAME_PATTERNS:
            if bad_pattern in branch_name:
                error_msg = '\n'.join([
                    f'Branch name "{branch_name}" contains invalid pattern "{bad_pattern}".',
                    '',
                    'Branch names should not include the following patterns:',
                    *[cmd.INDENT + pattern for pattern in self.configs.BAD_BRANCH_NAME_PATTERNS],
                    '',
                    '(from git config workflow.badBranchNamePatterns)',
                    '',
                    'To skip this check, use --skip-bad-name-check argument.'
                ])
                raise Exception(error_msg)
