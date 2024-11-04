import argparse
from thgit.src.commands import init, commit, hash_object, cat_object, write_tree, read_tree

def parse_args():
    parser = argparse.ArgumentParser()

    commands = parser.add_subparsers(dest='command')
    commands.required = True

    init_parser = commands.add_parser('init', help="Init the application")
    init_parser.set_defaults(func=init)

    hash_object_parser = commands.add_parser('hash-object')
    hash_object_parser.set_defaults(func=hash_object)
    hash_object_parser.add_argument('file')

    cat_object_parser = commands.add_parser('cat-object')
    cat_object_parser.set_defaults(func=cat_object)
    cat_object_parser.add_argument('file')

    write_tree_parser = commands.add_parser('write-tree')
    write_tree_parser.set_defaults(func=write_tree)

    read_tree_parser = commands.add_parser('read-tree')
    read_tree_parser.set_defaults(func=read_tree)
    read_tree_parser.add_argument('tree')

    commit_parser = commands.add_parser('commit', help="Commit the application")
    commit_parser.set_defaults(func=commit)
    commit_parser.add_argument('-m', '--message', help="Write a commit message", required=True)

    return parser.parse_args()
