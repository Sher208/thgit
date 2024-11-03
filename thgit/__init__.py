from thgit.src.args_parser import parse_args

def main():
    args = parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        exit("Invalid Command Found")