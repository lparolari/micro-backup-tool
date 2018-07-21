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
    parser.add_argument('--backup_paths', '-b', default=None, required=True, nargs='*', help='Paths to backup')
    parser.add_argument('--archive_type', '-t', default='targz', choices=['targz', 'zip'], help='The archive format')
    parser.add_argument('--logs_disabled', '-l', default=False, help='Disable logging')
    parser.add_argument('--errorlogs_disabled', '-e', default=False, help='Disable error logging')
    parser.add_argument('--unbacked_list_disabled', '-u', default=False, help='Disable unbacked-up files list')
    parser.add_argument('--out_path', '-p', default='', help='The output directory for the backup file')
    parser.add_argument('--out_name', '-n', default=None, help='The output name for the backup file')
    parser.add_argument('--out_cont', '-s', default=False, nargs='?', type=bool, choices=[False, True], help='Create output folded named as backup name')
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
    archive_type = args.archive_type
    out_name = args.out_name
    out_path = args.out_path
    out_cont = args.out_cont if args.out_cont is not None else True

    b = Backup(exec_path=exec_path,
               backup_paths=backup_paths,
               archive_type=archive_type,
               out_path=out_path, out_name=out_name, out_cont=out_cont)
    b.backup()

    # Put your main script logic here
    # print('No action defined for mbt module!')


if __name__ == '__main__':
    main()
