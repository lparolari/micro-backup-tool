import zlib
import zipfile
from os import path
from os import walk
import datetime
import os
import logging
import re
import shutil


class Backup(object):

    # Archive Types
    AT_TARGZ = 'targz'
    AT_ZIP = 'zip'
    
    DT_FORMAT = '%Y%m%d-%H%M%S'

    _exec_path = None
    _backup_paths = None
    _out_path = None
    _out_name = None
    _archive_type = None
    _tmp_archive_name = None
    _start_datetime = None
    _log_filename = None
    _errorlog_filename = None
    _unbacked_list_filename = None

    _log = None
    _ignore_re = None

    def __init__(self, exec_path,
                 backup_paths=None,
                 out_path='',
                 out_name=None,
                 out_cont=False,
                 archive_type=AT_TARGZ,
                 logs_enabled=True):
        """
        Initializes backup object.
        Args:
            exec_path: string   The script execution path.
            backup_paths: list<string>  The paths backup.
            out_path: string    The output path of the script.
            out_name: string    The output backup name.
            out_cont: bool  Enable folder output container.
            archive_type: string    The archive type.
            logs_enabled: bool  Enable logging.
        """

        now = datetime.datetime.now()
        out_name = out_name if out_name is not None else 'bck_{}'.format(datetime.datetime.now().strftime(self.DT_FORMAT))
        backup_paths = backup_paths if backup_paths is not None else [exec_path]

        self._exec_path = exec_path
        self._backup_paths = backup_paths
        self._archive_type = archive_type
        self._out_path = out_path
        self._out_name = out_name
        self._start_datetime = now
        self._tmp_archive_name = out_name + '.tmp'
        self._log_filename = out_name + '.log.txt'
        self._errorlog_filename = out_name + '.errorlog.txt'
        self._unbacked_list_filename = out_name + '.unbacked.txt'

        self._log = logging.Logger('mbt_logger')
        self._log.addHandler(logging.FileHandler(self._log_filename))

        self._ignore_re = self._parse_mbtignore()

        # Self contained.
        if out_cont:
            self._out_path = path.join(out_path, out_name)
            os.mkdir(self._out_path, 0o777)

        assert self._ok()

    def backup(self):
        """
        Executes the backup process.
        Returns:
            Void
        """
        zip_out = zipfile.ZipFile(self._tmp_archive_name, 'w', zipfile.ZIP_DEFLATED)

        # Iterating thought folder trees.
        for bpath in self._backup_paths:
            bpath = str(bpath)

            # todo: this works but there should be a better way to do this (allow to not specify --bakcup_paths !!)
            if bpath.endswith('/'):
                bpath = bpath[:-1]
            paths = bpath.split('/')
            for p in paths[:-1]:
                os.chdir(p)

            self._logd("*** ROOT DIRECTORY ***", prefix='', separator='')
            self._logd(bpath, prefix='***')
            # Walk visit all folders recursively
            for (folder, subfolders, files) in os.walk(paths[-1]):
                zip_out.write(folder)  # Write the path to the zip.
                self._logd(folder)
                for file in files:
                    # Add files in right path position.
                    f = os.path.join(folder, file)
                    zip_out.write(f)
                    self._logd(f)

        os.chdir(self._exec_path)

        zip_out.close()

        shutil.move(self._tmp_archive_name, path.join(self._out_path, self._out_name_full()))
        shutil.move(self._log_filename, path.join(self._out_path, self._log_filename))

    def _logd(self, msg, level=logging.DEBUG, prefix='+', separator=' '):
        """
        Prints debug on logging file.
        Args:
            msg: string The message to output.
            level: int  The log level.
            prefix: string  The message's prefix.
            separator: string   The message-prefix' separator.
        """
        self._log.log(level, prefix+separator+msg)

    def _out_name_full(self):
        """
        Generates the output full name for the backup file.
        Returns:
            string  The backup file full name.
        """
        return self._out_name + '.' + self._get_extension()

    def _parse_mbtignore(self):
        """
        Parses the .mbtignore file into regex.
        """
        try:
            file = open(path.join(self._exec_path, '.mbtignore'), 'r')
            content = file.read()
        except FileNotFoundError as e:
            content = ''

        return re.compile(content)

    def _get_extension(self):
        """
        Gets archive's extension based on chosen compression.
        Returns:
            The archive extension based on compression.
        """
        if self._archive_type == self.AT_TARGZ:
            return 'tar.gz'
        else:
            return 'zip'

    def _ok(self):
        """
        Checks class invariant.
        Returns:
            True if invariant is ok, false otherwise.
        """
        ok = True
        ok = ok and self._exec_path is not None
        ok = ok and self._archive_type in [self.AT_TARGZ, self.AT_ZIP]
        ok = ok and self._tmp_archive_name is not None
        ok = ok and self._log is not None
        ok = ok and self._ignore_re is not None
        return ok

# fh = logging.FileHandler(r'/path/to/log.txt')
# fh.setFormatter(formatter)
# logger.addHandler(fh)
