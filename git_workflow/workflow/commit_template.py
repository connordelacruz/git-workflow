import os
from git_workflow.utils import cmd, files
from .base import WorkflowBase


class CommitTemplate(WorkflowBase):
    """Create and configure commit template."""
    # TODO shorter command? maybe sub-sub commands (template set and template unset)
    command = 'commit-template'
    description = 'Configure git commit template for a branch.'

    def run(self):
        args = self.get_args()
        repo_root_dir = os.path.dirname(self.repo.git_dir)
        branch_name = self.repo.active_branch.name
        # Create and configure the commit template
        commit_template_file = self.create_template(args, repo_root_dir, branch_name)
        self.configure_template(branch_name, commit_template_file)

    @classmethod
    def add_subparser(cls, subparsers, generic_parent_parser):
        commit_template_subparser = subparsers.add_parser(
            cls.command, description=cls.description, help=cls.description,
            parents=[generic_parent_parser], add_help=False
        )
        commit_template_subparser.add_argument(
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

    def create_template(self, args, repo_root_dir, branch_name):
        """Create git commit template file.

        :param args: get_args() result
        :param repo_root_dir: Root directory of git repo
        :param branch_name: Name of the branch to create template for

        :return: Filename of the created template file
        """
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
        self.print_success('Template file created.', commit_template_path)
        return commit_template_file

    def configure_template(self, branch_name, commit_template_file):
        """Configure commit.template in branch's config file, then configure
        local repo to include branch's config file when that branch is checked
        out.

        :param branch_name: Name of the branch
        :param commit_template_file: Commit template filename
        """
        # TODO REPHRASE OUTPUT. Current output would be fine for --verbose but is too much otherwise
        branch_config_file = files.sanitize_filename(f'config_{branch_name}')
        branch_config_path = os.path.join(self.repo.git_dir, branch_config_file)
        # Branch config
        self.print(f'Configuring commit.template for branch {branch_name}...')
        self.repo.git.config('commit.template',
                             commit_template_file, file=branch_config_path)
        self.print_success(f'commit.template configured in .git/{branch_config_file}.')
        # Add includeIf for branch config to local config
        self.print('Configuring local repo...')
        self.repo.git.config(f'includeIf.onbranch:{branch_name}.path',
                             branch_config_file, file=self.configs.CONFIG_PATH)
        self.print_success('Local repo configured.',
                           f'Will include branch config .git/{branch_config_file}',
                           f'when branch {branch_name} is checked out.')

