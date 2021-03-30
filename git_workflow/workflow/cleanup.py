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
        orphans = targets.pop('orphans', [])
        # Pop current branch's configs if we shouldn't include it
        if not args['include_current_branch']:
            current_branch = targets.pop(self.repo.active_branch.name, None)
        # Otherwise keep track of it for messaging
        else:
            current_branch = targets.get(self.repo.active_branch.name, None)
        # Output: Configured Templates (unless --orphans-only)
        if not args['orphans_only']:
            # Case 1: We have branches to clean
            if targets:
                self.print('Commit templates will be unset for the following branches:',
                           '',
                           *targets.keys(),
                           '')
                if args['include_current_branch'] and current_branch:
                    self.print_warning('This includes the branch you are currently on!',
                                       '')
            # Case 2: Nothing to clean but current branch has a template
            elif current_branch:
                self.print('Only branch with a template configured is the current branch.')
                self.print('To include the current branch, use --include-current-branch argument.',
                           '')
        # Output: Orphans
        if orphans:
            self.print('The following commit templates do not have an associated branch and will be deleted:',
                       '',
                       *orphans,
                       '')
        # Output: Nothing to clean up
        if (not targets or args['orphans_only']) and (not orphans):
            self.print('Nothing to clean up.')
            return
        # Confirmation
        if args['confirm']:
            confirmation = cmd.prompt(
                'Confirm (y/n)',
                'Would you like to continue?',
                default_val='n', validate_function=cmd.validate_yn
            )
            if not confirmation:
                return
        # Unset Configured Templates
        if not args['orphans_only'] and targets:
            self.print('Unsetting configured templates...')
            for branch_name in targets.keys():
                unset_template_parsed_args = self.parser.parse_args([UnsetTemplate.command, branch_name, '--force'])
                unset_template = UnsetTemplate(self.repo, self.parser,
                                               parsed_args=unset_template_parsed_args,
                                               # TODO match verbosity if > 1?
                                               verbosity=0)
                unset_template.run()
                self.print_success(f'{branch_name} template unset.')
            self.print('')
        # Delete Orphans
        if orphans:
            self.print('Removing orphan templates...')
            repo_root_dir = os.path.dirname(self.repo.git_dir)
            for orphan in orphans:
                orphan_path = os.path.join(repo_root_dir, orphan)
                # NOTE: Probably don't need this exists() check since find_cleanup_targets()
                # builds this list based on the files it finds, but doing it just to be safe
                if os.path.exists(orphan_path):
                    os.remove(orphan_path)
                    if not os.path.exists(orphan_path):
                        self.print_success(f'Deleted {orphan}.')
                    else:
                        self.print_warning(f'Unable to delete {orphan}.')
            self.print('')

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
