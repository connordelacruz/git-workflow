from git_workflow.utils import cmd
from .base import WorkflowBase

class Branch(WorkflowBase):
    """Create a new branch."""
    # TODO DOCUMENT SCRIPT ABOVE

    def run(self):
        # TODO if not args.no_client:
        arg_client = None # TODO see if any values were passed in args
        client = cmd.prompt(
            'Client',
            '(Optional) Enter the name of the affected client.',
            validate_function=cmd.validate_optional_prompt,
            initial_input=arg_client
        )
        if client:
            client += '-'
        # TODO DEBUG
        print(client)

