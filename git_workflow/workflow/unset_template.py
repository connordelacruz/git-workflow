import os
from git import GitCommandError
from .base import WorkflowBase


class UnsetTemplate(WorkflowBase):
    """Unset configs for commmit template."""

    command = 'unset-template'
    description = 'Remove commit template for a branch.'

    @classmethod
    def add_subparser(cls, subparsers, generic_parent_parser):
        unset_commit_template_subparser = subparsers.add_parser(
            cls.command, description=cls.description, help=cls.description,
            parents=[generic_parent_parser], add_help=False
        )
        # TODO ARGS; configure to prompt for confirmation unless -f

    def get_args(self):
        """Parse command line arguments and prompt for any missing values.

        :return: A dictionary with the following keys:
            TODO: list
        """
        args = {}

        # TODO: take parsed_args.branch
        branch = self.repo.active_branch.name
        args['branch'] = branch

        return args

    def run(self):
        args = self.get_args()
        # Get branch config path, print and exit if non-existent
        branch_config_file = self.get_branch_config_file(args['branch'])
        if branch_config_file is None:
            self.print(f'Branch {args["branch"]} does not have an associated config file.')
            return
        branch_config_path = os.path.join(self.repo.git_dir, branch_config_file)
        # Verify config file exists
        if not os.path.exists(branch_config_path):
            self.print(f'Config file {branch_config_file} not found, unsetting include...')
            self.unset_includeif_onbranch_path(args['branch'])
            self.print_success('Config include removed.')
            return
        # Unset commit.template in branch config file
        self.print(f'Unsetting commit.template config for {args["branch"]}...')
        commit_template_file = self.get_commit_template_file_and_unset_config(branch_config_path)
        if commit_template_file is None:
            self.print(f'commit.template not configured for branch {args["branch"]}.')
            return
        self.print_success('commit.template config unset.')
        # Delete commit template
        repo_root_dir = os.path.dirname(self.repo.git_dir)
        commit_template_path = os.path.join(repo_root_dir, commit_template_file)
        if os.path.exists(commit_template_path):
            self.print(f'Deleting commit template file {commit_template_file}...')
            os.remove(commit_template_path)
            self.print_success('Commit template file removed.')
        else:
            self.print('Commit template file already removed.')
        # If branch config is now empty, delete the file and unset includeIf
        # TODO re: above, commit-template won't add duplicate entry for include path, will it?
        if os.stat(branch_config_path).st_size == 0:
            self.print(f'Removing empty branch config file and unsetting include...')
            self.unset_includeif_onbranch_path(args['branch'])
            os.remove(branch_config_path)
            self.print_success(f'Empty branch config removed.')

    # Helper Methods

    def get_branch_config_file(self, branch):
        return self.configs.get_config(
            f'includeif.onbranch:{branch}.path',
            local=True, includes=True
        )

    def get_commit_template_file_and_unset_config(self, branch_config_path):
        commit_template_file = self.configs.get_config(
            'commit.template', file=branch_config_path
        )
        self.configs.unset_config(
            'commit.template', file=branch_config_path
        )
        return commit_template_file

    def unset_includeif_onbranch_path(self, branch):
        self.configs.unset_config(
            f'includeif.onbranch:{branch}.path', file=self.configs.CONFIG_PATH
        )
