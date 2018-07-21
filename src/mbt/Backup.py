import zlib
import zipfile
from os import path
from os import walk


class Backup(object):
    _exec_path = None
    _backup_paths = None
    _out_archive_name = None

    def __init__(self, exec_path, backup_paths=None, out_archive_name=None, logs_enabled=True):
        self._exec_path = exec_path
        self._backup_paths = backup_paths
        if out_archive_name is None:
            self._out_archive_name = 'default.zip'
        assert self._ok()

    def backup(self):
        z = zipfile.ZipFile(self._out_archive_name, 'w', zipfile.ZIP_DEFLATED)
        # Implement here backup logic.

    def _ok(self):
        ok = self._exec_path is not None
        return ok

# fh = logging.FileHandler(r'/path/to/log.txt')
# fh.setFormatter(formatter)
# logger.addHandler(fh)
