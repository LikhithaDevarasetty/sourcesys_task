import nltk
nltk.download('wordnet', quiet=True)
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

words = ["running", "cats", "better", "studies", "geese"]

# Lemmatize as verb (pos='v') or noun (pos='n')
for word in words:
    as_noun = lemmatizer.lemmatize(word, pos='n')
    as_verb = lemmatizer.lemmatize(word, pos='v')
    print(f"{word:10} → noun: {as_noun:10} | verb: {as_verb}")