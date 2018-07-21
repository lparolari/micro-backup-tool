import zlib
import zipfile
from os import path
from os import walk
import datetime
import os


class Backup(object):
    COMP_TARGZ = 'targz'
    COMP_ZIP = 'zip'

    _exec_path = None
    _backup_paths = None
    _user_out_archive_name = None
    _compression = None
    _tmp_archive_name = None

    def __init__(self, exec_path, backup_paths=None, out_archive_name=None, compression=COMP_TARGZ, logs_enabled=True):
        self._exec_path = exec_path
        self._backup_paths = backup_paths
        self._user_out_archive_name = out_archive_name
        self._compression = compression
        self._tmp_archive_name = "bck_{}.tmp".format(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

        assert self._ok()

    def backup(self):
        """
        Executes the backup process.
        Returns:
            Void.
        """
        zip_out = zipfile.ZipFile(self._tmp_archive_name, 'w', zipfile.ZIP_DEFLATED)

        # Iterating thought folder trees.
        for bpath in self._backup_paths:
            # Walk visit all folders recursively
            for (folder, subfolders, files) in os.walk(bpath):
                zip_out.write(folder)  # Write the path to the zip.
                for file in files:
                    # Add files in right path position.
                    zip_out.write(os.path.join(folder, file))

        zip_out.close()
        self._on_finish()

    def _on_finish(self):
        os.rename(self._tmp_archive_name, self._out_archive_name())

    def _out_archive_name(self):
        """
        Calculates archive name based on user input.
        Returns:
            The archive name.
        """
        if self._user_out_archive_name is not None:
            return self._user_out_archive_name
        else:
            now = datetime.datetime.now()
            return 'bck_' + now.strftime("%Y%m%d-%H%M%S") + '.' + self._get_extension()

    def _get_extension(self):
        """
        Gets archive's extension based on chosen compression.
        Returns:
            The archive extension based on compression.
        """
        if self._compression == self.COMP_TARGZ:
            return 'tar.gz'
        else:
            return 'zip'

    def _ok(self) -> bool:
        """
        Checks class invariant.
        Returns:
            True if invariant is ok, false otherwise.
        """
        ok = True
        ok = ok and self._exec_path is not None
        ok = ok and self._compression in [self.COMP_TARGZ, self.COMP_ZIP]
        ok = ok and self._tmp_archive_name is not None
        return ok

# fh = logging.FileHandler(r'/path/to/log.txt')
# fh.setFormatter(formatter)
# logger.addHandler(fh)
