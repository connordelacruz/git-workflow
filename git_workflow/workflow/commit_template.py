import os
from git_workflow.utils import cmd
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

    def render_commit_template_body(self, args, configs, branch_name):
        # TODO DOC
        # TODO USE CONFIGURED TEMPLATE FORMAT!
        commit_template_body = '[{ticket}] '.format(ticket=args['ticket'])
        return commit_template_body

    def create_template(self, args, configs, branch_name=None):
        # TODO DOC
        if branch_name is None:
            branch_name = self.repo.active_branch.name
        repo_root_dir = os.path.dirname(self.repo.git_dir)
        # TODO make sure filename is valid and does not conflict with existing
        commit_template_file = '.gitmessage_local_{ticket}_{branch_name}'.format(ticket=args['ticket'], branch_name=branch_name)
        commit_template_path = os.path.join(repo_root_dir, commit_template_file)
        self.print('Creating commit template file...')
        with open(commit_template_path, 'w') as f:
            f.write(self.render_commit_template_body(args, configs, branch_name))
        # TODO VERIFY COMMIT TEMPLATE
        self.print('Template file created:', commit_template_path, formatting=cmd.SUCCESS)

    def run(self):
        args = self.get_args()
        configs = Configs(self.repo)
        self.create_template(args, configs)
        # TODO Configure the template
