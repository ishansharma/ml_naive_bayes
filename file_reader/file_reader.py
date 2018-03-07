import os.path
import sys
from file_reader import utilities as u


class FileReader:
    def __init__(self, dir_path):
        """
        Initialise with path.
        If path is not a directory or does not contain txt files, raise relevant exception and exit.

        Otherwise, count number of files and construct vocabulary

        Parameters
        ----------
        dir_path: str
            String containing path to ham or spam files
        """
        try:
            dir_path = os.path.abspath(dir_path)  # converting directory to a path
            if os.path.isdir(dir_path):
                self.files = list(map(lambda file_path: (os.path.join(dir_path, file_path)),
                                      filter(u.FileUtilities.filter_text_files, os.listdir(dir_path))))
                self.document_count = len(self.files)
                self.vocabulary = u.FileUtilities.construct_vocabulary(self.files)
            else:
                tb = sys.exc_info()[2]
                raise FileNotFoundError().with_traceback(tb)
        except FileNotFoundError as f:
            print("File not found exception", f)
            exit(0)
