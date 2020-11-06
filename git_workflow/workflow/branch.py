import datetime
import re

from git import Head, Remote

from git_workflow.utils import cmd
from .base import WorkflowBase

class Branch(WorkflowBase):
    """Create a new branch."""

    def format_branch_name(self, val):
        """Convert text to lowercase and replace spaces and underscores with
        hyphens.

        :param val: Text to format

        :return: Formatted text
        """
        return re.sub('[ _]+', '-', val.lower())

    # TODO use configs and update default docs
    # TODO self.print output
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
            remote_name = base.tracking_branch().remote_name
            remote = Remote(self.repo, remote_name)
            fetch_info = remote.pull()
        # Checkout new branch
        return base.checkout(b=branch_name)

    def get_args(self):
        """Parse command line arguments and prompt for any missing values.

        :return: A dicionary with the following keys:
            client, description, initials, timestamp
        """
        args = {}
        client = None
        if not self.args.no_client:
            client = cmd.prompt(
                'Client',
                '(Optional) Enter the name of the affected client.',
                initial_input=self.args.client,
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
            initial_input=self.args.description,
            format_function=self.format_branch_name,
        )
        description += '-'
        args['description'] = description

        # TODO  or config.initials, print info if configured
        initials = cmd.prompt(
            'Initials',
            'Enter your initials.',
            invalid_msg='Must enter initials.',
            initial_input=self.args.initials,
            format_function=self.format_branch_name,
        )
        args['initials'] = initials

        # TODO TICKET #

        # TODO allow arg override
        timestamp = datetime.datetime.now().strftime('%Y%m%d-')
        args['timestamp'] = timestamp

        return args

    @classmethod
    def add_subparser(cls, subparsers, generic_parent_parser):
        branch_description = 'Create a new branch.'
        branch_subparser = subparsers.add_parser(
            'branch', description=branch_description, help=branch_description,
            parents=[generic_parent_parser], add_help=False
        )
        # Branch Name
        branch_name_args = branch_subparser.add_argument_group('Branch Name Arguments')
        client_group = branch_name_args.add_mutually_exclusive_group()
        client_group.add_argument(
            '--client', '-c', metavar='<client>', help='Specify client name'
        )
        client_group.add_argument(
            '--no-client', '-C', help='No client name (skips prompt)',
            action='store_true', default=False
        )
        branch_name_args.add_argument(
            '--description', '-d', metavar='<description>', help='Specify branch description'
        )
        # TODO --timestamp
        branch_name_args.add_argument(
            '--initials', '-i', metavar='<initials>', help='Specify developer initials'
        )


    def run(self):
        args = self.get_args()
        branch_name = args['client'] + args['description'] + args['timestamp'] + args['initials']
        # TODO check for bad branch names if configured
        # TODO pass configs and args:
        # TODO print output based on verbosity
        # TODO error handling
        new_branch = self.create_branch(branch_name)

