import datetime
import re

from git_workflow.utils import cmd
from .base import WorkflowBase

class Branch(WorkflowBase):
    """Create a new branch."""
    # TODO DOCUMENT SCRIPT ABOVE

    def format_branch_name(self, val):
        return re.sub('[ _ ]+', '-', val.lower())

    def run(self):
        # TODO EXTRACT PROMPTS TO FUNCTION?
        # TODO if not args.no_client: else: client = ''
        arg_client = None # TODO see if any values were passed in args
        client = cmd.prompt(
            'Client',
            '(Optional) Enter the name of the affected client.',
            initial_input=arg_client,
            validate_function=cmd.validate_optional_prompt,
            format_function=self.format_branch_name,
        )
        if client:
            client += '-'

        arg_description = None # TODO args.description
        description = cmd.prompt(
            'Description',
            'Enter a brief description for the branch.',
            invalid_msg='Description must not be blank.',
            initial_input=arg_description,
            format_function=self.format_branch_name,
        )
        description += '-'

        arg_initials = None # TODO arg.initials or config.initials, print info if configured
        initials = cmd.prompt(
            'Initials',
            'Enter your initials.',
            invalid_msg='Must enter initials.',
            initial_input=arg_initials,
            format_function=self.format_branch_name,
        )

        # TODO TICKET #

        # TODO allow arg override
        timestamp = datetime.datetime.now().strftime('%Y%m%d-')

        branch_name = client + description + timestamp + initials
        # TODO DEBUG
        print(branch_name)

