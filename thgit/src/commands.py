import os
import sys
from . import data
from . import base

def init(args):
    data.init()
    print('Initialized empty ugit repository in %s' % os.path.join(os.getcwd(), data.GIT_DIR))

def hash_object(args):
    with open(args.file, 'rb') as f:
        print(data.hash_object(f.read()))

def cat_object(args):
    sys.stdout.flush()
    sys.stdout.buffer.write(data.get_object(args.file, expected=None))

def write_tree(args):
    print(base.write_tree())

def read_tree(args):
    base.read_tree(args.tree)

def commit(args):
    print(base.commit(args.message))