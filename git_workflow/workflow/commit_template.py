from git_workflow.utils import cmd, repository
from .base import WorkflowBase


class CommitTemplate(WorkflowBase):
    """Create and configure commit template."""
    # TODO shorter command? maybe sub-sub commands (template set and template unset)
    command = 'commit-template'
    description = 'Configure git commit template for a branch.'

    @classmethod
    def add_subparser(cls, subparsers, generic_parent_parser):
        # TODO add command description abstract property and make this part generic in parent class:
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
            invalid_msg='Invalid ticket number formatting.', # TODO details
            initial_input=self.args.ticket,
            # TODO custom format_function and validate_function
        )
        args['ticket'] = ticket

        return args

    def run(self):
        args = self.get_args()
        repository.initialize(self.repo)
        # TODO Create template file
        # TODO Configure the template
