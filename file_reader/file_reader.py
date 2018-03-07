import os.path
import sys
import io
import re


class FileReader:
    index = 0

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
                                      filter(self.filter_text_files, os.listdir(dir_path))))
                self.document_count = len(self.files)
                self.vocabulary = self.construct_vocabulary(self.files)
            else:
                tb = sys.exc_info()[2]
                raise FileNotFoundError().with_traceback(tb)
        except FileNotFoundError as f:
            print("File not found exception", f)
            exit(0)

    def construct_vocabulary(self, files):
        """
        Given a list of files, read them one by one and construct vocabulary

        Parameters
        ----------
        files

        Returns
        -------
        vocab : dict
        """
        vocab = {}

        for file in files:
            words = self.get_word_frequency(file)
            for word in words:
                if word in vocab:
                    vocab[word] += words[word]
                else:
                    vocab[word] = words[word]
        return vocab

    def get_word_frequency(self, file_path):
        """
        Accept a file_path and return the list of words along with frequency for it

        Parameters
        ----------
        file_path

        Returns
        -------
        words : dict
        """
        words = {}

        with io.open(file_path, 'r', encoding='utf8', errors='ignore') as f:
            # replace new lines with spaces
            file_text = f.read().replace('\n', ' ')

            # strip everything but text and numbers
            file_text = re.sub(r'[\W+]', ' ', file_text)

            # remove excess spaces
            file_text = re.sub(r'\s+', ' ', file_text)

            file_text = file_text.split(' ')

            for word in file_text:
                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1
        return words

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
