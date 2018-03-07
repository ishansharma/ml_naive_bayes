import os.path
import sys
import io
import re


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
                files = list(filter(self.filter_text_files, os.listdir(dir_path)))  # list of files in the directory
                self.document_count = len(files)
                self.vocabulary = self.construct_vocabulary(dir_path, files)
            else:
                tb = sys.exc_info()[2]
                raise FileNotFoundError().with_traceback(tb)
        except FileNotFoundError as f:
            print("File not found exception", f)
            exit(0)

    def construct_vocabulary(self, dir_path, files):
        """
        Given a list of files, read them one by one and construct vocabulary
        Parameters
        ----------
        files
        """
        vocab = {}

        for file in files:
            # temporary hack to avoid file
            if file == "2248.2004-09-23.GP.spam.txt":
                continue

            with io.open(os.path.join(dir_path, file), 'r', encoding='utf8') as f:
                # replace new lines with spaces
                file_text = f.read().replace('\n', ' ')

                # strip everything but text and numbers
                file_text = re.sub(r'[\W+]', ' ', file_text)

                # remove excess spaces
                file_text = re.sub(r'\s+', ' ', file_text)

                file_text = file_text.split(' ')

                for word in file_text:
                    if word in vocab:
                        vocab[word] += 1
                    else:
                        vocab[word] = 1
        return vocab

    def filter_text_files(self, file_path):
        """
        If given file path is of type txt, return true

        Parameters
        ----------
        file_path

        Returns
        -------
        bool
        """
        file = os.path.splitext(file_path)

        if file[1] == ".txt":
            return True

        return False
