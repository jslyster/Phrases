import re
import collections
import string
import access_docx as ad
from ODTReader.odtreader import odtToText
import platform

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


def open_file(file_path, file_type):
    match file_type:
        case "odt":
            return odtToText(file_path)
        case "docx":
            return ad.get_docx_text(file_path)
        case other:
            with open(file_path, "r") as file:
                return file.read()


def get_phrases(text, min_words, max_words, min_repetitions):
    results_dict = {}
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)
    words = text.split()
    repeated_phrases = collections.defaultdict(int)
    for i in range(len(words) - min_words + 1):
        for j in range(min_words, max(min_words, min(len(words) - i, max_words)) + 1):
            repeated_phrases[" ".join(words[i:i+j])] += 1

    for phrase, count in repeated_phrases.items():
        if count >= min_repetitions:
            results_dict[phrase] = count

    return results_dict


def save_results_as_text(file_path, results):
    print(platform.system())
    if platform.system() == 'Windows':
        end_of_line = '\r\n'
    else:
        end_of_line = '\n'
    results_text = ""
    for phrase, count in results.items():
        results_text += phrase + ": " + str(count) + end_of_line

    try:
        with open(file_path, "w") as file:
            file.write(results_text)

        return 0
    except:
        return -1


def save_results_as_csv(file_path, results):
    results_csv = ""
    for phrase, count in results.items():
        results_csv += '"' + phrase + '", "' + str(count) + '"\n'

    try:
        with open(file_path, "w") as file:
            file.write(results_csv)
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

    results = get_phrases(text, 2,5, 3)

    # file_path = "/home/jonathan/Documents/Writing/Edits in progress/Results.txt"
    file_path_csv = "/home/jonathan/Documents/Writing/Edits in progress/Results.csv"

    # save_results_as_text(file_path, results)
    save_results_as_csv(file_path_csv, results)


def test_odt():
    file_path = "/home/jonathan/Documents/Writing/Edits in progress/The Road to Elysium.odt"
    print(odtToText(file_path))

if __name__ == '__main__':
    # test_phrases()
    test_odt()
