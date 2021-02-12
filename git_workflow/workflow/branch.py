import datetime
import re
from git import Head, Remote
from git_workflow.utils import cmd
from .base import WorkflowBase
from .commit_template import CommitTemplate


class Branch(WorkflowBase):
    """Create a new branch."""
    command = 'branch'
    description = 'Create a new branch.'

    def run(self):
        args = self.get_args()
        branch_name = args['client'] + args['description'] + args['timestamp'] + args['initials']
        # TODO check for bad branch names if configured
        new_branch = self.create_branch(branch_name)
        # If specified, call commit-template
        if args['ticket']:
            self.print('', 'Checking ticket number format...')
            commit_template_parsed_args = self.parser.parse_args([CommitTemplate.command, args['ticket']])
            commit_template = CommitTemplate(self.repo, self.parser, parsed_args=commit_template_parsed_args,
                                             verbosity=self.verbosity)
            commit_template.run()

    @classmethod
    def add_subparser(cls, subparsers, generic_parent_parser):
        branch_subparser = subparsers.add_parser(
            cls.command, description=cls.description, help=cls.description,
            parents=[generic_parent_parser], add_help=False
        )
        # Branch Name
        branch_name_args = branch_subparser.add_argument_group('Branch Name Arguments')
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
        # Commit Template
        commit_template_args = branch_subparser.add_argument_group('Commit Template Arguments')
        ticket_group = commit_template_args.add_mutually_exclusive_group()
        ticket_group.add_argument(
            '-t', '--ticket', metavar='<ticket#>', help='Specify ticket number (will create commit template)'
        )
        ticket_group.add_argument(
            '-T', '--no-ticket', help="Skip ticket number prompt, don't create commit template (overrides -t)",
            action='store_true', default=False
        ) # https://youtu.be/iHSPf6x1Fdo
        # TODO --timestamp, other args

    def get_args(self):
        """Parse command line arguments and prompt for any missing values.

        :return: A dictionary with the following keys:
            client, description, initials, timestamp
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

        # TODO  or config.initials, print info if configured
        initials = cmd.prompt(
            'Initials',
            'Enter your initials.',
            invalid_msg='Must enter initials.',
            initial_input=self.parsed_args.initials,
            format_function=self.format_branch_name,
        )
        args['initials'] = initials

        # TODO use CommitTemplate validate method (only if the input isn't empty)
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

        return args

    def format_branch_name(self, val):
        """Convert text to lowercase and replace spaces and underscores with
        hyphens.

        :param val: Text to format

        :return: Formatted text
        """
        return re.sub('[ _]+', '-', val.lower())

    # TODO use configs and update default docs
    def create_branch(self, branch_name, base_branch='master',
                      update_base_branch=True):
        """Create a new branch.

        :param branch_name: The name of the new branch to create
        :param base_branch: (Default: 'master') New branch will be based off
            this branch
        :param update_base_branch: (Default: True) If true, attempt to pull
            changes to base_branch before branching

        :return: New branch name
        """
        # Checkout base_branch
        base = Head(self.repo, 'refs/heads/' + base_branch)
        if self.repo.active_branch != base:
            base.checkout()
        # Update
        if update_base_branch and base.tracking_branch():
            self.print('Pulling updates to {}...'.format(base_branch))
            remote_name = base.tracking_branch().remote_name
            remote = Remote(self.repo, remote_name)
            base_commit = base.commit
            for fetch_info in remote.pull():
                if fetch_info.ref == base.tracking_branch():
                    if fetch_info.commit != base_commit:
                        self.print('Updated {} to {}'.format(base_branch, fetch_info.commit.hexsha))
                    else:
                        self.print('{} already up to date.'.format(base_branch))
            self.print('')
        # Checkout new branch
        self.print('Creating new branch {}...'.format(branch_name))
        # TODO try/except:
        new_active_branch = base.checkout(b=branch_name)
        if new_active_branch.name == branch_name:
            self.print('Branch created.', formatting=cmd.SUCCESS)
        else:
            pass # TODO should we get here if we wrap the above in try/except?
        return new_active_branch

