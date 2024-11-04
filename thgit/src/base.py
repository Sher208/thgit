import os
import fnmatch
from thgit.src.variables import GIT_DIR, GIT_IGNORE
from . import data

def _iter_tree_entries(oid):
    if not oid:
        return
    tree = data.get_object(oid, 'tree')
    for entry in tree.decode().splitlines():
        type_, oid, name = entry.split(' ', 2)
        yield type_, oid, name


def get_tree(oid, base_path=''):
    result = {}
    for type_, oid, name in _iter_tree_entries(oid):
        assert '/' not in name
        assert name not in ('..', '.')
        path = base_path + name
        if type_ == 'blob':
            result[path] = oid
        elif type_ == 'tree':
            result.update(get_tree(oid, f'{path}/'))
        else:
            assert False, f'Unknown tree entry{type_}'
    return result

def read_tree(tree_oid):
    for path, oid in get_tree(tree_oid, base_path='./').items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(data.get_object(oid))


def write_tree(directory='.'):
    entries = []
    with os.scandir(directory) as it:
        for entry in it:
            full = f'{directory}/{entry.name}'
            if is_ignored_from_file(full) or is_ignored(full):
                continue
            if entry.is_file(follow_symlinks=False):
                type_ = 'blob'
                with open(full, 'rb') as f:
                    oid = data.hash_object(f.read())
            elif entry.is_dir(follow_symlinks=False):
                type_ = 'tree'
                oid = write_tree(full)
            entries.append((type_, oid, entry.name))

    tree = ''.join(f'{type_} {oid} {name}\n' for type_, oid, name in sorted(entries))

    return data.hash_object(tree.encode(), 'tree')

def is_ignored(path):
    ugit_ignore = GIT_DIR in path.split('/')
    file_ingore = GIT_IGNORE in path.split('/')
    return ugit_ignore or file_ingore

def is_ignored_from_file(path, ignore_file=GIT_IGNORE):
    if not os.path.exists(path):
        return False
    
    patterns = parse_ignore_file(ignore_file)
    normalized_path = os.path.normpath(path)
    for pattern in patterns:
        normalized_pattern = os.path.normpath(pattern)
        if fnmatch.fnmatch(normalized_path, normalized_pattern):
            return True
        
    return False

def parse_ignore_file(file_path=GIT_IGNORE):
    patterns = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()

                if line and not line.startswith("#"):
                    patterns.append(line)
    except FileNotFoundError:
        print(f"Ingore file {file_path} not found.")
    return patterns