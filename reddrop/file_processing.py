import copy
import os
import tarfile
import datetime
import tempfile
from unicodedata import numeric

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from reddrop.config import config
from reddrop.processors import processFromList
from reddrop.logger import logger

def tarfileIsSafe(tarFile: tarfile.TarFile):
    """
    Validate that each member in the tarFile does not contain 
    an absolute path nor a relative path which could overwrite existing files
    
    Why? From the docs:  https://docs.python.org/3/library/tarfile.html#tarfile.TarFile.extractall
     Warning:
     Never extract archives from untrusted sources without prior inspection. 
     It is possible that files are created outside of path, 
     e.g. members that have absolute filenames starting with `/` or 
     filenames with two dots `..`.
    """
    for member in tarFile:
        memberPath = os.path.normpath(member.name)
        
        if memberPath.startswith("..") or os.path.isabs(memberPath):
            return False

    return True


def extractTarFile(tar:tarfile.TarFile, path="."):
    """
    A combination of the techniques illustrated in the `tarfile.TarFile.extractall()` method and 
    those outlined here: 
    - https://github.com/python/cpython/blob/main/Lib/tarfile.py#L2029
    - https://stackoverflow.com/questions/7237475/overwrite-existing-read-only-files-when-using-pythons-tarfile

    This function allows us to extract files with read-only permissions by first removing the originals on extraction.
    """
    directories = []

    for tarinfo in tar:
        if tarinfo.isdir():
            # Extract directories with a safe mode.
            directories.append(tarinfo)
            tarinfo = copy.copy(tarinfo)
            tarinfo.mode = 0o700

        filename = os.path.join(path, tarinfo.name)

        try:
            tar.extract(tarinfo, path=path, set_attrs=not tarinfo.isdir())

        except IOError as e:
            os.remove(filename)
            tar.extract(tarinfo, path=path, set_attrs=not tarinfo.isdir())

        # TODO: 
        # FileNotFoundError - 
        # Need to figure out why! File exists! File is a symlink, maybe thats messing something up
        if not os.path.islink(filename):
            os.chmod(filename, tarinfo.mode)
        
    # Reverse sort directories.
    directories.sort(key=lambda a: a.name)
    directories.reverse()
    numeric_owner = False

    for tarinfo in directories:
        dirpath = os.path.join(path, tarinfo.name)
        try:
            tar.chown(tarinfo, dirpath, numeric_owner=numeric_owner)
            tar.utime(tarinfo, dirpath)
            tar.chmod(tarinfo, dirpath)

        except tarfile.ExtractError as e:
            if tar.errorlevel > 1:
                raise
            else:
                tar._dbg(1, "tarfile: %s" % e)

def processFile(parameter:str, f:FileStorage, src_ip:str, processing_list=[]):
    """
    Process a FileStorage object `f` and save it to disk with a concatenated filename of:
        `<date>.<parameter>.<FileStorage.filename>[.tar.gz]`

    This function will create a directory structure to store files as defined in `config['upload_dir']`, 
      it will create subdirectories based on the `src_ip` passed to it to organize files.

    This function will process and extract tar archive files passed to it given a set of configuration options.
    """

    fileDir = os.path.join(os.path.abspath(config['upload_dir'].get()), secure_filename(src_ip))

    if not os.path.exists(fileDir):
        os.makedirs(fileDir)

    currentTimeStamp = datetime.datetime.now().strftime('%d-%b-%Y-%H-%M-%S')
    fileName = secure_filename(f"{currentTimeStamp}.{parameter}.{f.filename}")

    decodedStream, processing_list = processFromList(f.stream.read(), processing_list)
    f.stream = tempfile.SpooledTemporaryFile()
    f.stream.write(decodedStream)
    f.stream.seek(0)
    del decodedStream

    isArchive = False
    wasExtracted = False
    if tarfile.is_tarfile(f.stream):
        if config['auto_extract_tar'].get():
            try:
                f.stream.seek(0)

                with tarfile.open(fileobj=f.stream, mode="r:") as uploadedTar:
                    if not tarfileIsSafe(uploadedTar):
                        raise Exception("TarFile has unsafe members")
                    
                    try:
                        extractTarFile(uploadedTar, path=fileDir)
                        wasExtracted = True
                    except KeyError: #Exception as e:
                        logger.error(f"There was a problem extracting the TarFile: {e}")
                        wasExtracted = False

            except tarfile.ReadError as e:
                logger.error(f"Could not open Tar archive: {e}")

        isArchive = True
        fileName = f'{fileName}.tar.gz'

    f.stream.seek(0)
    f.save(os.path.join(fileDir, fileName))

    fileLogObject = {
        "fileDir": fileDir,
        "fileName": fileName,
        "isArchive": isArchive,
        "autoExtracted": wasExtracted,
        "process": processing_list,
        "parameter": parameter
    }
    return fileLogObject