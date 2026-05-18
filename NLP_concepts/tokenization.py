import nltk
nltk.download('punkt', quiet=True)
from nltk.tokenize import word_tokenize, sent_tokenize

text = "The cats are running quickly. Dogs bark loudly!"

# Word tokenization — split into individual words
words = word_tokenize(text)
print("Words:", words)

# Sentence tokenization — split into sentences
sentences = sent_tokenize(text)
print("Sentences:", sentences)