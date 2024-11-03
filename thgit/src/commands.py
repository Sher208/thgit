import os
import thgit.src.data as data

def init(args):
    data.init()
    print('Initialized empty ugit repository in %s' % os.path.join(os.getcwd(), data.GIT_DIR))

def commit(args):
    print("Commit")