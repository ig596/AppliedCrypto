import argparse
import getpass
import json
import logging
import pathlib
import sys
import errno


logger = logging.getLogger('Fencrypt')

FORMAT = "[%(levelname)s - %(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
METADATA_FILENAME = '.fenc-meta.{file_name}'
logging.basicConfig(format=FORMAT)

logger.setLevel(logging.CRITICAL)


def get_files_in_dir(directory: pathlib.Path):
    if directory is None:
        directory=pathlib.Path()
    logger.debug(directory.name)
    files = []

    for item in directory.iterdir():

        if item.is_file():
            files.append(item)
    logger.debug(files)
    return files


def get_metadata(file:pathlib.Path) -> dict:
    metadata_file=file.with_name(METADATA_FILENAME.format(file_name=file.name))
    return json.loads(metadata_file.read_text())


def get_password() -> str:
    logger.debug("trying to get password")

    if sys.stdin.isatty():

        password = getpass.getpass("password: ")

    else:

        password = sys.stdin.readline().strip()

    logger.debug("Got password")

    if password is None or len(password) < 1:
        logger.debug("No password")

        return sys.exit(errno.EINVAL)

    return password


def file_checks(file: pathlib.Path):
    if not file.exists() or not file.is_file():
        logger.error("File Failed Check")
        return sys.exit(errno.EINVAL)
    elif  file.stat().st_size < 32:
        logger.error("File Failed Check")
        return sys.exit(errno.EINVAL)
    return True

def check_metadata_status(file:pathlib.Path, encrypt:bool):
    metadata = file.with_name(METADATA_FILENAME.format(file_name=file.name))
    status=False
    if encrypt:
        try:
            logger.debug(metadata.exists())
            if metadata.exists():
                logger.error("Metadata Exists")
                exit(errno.EEXIST)
            else:
                logger.debug("Metadata not found")
                logger.debug(get_files_in_dir(pathlib.Path.cwd()))
                status=True
        except FileNotFoundError:
            logger.debug("couldn't find")
            status =True
    else:
        if (metadata.exists() and metadata.is_file()):
            status = True
    return status

def get_password() -> str:
    logger.debug("trying to get password")
    if sys.stdin.isatty():
        password = getpass.getpass("password: ")
    else:
        password = sys.stdin.readline().strip()
    logger.debug("Got password")

    if password is None or len(password) < 1:
        logger.debug("No password")

        return sys.exit(errno.EINVAL)

    return password

def arg_checks(args):

    # logger.debug(args)

    if not args.search and not args.decrypt and not args.encrypt:
        logger.debug("operation not set so will try to encrypt")
        args.encrypt = True
    elif not args.search:
        # logger.debug(get_files_in_dir(pathlib.Path()))
        args.files = [pathlib.Path(file) for file in args.files]
        for file in args.files:
            check_status = file_checks(file)
            logger.debug(file.name + " : " + str(check_status))
            if not check_status:
                logger.error("Bad status")
                return sys.exit(errno.EBADF)
            elif not check_metadata_status(file,args.encrypt):
                logger.error("Bad metadata")
                return sys.exit(errno.EBADF)
        return args


def arg_setup():
    parser = argparse.ArgumentParser(prog="fencrypt", description='Process some encryption.')

    group = parser.add_mutually_exclusive_group()

    parser.add_argument('-j', dest='json_out', action='store_true', help='enable json output')

    group.add_argument('-d', dest='decrypt', action='store_true', help='enable decryption mode')

    group.add_argument('-e', dest='encrypt', action='store_true', help='enable encryption mode')

    group.add_argument('-s', dest='search', action='store_true')

    parser.add_argument('--v', dest='log_level', type=int, default=1)

    parser.add_argument(dest="files", nargs='+', type=str)

    try:

        args = parser.parse_args()  # logger.debug(args)
        if args.log_level < 1:
            logger.setLevel(logging.ERROR)
        elif args.log_level == 1:
            logger.setLevel(logging.INFO)
        elif args.log_level == 2:
            logger.setLevel(logging.DEBUG)

    except (argparse.ArgumentError) as ae:
        logger.error(ae)
        return sys.exit(errno.ENOENT)

    args=arg_checks(args)
    return args
