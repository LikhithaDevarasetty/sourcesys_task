from nltk.stem import PorterStemmer, SnowballStemmer

porter   = PorterStemmer()
snowball = SnowballStemmer("english")

words = ["running", "studies", "happiness", "fairly", "generously"]

print(f"{'Word':14}{'Porter':14}Snowball")
print("-" * 42)

for word in words:
    p = porter.stem(word)
    s = snowball.stem(word)
    print(f"{word:14}{p:14}{s}")