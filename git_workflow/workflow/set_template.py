import os
from cmd_utils import cmd
from git_workflow.utils import files
from .base import WorkflowBase


class SetTemplate(WorkflowBase):
    """\
    Create and configure commit template for the current branch.

    By default, the commit template includes the specified ticket number before
    the commit message. E.g. for ticket number ``AB-12345``:

    ::

        [AB-12345] <commit message text starts here>

    The commit template file will be created in the root of the git repository.
    By default, the filename will be in this format:

    ::

        .gitmessage_local_<ticket>_<branch>

    The format of the filename, commit template body, accepted ticket numbers,
    and more can be customized with git configs (see the Configs section below
    for details).
    """
    command = 'set-template'
    description = 'Configure git commit template for a branch.'
    configs_used = [
        'commitTemplateFilenameFormat',
        'commitTemplateFormat',
        'ticketInputFormatRegex',
        'ticketFormatCapitalize',
        'ticketInputFormatRegex',
        'initials',
    ]

    @classmethod
    def add_subparser(cls, subparsers, generic_parent_parser):
        commit_template_subparser = cls._add_base_subparser(subparsers, generic_parent_parser)
        positional_args = commit_template_subparser.add_argument_group(
            'Positional Arguments'
        )
        positional_args.add_argument(
            'ticket', metavar='<ticket>', nargs='?', help='Ticket number to use in commit template',
            default=None
        )

    def get_args(self):
        """Parse command line arguments and prompt for any missing values.

        :return: A dictionary with the following keys:
            ticket
        """
        args = {}

        validate_ticket_number = cmd.generate_validate_regex_function(
            self.configs.TICKET_INPUT_FORMAT_REGEX
        )
        ticket = cmd.prompt(
            'Ticket Number',
            'Enter ticket number to use in commit messages.',
            invalid_msg='Invalid ticket number formatting.',
            initial_input=self.parsed_args.ticket,
            validate_function=validate_ticket_number,
            format_function=self.format_ticket_number,
        )
        args['ticket'] = ticket

        return args

    def run(self):
        args = self.get_args()
        repo_root_dir = os.path.dirname(self.repo.git_dir)
        branch_name = self.repo.active_branch.name
        # Create commit template
        format_kwargs = self.get_format_kwargs(args, branch_name)
        # NOTE: filenames will always begin with '.gitmessage_local_'
        commit_template_file = files.sanitize_filename(
            '.gitmessage_local_' + self.configs.COMMIT_TEMPLATE_FILENAME_FORMAT.format(**format_kwargs)
        )
        commit_template_path = os.path.join(repo_root_dir, commit_template_file)
        self.print('Creating commit template file...')
        commit_template_body = self.configs.COMMIT_TEMPLATE_FORMAT.format(**format_kwargs)
        with open(commit_template_path, 'w') as f:
            f.write(commit_template_body)
        if not os.path.exists(commit_template_path):
            raise Exception('Unable to create commit template at path ' + commit_template_path)
        self.print_success('Template file created.', commit_template_path, '')
        # Configure commit template
        # TODO REPHRASE OUTPUT. Current output would be fine for --verbose but is too much otherwise
        branch_config_file = files.sanitize_filename(f'config_{branch_name}')
        branch_config_path = os.path.join(self.repo.git_dir, branch_config_file)
        # Branch config
        self.print(f'Configuring commit.template for branch {branch_name}...')
        self.repo.git.config('commit.template', commit_template_file,
                             file=branch_config_path)
        self.print_success(f'commit.template configured in .git/{branch_config_file}.', '')
        # Add includeIf for branch config to local config
        self.print('Configuring local repo...')
        self.repo.git.config(f'includeIf.onbranch:{branch_name}.path', branch_config_file,
                             file=self.configs.CONFIG_PATH)
        self.print_success('Local repo configured.',
                           f'Will include branch config .git/{branch_config_file}',
                           f'when branch {branch_name} is checked out.',
                           '')

    # Helper Methods

    def format_ticket_number(self, val):
        """Format ticket number input based on configs.

        :param val: Text to format

        :return: formatted text
        """
        if self.configs.TICKET_FORMAT_CAPITALIZE:
            val = val.upper()
        return val

    def get_format_kwargs(self, args, branch_name):
        """Returns a dict mapping placeholders to their respective values.

        :param args: get_args() result
        :param branch_name: Name of the branch to create template for

        :return: Dictionary to pass as kwargs to .format()
        """
        format_kwargs = {
            'ticket': args['ticket'],
            'branch': branch_name,
            'initials': self.configs.INITIALS or '',
        }
        return format_kwargs
