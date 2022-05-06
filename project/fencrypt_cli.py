import argparse
import getpass
import pathlib
import sys
import logging
import errno
logger = logging.getLogger('Fencrypt')
FORMAT = "[%(levelname)s - %(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.CRITICAL)


def get_password()->str:
    logger.debug("trying to get password")
    if sys.stdin.isatty():
        password= getpass.getpass("password: ")
    else:
        password= sys.stdin.readline().strip()
    logger.debug("Got password")
    if password is None or len(password)<1:
        logger.debug("No password")
        sys.exit(errno.EINVAL)
    return password


def file_checks(file):
    try:
        path = pathlib.Path(file)
        if not path.exists() or not path.is_file() or path.stat().st_size < 32 :
            logger.error("File Failed Check")
            sys.exit(errno.EINVAL)
    except FileNotFoundError as fe:
        logger.debug(fe)
        # sys.exit(errno.ENOENT)
        return False
    return True
def arg_setup():
    parser = argparse.ArgumentParser(prog="fencrypt", description='Process some encryption.')
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('-j', dest='json_out', action='store_true', help='enable json output')
    group.add_argument('-d', dest='decrypt', action='store_true', help='enable decryption mode')
    group.add_argument('-e', dest='encrypt', action='store_true', help='enable encryption mode')
    group.add_argument('-s', dest='search',action='store_true')
    parser.add_argument('--v',dest='log_level',type=int,default=0)
    parser.add_argument(dest="files", nargs='+', type=pathlib.Path)
    try:
        args = parser.parse_args()
    except (argparse.ArgumentError,FileNotFoundError) as ae:
        logger.debug(ae)
        sys.exit(errno.ENOENT)
    if args.log_level==1:
        logger.setLevel(logging.INFO)
    if args.log_level==2:
        logger.setLevel(logging.DEBUG)
    if not args.search and not args.decrypt:
        logger.debug("opperation not set so will try to encrypt")
        args.encrypt=True
    if args.search:
        return args
    for file in args.files:
        check_status = file_checks(file)
        logger.debug(file.stat())
        logger.debug(file.name+" : "+str(check_status))
        metadata = pathlib.Path(f'{file.parent}/.fenc-metadata.{file.name}')
        if not check_status:
            logger.error("Bad status")
            sys.exit(13)
        if args.encrypt:
            if metadata.exists() and metadata.is_file():
                logger.error("Metadata already exists for this file.")
                sys.exit(errno.EEXIST)
        elif args.decrypt:
            logger.debug(metadata.parent)
            if not metadata.exists() or not metadata.is_file():
                logger.error("Metadata missing for file")
                sys.exit(errno.ENOENT)
    return args
