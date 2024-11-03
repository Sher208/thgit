import argparse
from thgit.src.commands import init, commit

def parse_args():
    parser = argparse.ArgumentParser()

    commands = parser.add_subparsers(dest='command')
    commands.required = True

    init_parser = commands.add_parser('init', help="Init the application")
    init_parser.set_defaults(func=init)

    commit_parser = commands.add_parser('commit', help="Commit the application")
    commit_parser.set_defaults(func=commit)

    return parser.parse_args()
