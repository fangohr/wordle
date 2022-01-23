import urllib

# Import the Memory class from joblib
from joblib import Memory

# Create cache directory
cache_dir = ".joblib-cache"

# Create a memory object
mem = Memory(cache_dir)


@mem.cache(verbose=0)
def get_word_list():
    url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
    words = urllib.request.urlopen(url).read().decode().split()
    return words
    # read world list
    # words = open('english-words/words_alpha.txt', 'rt').read().split()


words = get_word_list()

w5 = [word for word in words if len(word) == 5]

# letters with known correct positions

correct_pos = {"c": 0, "r": 1, "i": 2, "p": 4}
# correct_pos = {'e': 4, 'i': 1, 'n': 2, 'c':3}

# known incorrect letters
incorrect_letters = set("alveunons")

# correct letters with known incorrect position
incorrect_position = {"r": 3}
must_include = set(incorrect_position.keys())


sel = w5
print(f"Found {len(sel)} words with 5 characters.")

for letter in correct_pos:
    sel = [word for word in sel if word[correct_pos[letter]] == letter]
    print(f"With {letter} in position {correct_pos[letter]} : {len(sel)}")


for letter in must_include:
    sel = [word for word in sel if letter in word]
    print(f" with '{letter}': {len(sel)} remaining.")

# make use of known incorrect position
for letter in incorrect_position:
    sel = [word for word in sel if not word[incorrect_position[letter]] == letter]
    print(
        f" without '{letter}' at pos {incorrect_position[letter]}: {len(sel)} remaining."
    )


for wl in incorrect_letters:
    sel = [word for word in sel if not wl in word]
    print(f" without '{wl}': {len(sel)} remaining.")

# have we checked all vowels?
vowels = set("aeiou")

unchecked_vowels = (
    vowels - incorrect_letters - set(incorrect_position) - set(correct_pos)
)

if unchecked_vowels:
    print(f"Unchecked vowels: {unchecked_vowels}")
    # propose words with the untested vowels:
    for vowel in unchecked_vowels:
        sel = [word for word in sel if vowel in word]
        print(f" with '{vowel}': {len(sel)} remaining.")

print("=== Suggestions ===")
for i in range(min(20, len(sel))):
    print(sel[i])
if len(sel) > 20:
    print("...")
