import os
from cmd_utils import cmd
from .base import WorkflowBase


class UnsetTemplate(WorkflowBase):
    """\
    Remove commmit template for a branch.

    By default, this command will prompt for confirmation before removing the
    commit template unless ``--force`` is specified.
    """

    command = 'unset-template'
    description = 'Remove commit template for a branch.'
    configs_used = ['unsetTemplateConfirmationPrompt']

    @classmethod
    def add_subparser(cls, subparsers, generic_parent_parser):
        unset_commit_template_subparser = cls._add_base_subparser(subparsers, generic_parent_parser)
        # Specify branch
        positional_args = unset_commit_template_subparser.add_argument_group(
            'Positional Arguments'
        )
        positional_args.add_argument(
            'branch', metavar='<branch>', nargs='?',
            help='Branch to unset template for (default: current)',
            default=None
        )
        # Confirmation prompt
        confirmation_args = unset_commit_template_subparser.add_argument_group(
            'Confirmation Prompt Arguments',
            'Override workflow.unsetTemplateConfirmationPrompt config.'
        )
        confirmation_group = confirmation_args.add_mutually_exclusive_group()
        confirmation_group.add_argument(
            '-f', '--force', help='Skip confirmation prompt (if configured)',
            dest='confirm', action='store_false', default=None
        )
        confirmation_group.add_argument(
            '-c', '--confirmation', help='Prompt for confirmation before unsetting',
            dest='confirm', action='store_true', default=None
        )

    def get_args(self):
        """Parse command line arguments and prompt for any missing values.

        :return: A dictionary with the following keys:
            branch, confirm
        """
        args = {}
        args['branch'] = (self.parsed_args.branch
                          if self.parsed_args.branch is not None else
                          self.repo.active_branch.name)
        # Default to config value unless otherwise specified
        args['confirm'] = (self.configs.UNSET_TEMPLATE_CONFIRMATION_PROMPT
                           if self.parsed_args.confirm is None else
                           self.parsed_args.confirm)
        return args

    def run(self):
        args = self.get_args()
        branch = args['branch']
        # Get branch config path, print and exit if non-existent
        branch_config_file = self.configs.get_config(
            f'includeif.onbranch:{branch}.path',
            local=True, includes=True
        )
        if branch_config_file is None:
            self.print(f'Branch {branch} does not have an associated config file.')
            return
        # Confirmation prompt
        if args['confirm']:
            confirmation = cmd.prompt(
                'Unset Template? (y/n)',
                f'Unset commit template for {branch}?',
                default_val='n', validate_function=cmd.validate_yn
            )
            if not confirmation:
                return
        # Verify config file exists
        branch_config_path = os.path.join(self.repo.git_dir, branch_config_file)
        if not os.path.exists(branch_config_path):
            self.print(f'Config file {branch_config_file} not found, unsetting include...')
            self.unset_includeif_onbranch_path(branch)
            self.print_success('Config include removed.', '')
            return
        # Unset commit.template in branch config file
        self.print(f'Unsetting commit.template config for {branch}...')
        commit_template_file = self.configs.get_config(
            'commit.template', file=branch_config_path
        )
        if commit_template_file is None:
            self.print(f'commit.template not configured for branch {branch}.', '')
            return
        self.configs.unset_config(
            'commit.template', file=branch_config_path
        )
        self.print_success('commit.template config unset.', '')
        # Delete commit template
        repo_root_dir = os.path.dirname(self.repo.git_dir)
        commit_template_path = os.path.join(repo_root_dir, commit_template_file)
        if os.path.exists(commit_template_path):
            self.print(f'Deleting commit template file {commit_template_file}...')
            os.remove(commit_template_path)
            self.print_success('Commit template file removed.', '')
        else:
            self.print('Commit template file already removed.')
        # If branch config is now empty, delete the file and unset includeIf
        if os.stat(branch_config_path).st_size == 0:
            self.print(f'Removing empty branch config file and unsetting include...')
            self.unset_includeif_onbranch_path(branch)
            os.remove(branch_config_path)
            self.print_success(f'Empty branch config removed.', '')

    # Helper Methods

    def unset_includeif_onbranch_path(self, branch):
        self.configs.unset_config(
            f'includeif.onbranch:{branch}.path',
            file=self.configs.CONFIG_PATH
        )
