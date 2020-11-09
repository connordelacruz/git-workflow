"""Common argparser utilities."""
import argparse

from git_workflow.__about__ import __version__

def get_generic_parent_parser():
    """Returns a generic parent ArgumentParser with --help, --version, and
    --verbose args

    Note: parsers that have this as a parent should be initialized with
    add_help=False. This parser overrides the default help arg so it can be
    nested under the 'General' group in help message output

    :return: ArgumentParser to use as parent
    """
    parser = argparse.ArgumentParser(add_help=False)
    group = parser.add_argument_group('General')
    # Overriding the default -h arg so it can be nested under the 'General'
    # heading in help message. Parsers that have this as a parent should be
    # initialized with add_help=False
    group.add_argument('-h', '--help', action='help',
                       help='Show this help message and exit')
    group.add_argument('-V', '--version', action='version',
                       version='%(prog)s ' + __version__,
                       help='Show version number and exit')
    # TODO: Implement verbose
    # group.add_argument('-v', '--verbose', type=int, choices=range(0,3),
    #                    nargs='?', default=1, const=2,
    #                    help='Set verbosity level')
    return parser


