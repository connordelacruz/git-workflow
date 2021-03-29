import glob
import os
import re
from git_workflow.utils import cmd
from .base import WorkflowBase
from .unset_template import UnsetTemplate

class Cleanup(WorkflowBase):
    """TODO"""

    command = 'cleanup'
    description = 'Tidy up workflow-related files and configs.'
    # TODO configs_used = []

    @classmethod
    def add_subparser(cls, subparsers, generic_parent_parser):
        cleanup_subparser = subparsers.add_parser(
            cls.command, description=cls.description, help=cls.description,
            parents=[generic_parent_parser], add_help=False
        )
        # TODO confirmation, --include-current-branch, --orphans-only

    def get_args(self):
        args = {}
        # TODO implement
        args['confirm'] = True
        args['include_current_branch'] = False
        args['orphans_only'] = False
        return args

    def run(self):
        args = self.get_args()
        targets = self.find_cleanup_targets()
        # TODO handle include_current_branch

    # Helper Methods

    def find_cleanup_targets(self):
        """Get configured and orphaned commit templates.

        :return: Dictionary with keys for each branch that map to a dictionary
            with keys 'config' and 'template' (the respective branch's config
            file and configured template). If there are orphaned commit
            templates, there will also be a key 'orphans' that's mapped to a
            list of orphaned commit templates.
        """
        # Get all branch-specific config paths
        config_expr = 'includeif\.onbranch:(.*)\.path'
        config_matches = self.configs.call_config_command(
            config_expr, file=self.configs.CONFIG_PATH, get_regexp=True
        )
        if config_matches is not None:
            config_matches = config_matches.split('\n')
        else:
            config_matches = []
        # Map branch names to their config files and configured templates
        expr = r'includeif\.onbranch:(.*)\.path (.*)'
        targets = {}
        # Used to keep track of all configured commit templates so orphaned ones can be determined
        configured_commit_templates = []
        for line in config_matches:
            match = re.match(expr, line)
            if match:
                branch_name = match.group(1)
                branch_config_file = match.group(2)
                branch_commit_template = self.configs.get_config(
                    'commit.template', file=os.path.join(self.repo.git_dir, branch_config_file)
                )
                targets[branch_name] = {
                    'config': branch_config_file,
                    'template': branch_commit_template,
                }
                configured_commit_templates.append(branch_commit_template)
        # Find orphaned templates
        repo_root_dir = os.path.dirname(self.repo.git_dir)
        all_commit_templates = [
            os.path.basename(path)
            for path in glob.glob(os.path.join(repo_root_dir, '.gitmessage_local*'))
        ]
        orphan_commit_templates = [
            template for template in all_commit_templates
            if template not in configured_commit_templates
        ]
        if orphan_commit_templates:
            targets['orphans'] = orphan_commit_templates
        return targets
