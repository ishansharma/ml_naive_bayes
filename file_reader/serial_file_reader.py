import os.path
import sys
from file_reader import utilities as u


class SerialFileReader:
    def __init__(self, dir_path):
        """
        Read the filenames from given directory
        Parameters
        ----------
        dir_path : str
        """
        try:
            dir_path = os.path.abspath(dir_path)
            if os.path.isdir(dir_path):
                self.files = list(map(lambda file_path: (os.path.join(dir_path, file_path)),
                                      filter(u.FileUtilities.filter_text_files, os.listdir(dir_path))))
                self.document_count = len(self.files)
                self.index = 0
            else:
                tb = sys.exc_info()[2]
                raise FileNotFoundError().with_traceback(tb)
        except FileNotFoundError as f:
            print("File not found exception", f)
            exit(0)

    def next(self):
        """
        Get the word frequency for next file

        Returns
        -------
        bool/dict
        """
        if self.index > self.document_count:
            self.index = 0  # need to loop back to first file
            return False

        file_path = self.files[self.index]
        words = u.FileUtilities.get_word_frequency(file_path)

        return words
