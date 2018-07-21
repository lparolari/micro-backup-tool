import argparse
import os
import sys

import mbt
from mbt import __version__, Backup


def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser('micro-backup-tool')
    version = '%(prog)s ' + __version__
    parser.add_argument('--version', '-v', action='version', version=version)
    parser.add_argument('--backup_paths', '-b', default=None, nargs='*', help='Paths to backup')
    parser.add_argument('--compression', '-c', default='targz', choices=['targz', 'zip'], help='The compression format')
    parser.add_argument('--logs_disabled', '-l', default=False, help='Disable logging')
    parser.add_argument('--errorlogs_disabled', '-e', default=False, help='Disable error logging')
    parser.add_argument('--unbacked_list_disabled', '-u', default=False, help='Disable unbacked-up files list')
    return parser


def main(args=None):
    """
    Main entry point for your project.

    Args:
        args : list
            A of arguments as if they were input in the command line. Leave it
            None to use sys.argv.
    """

    parser = get_parser()
    args = parser.parse_args(args)
    print(args)

    exec_path = os.getcwd()
    backup_paths = args.backup_paths
    compression = args.compression

    b = Backup(exec_path=exec_path,
               backup_paths=backup_paths,
               compression=compression)
    b.backup()

    # Put your main script logic here
    # print('No action defined for mbt module!')


if __name__ == '__main__':
    main()
