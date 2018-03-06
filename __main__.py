import argparse

parser = argparse.ArgumentParser(description='Run Naive Bayes and Logistic Regression on given dataset and report '
                                             'accuracy')

# arguments
#  ham_directory
#  spam_directory
#  lambda
#  limit_iterations
#  filter_stop_words

parser.add_argument('ham_directory', type=str, help="Path to directory containing all the ham")
parser.add_argument('spam_directory', type=str, help="Path to directory containing all the spam")
parser.add_argument('lambda', type=int, help="Regularization parameter for logistic regression")
parser.add_argument('limit_iterations', type=int, help="Hard limit on number of iterations for logistic regression")
parser.add_argument('filter_stop_words', type=str, help="Whether to filter stop words or not")

args = parser.parse_args()
