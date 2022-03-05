import operator
import string
from collections import Counter
from itertools import chain
from pathlib import Path

DICT = "sowpods.txt"

ALLOWABLE_CHARACTERS = set(string.ascii_letters)
ALLOWED_ATTEMPTS = 6
WORD_LENGTH = 5

WORDS = {
    word.lower()
    for word in Path(DICT).read_text().splitlines()
    if len(word) == WORD_LENGTH and set(word) < ALLOWABLE_CHARACTERS
}

LETTER_COUNTER = Counter(chain.from_iterable(WORDS))
LETTER_FREQ = {
    character: value / LETTER_COUNTER.total()
    for character, value in LETTER_COUNTER.items()
}


def calculate_word_commonality(word):
    score = 0.0
    for char in word:
        score += LETTER_FREQ[char]
    return score / (WORD_LENGTH - len(set(word)) + 1)


def sort_by_word_commanality(words):
    sort_by = operator.itemgetter(1)
    return sorted(
        [(word, calculate_word_commonality(word)) for word in words],
        key=sort_by,
        reverse=True)


def display_word_table(word_common):
    for(word, freq) in word_common:
        print(f"{word:<10} | {freq:<5.2}")


def input_word():
    while True:
        word = input("Input the word you entered> ")
        if len(word) == WORD_LENGTH and word.lower() in WORDS:
            break
    return word.lower()


def input_response():
    print("Type the color-coded reply from Wordle:")
    print("  G for Green")
    print("  Y for Yellow")
    print("  ? for Gray")
    while True:
        response = input("Response from Wordle>")
        if len(response) == WORD_LENGTH and set(response) <= {"G", "Y", "?"}:
            break
        else:
            print(f"Invalid answer {response}")
    return response


def match_word_vector(word, word_vector):
    assert len(word) == len(word_vector)
    for letter, v_letter in zip(word, word_vector):
        if letter not in v_letter:
            return False
    return True


def match(word_vector, all_words):
    return [word for word in all_words if match_word_vector(word, word_vector)]


def solver():
    all_words = WORDS.copy()
    word_vector = [set(string.ascii_lowercase) for _ in range(WORD_LENGTH)]
    for attempt in range(1, ALLOWED_ATTEMPTS + 1):
        print(f"Attempt {attempt} with {len(all_words)} possible words")
        display_word_table(sort_by_word_commanality(all_words)[:15])
        word = input_word()
        response = input_response()
        for index, letter in enumerate(response):
            if letter == "G" or "g":
                word_vector[index] = {word[index]}
            elif letter == "Y" or "y":
                try:
                    word_vector[index].remove(word[index])
                except KeyError:
                    pass
            elif letter == "?":
                for vector in word_vector:
                    try:
                        vector.remove(word[index])
                    except KeyError:
                        pass
        all_words = match(word_vector, all_words)


if __name__ == '__main__':
    solver()

