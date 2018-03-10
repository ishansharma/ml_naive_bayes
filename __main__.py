import argparse
from file_reader import file_reader
from naive_bayes import naive_bayes as nb

parser = argparse.ArgumentParser(description='Run Naive Bayes and Logistic Regression on given dataset and report '
                                             'accuracy')
# arguments
#  ham_directory
#  spam_directory
#  lambda
#  limit_iterations
#  filter_stop_words

parser.add_argument('--training_ham_directory', type=str, help="Training directory containing all the ham")
parser.add_argument('--training_spam_directory', type=str, help="Training directory containing all the spam")
parser.add_argument('--test_ham_directory', type=str, help="Test directory containing files classified as ham")
parser.add_argument('--test_spam_directory', type=str, help="Test directory containing files classified as spam")
parser.add_argument('--lambda', type=int, help="Regularization parameter for logistic regression")
parser.add_argument('--limit_iterations', type=int, help="Hard limit on number of iterations for logistic regression")
parser.add_argument('--filter_stop_words', type=str, help="Whether to filter stop words or not")

args = parser.parse_args()

# read ham
ham = file_reader.FileReader(args.training_ham_directory)
print(ham.document_count, "ham files found")

# read spam
spam = file_reader.FileReader(args.training_spam_directory)
print(spam.document_count, "spam files found")

nb_classifier = nb.NaiveBayes(ham=ham, spam=spam)
print("Total training documents:", nb_classifier.total)
# print("Prior probability for ham", nb_classifier.priors['ham'])
# print("Prior probability for spam", nb_classifier.priors['spam'])

# print("Conditional probabilities")
# print(nb_classifier.conditionals)

# test data classification
print("\n====\nRunning Naive Bayes on Test Data")
test_ham = file_reader.FileReader(args.test_ham_directory)
test_spam = file_reader.FileReader(args.test_spam_directory)

r = nb_classifier.apply(test_ham, test_spam)
total_test_docs = r['accurate'].count()
accurately_classified = r['accurate'].sum()
print("Accurate documents:", accurately_classified)
print("Total Documents: ", total_test_docs)
print("Accuracy:", (accurately_classified / total_test_docs) * 100)

