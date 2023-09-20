import re
import collections
import string
import subprocess


def analyze_text(text, min_length, max_length):
    repeated_phrases = {}
    for length in range(min_length, max_length + 1):
        phrases = generate_phrases(text, length)
        for phrase, count in phrases.items():
            if count > 1:
                repeated_phrases[phrase] = count
    return repeated_phrases


def generate_phrases(text, phrase_length):
    words = [word.strip(string.punctuation).lower() for word in text.split()]
    phrases = {}
    for i in range(len(words) - phrase_length + 1):
        phrase = " ".join(words[i:i + phrase_length])
        if phrase in phrases:
            phrases[phrase] += 1
        else:
            phrases[phrase] = 1
    return phrases


def open_file(file_path):
    if file_path.endswith(".odt"):
        subprocess.call(["unoconv", "-f", "txt", file_path])
        text_file_path = file_path[:-4] + ".txt"
        with open(text_file_path, "r") as text_file:
            text = text_file.read()
        subprocess.call(["rm", text_file_path])

        return text
    else:
        with open(file_path, "r") as file:
            text = file.read()

    return text


def get_phrases(text, min_words, max_words, min_repetitions):
    results_text = ""
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)
    words = text.split()
    repeated_phrases = collections.defaultdict(int)
    for i in range(len(words) - min_words + 1):
        for j in range(min_words, max(min_words, min(len(words) - i, max_words)) + 1):
            repeated_phrases[" ".join(words[i:i+j])] += 1

    for phrase, count in repeated_phrases.items():
        if count >= min_repetitions:
            results_text += f"{phrase}: {count}\n"

    return results_text


def save_file(file_path, results):
    try:
        with open(file_path, "w") as file:
            file.write(results)
        return 0
    except:
        return -1


def analyze_text(text, min_length, max_length):
    repeated_phrases = {}
    for length in range(min_length, max_length + 1):
        phrases = generate_phrases(text, length)
        for phrase, count in phrases.items():
            if count > 1:
                repeated_phrases[phrase] = count
    return repeated_phrases


def test_phrases():
    file_path = "/home/jonathan/Documents/Writing/Edits in progress/The Frog of War.txt"
    text = open_file(file_path)

    print(get_phrases(text, 2,5, 3))


if __name__ == '__main__':
    test_phrases()
