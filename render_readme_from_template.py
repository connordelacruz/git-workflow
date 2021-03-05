#!/usr/bin/env python3
"""Generate README.rst from template.

Requires Jinja2, which is included in the dev extras. To install these, run:

    pip install -e .[dev]
"""
from contextlib import redirect_stdout
from io import StringIO
import os
import sys
import jinja2
from git_workflow.__about__ import *
from git_workflow.__main__ import get_parser
from git_workflow.workflow import commands


RST_INDENT = ' ' * 4


def main():
    # Set context for template
    context = {
        'about': {
            'version': __version__,
            'min_python_version': __min_python_version__,
            'min_git_version': __min_git_version__,
        },
        'workflow': {
            'command': __command__,
        },
    }
    parser = get_parser(prog='workflow')
    for command, command_class in commands.items():
        context[command.replace('-', '_')] = {
            'command': command_class.command,
            'desc': command_class.description,
            'help': get_command_help(parser, command_class),
        }
    # Render .j2 template to file
    project_root = os.path.dirname(os.path.abspath(__file__))
    readme_path = os.path.join(project_root, 'README.rst')
    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(project_root),
        trim_blocks=True, lstrip_blocks=True,
    )
    template = environment.get_template('README.rst.j2')
    readme_contents = template.render(context)
    with open(readme_path, 'w') as f:
        f.write(readme_contents)


# Helper Functions

def get_command_help(parser, command_class):
    help_text = ''
    # No easy way to get help text for a subcommand as a string, so catch stdout
    with StringIO() as buf, redirect_stdout(buf):
        try:
            parser.parse_args([command_class.command, '--help'])
        # Stop argparse help action from exiting after printing
        except SystemExit:
            pass
        help_text = buf.getvalue()
    # Add an indent to support pre-formatted block
    return help_text.replace('\n', '\n' + RST_INDENT)


if __name__ == '__main__':
    main()

