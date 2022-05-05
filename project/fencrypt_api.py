import argparse
import pathlib
import getpass
import warnings
warnings.filterwarnings("ignore")


def get_password():
    password = getpass.getpass(prompt=None)
    if password is not None and len(password)>1:
        return password
    else:
        exit(13)

def file_checks(file):
    try:
        path = pathlib.Path(file)
        if not path.exists():
            # print("Path Not Found")
            return False
        elif not path.is_file():
            # print("Not a file")
            return False
        elif path.stat().st_size < 32:
            # print(path.stat())
            # print("File is too small to process")
            return False
        else:
            return True
    except FileNotFoundError as fe:
        print("File Not Found")
        return False


def arg_setup():
    parser = argparse.ArgumentParser(prog="fencrypt", description='Process some encryption.')
    parser.add_argument('-j', dest='json_out', action='store_true',
                        help='enable json output', required=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', dest='decrypt', action='store_true', help='enable decyrption mode')
    group.add_argument('-e', dest='encrypt', action='store_true', help='enable encyrption mode')
    group.add_argument('-s', dest='search',action='store_true')
    parser.add_argument(dest="files", nargs='+', type=pathlib.Path, default=None)
    args = parser.parse_args()
    for file in args.files:
        # print(file)
        check_status = file_checks(file.name)
        if check_status:
            continue
        else:
            exit(13)
    return args
