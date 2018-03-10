import os.path
import io
import re
import copy


class FileUtilities:
    @staticmethod
    def get_word_frequency(file_path):
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

    @staticmethod
    def filter_text_files(file_path):
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

    @staticmethod
    def construct_vocabulary(files):
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
            words = FileUtilities.get_word_frequency(file)
            for word in words:
                if word in vocab:
                    vocab[word] += words[word]
                else:
                    vocab[word] = words[word]
        return vocab

    @staticmethod
    def merge_dictionaries(ham_dict, spam_dict):
        """
        We accept ham and spam dictionary separately. However, we need combined vocabulary.
        This function combined the two dictionaries and sets the vocabulary

        Parameters
        ----------
        ham_dict
        spam_dict

        Returns
        -------
        vocab : dict
        """
        vocab = copy.copy(ham_dict)

        for word in spam_dict:
            if word in vocab:
                vocab[word] += spam_dict[word]
            else:
                vocab[word] = spam_dict[word]

        return vocab