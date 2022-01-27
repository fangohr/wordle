# Wordle advisor
#
# Provide partial information about guesses
# and get suggestions for next guesses.
#
# (C) Hans Fangohr, Jan 2022
# 


############################################
#
# Enter known information here
#
#

# 1. enter letters with known correct positions here:
# If we know the first 4 characters are 'alif', we would type
#
# correct_pos = {"a": 0, "l": 1, "i": 2, "f": 3}
#
# In Python (as in C), the first entry has index 0.
#
# if we don't know any correct letters with correct positions yet, use
#
# correct_pos = {}

correct_pos = {}

# 2. Add letters which you know are wrong and do not occur in the searched
# wordle. These can be added in any order. For example, if
# the letters x, y, z, a, k, and c are incorrect, we could write:
#
# incorrect_letters = set("xyzakc")
#
# start with an empty set:
#
# incorrect_letters = set("")

incorrect_letters = set("")

# Add letters for which we know that they occur in the wordle, but
# we haven't got the correct position yet. Enter the wrong position as
# an index.
#
# For example: if 'm' is in the word but not in the first position
# (=index 0), and  'q' is in the word but not in the third
# position (=index 2), write:
#
# incorrect_position = {'m': 0, 'q':2}
#
# start with empty dictionary:
#
# incorrect_position = {}

incorrect_position = {}

#
# No changes needed below here
#
###################################################




import urllib

# Import the Memory class from joblib (to cache word list)
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

# Download word list
words = get_word_list()

# select only those words that are 5 characters long
sel = [word for word in words if len(word) == 5]

# what letters must be in the wordle?
must_include = set(incorrect_position.keys())

print(f"Found {len(sel)} words with 5 characters.")

for letter in correct_pos:
    sel = [word for word in sel if word[correct_pos[letter]] == letter]
    print(f"With {letter} at index {correct_pos[letter]} : {len(sel)}")

for letter in must_include:
    sel = [word for word in sel if letter in word]
    print(f" with '{letter}': {len(sel)} remaining.")

# make use of known incorrect position
for letter in incorrect_position:
    sel = [word for word in sel if not word[incorrect_position[letter]] == letter]
    print(
        f" without '{letter}' at index {incorrect_position[letter]}: {len(sel)} remaining."
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
