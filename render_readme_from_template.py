#!/usr/bin/env python3
"""Generate README.rst from template.

Requires Jinja2, which is included in the dev extras. To install these, run:

    pip install -e .[dev]
"""
import os
import jinja2
from git_workflow.__main__ import get_parser
from git_workflow.workflow import commands

def main():
    # Set context for template
    context = {
        'workflow': {
            'command': 'workflow',
        },
    }
    parser = get_parser()
    for command, command_class in commands.items():
        context[command.replace('-', '_')] = {
            'command': command_class.command,
            'desc': command_class.description,
            # TODO HELP
        }
    # TODO render .j2 template to file
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

if __name__ == '__main__':
    main()

