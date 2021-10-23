from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')


class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()

    def get_doc_id(self, doc):
        """ Splits each line of the document, into doc_id & text.
            Already implemented"""
        arr = doc.split("\t")
        return int(arr[0]), arr[1]

    def tokenizer(self, text):
        """ Implement logic to pre-process & tokenize document text.
            Write the code in such a way that it can be re-used for processing the user's query.
            To be implemented."""
        filtered_text = re.sub('([^a-zA-Z0-9]+)|(\s\s+)', ' ', text)
        stripped_text = filtered_text.strip()
        tokens = stripped_text.split(' ')

        filtered_tokens = filter(lambda token: token not in self.stop_words, tokens)
        filtered_tokens = filter(lambda token: token != '', filtered_tokens)

        stemmed_tokens = [self.ps.stem(token) for token in filtered_tokens]

        return stemmed_tokens


if __name__ == "__main__":
    preprocessor = Preprocessor()
    print(preprocessor.ps.stem('Epidemiological'))
    print(preprocessor.ps.stem('Epidemiología'))
    print(preprocessor.ps.stem('Epidemiologic'))