import copy


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
        self.vocabulary = self.merge_dictionaries(ham.vocabulary, spam.vocabulary)
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
        combined_vacabulary_size = len(self.vocabulary)
        ham_words = sum(ham.vocabulary.values())
        spam_words = sum(spam.vocabulary.values())

        laplace_ham_size = ham_words + combined_vacabulary_size
        laplace_spam_size = spam_words + combined_vacabulary_size

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

    def merge_dictionaries(self, ham_dict, spam_dict):
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