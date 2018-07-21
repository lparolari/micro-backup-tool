import os
import mbt
import shutil
from os.path import *


def setup():
    folder = 'out'
    if not isdir(folder):
        os.mkdir(folder, 0o777)
    else:
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)


def test_create_backup_obj():
    setup()

    exec_path = os.getcwd()
    try:
        mbt.Backup(exec_path)
        assert True  # Build correctly.
    except Exception:
        assert False  # Error while creating backup object.


def test_execute_backup():
    setup()

    exec_path = os.getcwd()
    b = mbt.Backup(exec_path, backup_paths=['resources/t1'], out_path='out')
    b.backup()

    name = 'bck_{}'.format(b._start_datetime.strftime('%Y%m%d-%H%M%S'))

    assert isfile(join('out', name + '.tar.gz'))
    assert isfile(join('out', name + '.log.txt'))

    # todo: add assert for errorlog file
    # todo: add assert for upbacked up list file


def test_execute_backup_outname():
    setup()

    exec_path = os.getcwd()
    b = mbt.Backup(exec_path, backup_paths=['resources/t1'], out_path='out', out_name='unconventional_name')
    b.backup()

    name = 'unconventional_name'

    assert isfile(join('out', name + '.tar.gz'))
    assert isfile(join('out', name + '.log.txt'))


def test_execute_backup_outcont():
    setup()

    exec_path = os.getcwd()
    b = mbt.Backup(exec_path, backup_paths=['resources/t1'], out_path='out', out_cont=True)
    b.backup()

    name = 'bck_{}'.format(b._start_datetime.strftime('%Y%m%d-%H%M%S'))

    assert isfile(join('out/' + name, name + '.tar.gz'))
    assert isfile(join('out/' + name, name + '.log.txt'))


def test_execute_backup_targz_type():
    setup()

    exec_path = os.getcwd()
    b = mbt.Backup(exec_path, backup_paths=['resources/t1'], out_path='out', archive_type=mbt.Backup.AT_TARGZ)
    b.backup()

    name = 'bck_{}'.format(b._start_datetime.strftime('%Y%m%d-%H%M%S'))

    assert isfile(join('out', name + '.tar.gz'))
    assert isfile(join('out', name + '.log.txt'))


def test_execute_backup_zip_type():
    setup()

    exec_path = os.getcwd()
    b = mbt.Backup(exec_path, backup_paths=['resources/t1'], out_path='out', archive_type=mbt.Backup.AT_ZIP)
    b.backup()

    name = 'bck_{}'.format(b._start_datetime.strftime('%Y%m%d-%H%M%S'))

    assert isfile(join('out', name + '.zip'))
    assert isfile(join('out', name + '.log.txt'))


def test_execute_backup_mbtignore():
    setup()

    exec_path = os.getcwd()
    b = mbt.Backup(exec_path, backup_paths=['resources/t2'], out_path='out')
    b.backup()

    name = 'bck_{}'.format(b._start_datetime.strftime('%Y%m%d-%H%M%S'))

    assert isfile(join('out', name + '.tar.gz'))
    assert isfile(join('out', name + '.log.txt'))
