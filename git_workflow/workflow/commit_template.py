import os
from git_workflow.utils import cmd, files
from git_workflow.utils.config import Configs
from .base import WorkflowBase


class CommitTemplate(WorkflowBase):
    """Create and configure commit template."""
    # TODO shorter command? maybe sub-sub commands (template set and template unset)
    command = 'commit-template'
    description = 'Configure git commit template for a branch.'

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
        ticket = cmd.prompt(
            'Ticket',
            'Enter ticket number to use in commit messages.',
            invalid_msg='Invalid ticket number formatting.',
            initial_input=self.args.ticket,
            # TODO custom format_function and validate_function
        )
        args['ticket'] = ticket

        return args

    def get_format_kwargs(self, args, configs, branch_name):
        """Returns a dict mapping placeholders to their respective values.

        :param args: get_args() result
        :param configs: Configs instance
        :param branch_name: Name of the branch to create template for

        :return: Dictionary to pass as kwargs to .format()
        """
        # TODO: client?
        format_kwargs = {
            'ticket': args['ticket'],
            'branch': branch_name,
            'initials': configs.INITIALS or '',
        }
        return format_kwargs

    def create_template(self, args, configs, repo_root_dir, branch_name):
        """Create git commit template file.

        :param args: get_args() result
        :param configs: Configs instance
        :param repo_root_dir: Root directory of git repo
        :param branch_name: Name of the branch to create template for

        :return: Filename of the created template file
        """
        format_kwargs = self.get_format_kwargs(args, configs, branch_name)
        # TODO make sure does not conflict with existing file?
        commit_template_file = files.sanitize_filename(
            configs.COMMIT_TEMPLATE_FILENAME_FORMAT.format(**format_kwargs)
        )
        commit_template_path = os.path.join(repo_root_dir, commit_template_file)
        self.print('Creating commit template file...')
        commit_template_body = configs.COMMIT_TEMPLATE_FORMAT.format(**format_kwargs)
        with open(commit_template_path, 'w') as f:
            f.write(commit_template_body)
        # TODO VERIFY COMMIT TEMPLATE
        self.print('Template file created:', commit_template_path, formatting=cmd.SUCCESS)
        return commit_template_file

    def configure_template(self, configs, branch_name, commit_template_file):
        """Configure commit.template in branch's config file, then configure
        local repo to include branch's config file when that branch is checked
        out.

        :param configs: Configs instance
        :param branch_name: Name of the branch
        :param commit_template_file: Commit template filename
        """
        # TODO rephrase output?
        branch_config_file = files.sanitize_filename(f'config_{branch_name}')
        branch_config_path = os.path.join(self.repo.git_dir, branch_config_file)
        self.print(f'Configuring commit.template for {branch_name}...')
        self.repo.git.config('commit.template', commit_template_file, file=branch_config_path)
        self.print(f'commit.template configured in .git/{branch_config_file}.', formatting=cmd.SUCCESS)
        self.print('Configuring local repo...')
        self.repo.git.config(f'includeIf.onbranch:{branch_name}.path', branch_config_file, file=configs.CONFIG_PATH)
        self.print('Local repo configured.',
                   f'Will include branch config .git/{branch_config_file}',
                   f'when branch {branch_name} is checked out.',
                   formatting=cmd.SUCCESS)

    def run(self):
        args = self.get_args()
        configs = Configs(self.repo)
        repo_root_dir = os.path.dirname(self.repo.git_dir)
        branch_name = self.repo.active_branch.name
        commit_template_file = self.create_template(args, configs, repo_root_dir, branch_name)
        self.configure_template(configs, branch_name, commit_template_file)
