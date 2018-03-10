import math
import pandas as pd
from file_reader import utilities as u


class NaiveBayes:
    def __init__(self, ham, spam):
        """
        Initialize the NaiveBayes classifier
        Parameters
        ----------
        ham : FileReader
            FileReader object containing document count and dictionary for ham documents

        spam : FileReader
            FileReader object containing document count and dictionary for spam documents
        """
        self.total = ham.document_count + spam.document_count
        self.vocabulary = u.FileUtilities.merge_dictionaries(ham.vocabulary, spam.vocabulary)
        self.priors = {'ham': ham.document_count / self.total, 'spam': spam.document_count / self.total}
        self.conditionals = self.train(ham, spam)

    def train(self, ham, spam):
        """
        Calculates the posterior probabilities for data set

        Parameters
        ----------
        spam : FileReader
        ham : FileReader

        Returns
        -------
        vocab : dict
        """
        vocab = {}

        # calculating variables needed again instead of asking for length each time
        combined_vocabulary_size = len(self.vocabulary)
        ham_words = sum(ham.vocabulary.values())
        spam_words = sum(spam.vocabulary.values())

        laplace_ham_size = ham_words + combined_vocabulary_size
        laplace_spam_size = spam_words + combined_vocabulary_size

        # calculating priors for each word now
        for word in self.vocabulary:
            count_in_ham = 1  # since we are using Laplace smoothing, set to 1 in case word doesn't exist
            if word in ham.vocabulary:
                count_in_ham += ham.vocabulary[word]
            conditional_for_ham = count_in_ham / laplace_ham_size

            count_in_spam = 1
            if word in spam.vocabulary:
                count_in_spam += spam.vocabulary[word]

            conditional_for_spam = count_in_spam / laplace_spam_size

            vocab[word] = {
                'ham': conditional_for_ham,
                'spam': conditional_for_spam
            }
        return vocab

    def apply(self, ham_files, spam_files):
        """
        Apply Naive Bayes on all documents, return the
        Parameters
        ----------
        ham_files
        spam_files

        Returns
        -------
        results: DataFrame
        """
        results = pd.DataFrame({}, columns=["file", "class", "classified", "accurate"])

        ham_prior = self.priors['ham']
        spam_prior = self.priors['spam']
        for c in ['ham', 'spam']:
            if c == 'ham':
                files = ham_files.files
            else:
                files = spam_files.files

            for file in files:
                score_ham = math.log(ham_prior)
                score_spam = math.log(spam_prior)
                words = u.FileUtilities.get_word_frequency(file)

                for word in words:
                    if word in self.conditionals:
                        score_ham += math.log(self.conditionals[word]['ham'])
                        score_spam += math.log(self.conditionals[word]['spam'])
                classified_as = 'spam'
                if score_ham > score_spam:
                    classified_as = 'ham'

                accurate = 0
                if c == classified_as:
                    accurate = 1
                results = results.append({"file": file, "class": c, "classified": classified_as, "accurate": accurate},
                                         ignore_index=True)

        # print("Spam Files:")
        # print(spam_files.files)

        return results
