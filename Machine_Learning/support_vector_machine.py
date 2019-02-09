import csv

# function to use the support vector machine algorithm on a dataset
def do_svm():
    """
    We use the Support Vector Machine (with k-nearest neighbour) algorithm to determine the class of each tweet.
    We work with our data_list containing all stemmed and processed tweets and our sentiment_lexicon.

    First we need to estimate the vectors for each tweet. The values of the vector are the number of times each word of our lexicon appears in our tweet.
    Then we compare for each tweet its vector with all other vectors to find the ones most similar. To do this, we need to estimate the normalized dot product.

    The sentiment of our tweet is estimated by the (intellectually assigned) sentiment of the k tweets with the most similar vector
    (k=3 or k=5, whichever gets the better results).
    """

    return