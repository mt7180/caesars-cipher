import sys
from collections import Counter, defaultdict


def encode_text(text, key):
    """Return encoded text by cyclically shifting each letter by
    'key'-number of letters in the alphabet,
    e.g.: encode_text("abc", "26-3")
    """
    try:
        converted_key = int(key)
    except:
        try:
            # only simple sum OR simple subtraction possible
            if "+" in key: converted_key = sum(map(int, key.split("+")))
            elif "-" in key: converted_key = subtract(map(int, key.split("-")))
            else: raise ValueError("Wrong key for encoding given.")   # add usage
        except Exception as e:
            print("Unexpected Error on given key: ", e)
            return
    
    return "".join((encode_letter(letter, converted_key) 
                          if letter.isalpha() 
                          else letter for letter in text))


def encode_letter(letter, key):
    """Return encoded letter by cyclically shifting it by "key" number
    of letters in the alphabet
    """
    a_limit = 65 if letter.isupper() else 97
    return chr((ord(letter) + key - a_limit) % 26 + a_limit)


def subtract(raw_input):
    """Return the value of subtracting all list items from the first item"""
    lst = list(raw_input)
    return lst[0] - sum(lst[1:])


def string_histogram(text):
    """Return dictionary of letters : frequency of each letter
    in given text
    """
    char_generator = (chr.lower() for chr in text if chr.isalpha())
    return dict(Counter(char_generator))  # Fussnote (2)


def frequencies(histogram):
    """Return pobability vector for occurence of each letter in the
    alphabet based on given histogram
    """
    total_letter_count = sum(histogram.values())
    return [count / total_letter_count 
            if (count := histogram.get(chr(ord), None)) 
            else 0 
            for ord in range(97,123)]


def crack_caesar(exampletext, text):
    """Return the decoded text by using the letter frequency probability of a given exampletext 
    and compare it to the letter probability vector of the en-/ decoded text, 
    The solution with a minimized chi-squared value should be the result
    """
    prob_E_vec = frequencies(string_histogram(exampletext))
    chi_values = {}

    for i in range(26):
        chi_squared = 0
        prob_O_vec = frequencies(string_histogram(encode_text(text,26-i)))
    
        for prob_E, prob_O in zip(prob_E_vec, prob_O_vec):
            if prob_E != 0:
                chi_squared += (prob_O-prob_E) * (prob_O-prob_E) / prob_E
    
        chi_values[str(26-i)] = chi_squared
    
    min_chi_tuple = min(chi_values.items(), key = lambda x : x[1])
    return encode_text(text, min_chi_tuple[0])

if __name__ == "__main__":

    puzzle = ("Xka pl fq fp. Clo qefp qfjb F tfii ibxsb vlr: Ql-jloolt, "
              "fc vlr mibxpb ql pmbxh tfqe jb, F tfii zljb eljb ql vlr; "
              "lo, fc vlr tfii, Zljb eljb ql jb, xka F tfii txfq clo vlr.")

    try:
        with open("example.txt", "r") as f:
            exampletext = f.read()
    except Exception as e:
        print("Can not open mandatory file example.txt: ", e)
        raise SystemExit(
            "\nPlease add example.txt with the text \"Julius Caesar\""
            "of William Shakespear to project folder to evaluate a \""
            "pobability vector."
        )

    print("\ncrack caesars text!")
    print(crack_caesar(exampletext, puzzle),"\n")
    
    if len(sys.argv) < 3: 
        raise SystemExit("""
        ... Error, wrong number of command line parameters. 
        Please give the parameters \"text\" and key to encode a given text.

        Usage: caesar.py \"text\" key\n
        parameters:
            text   : text to be encoded
            key    : cyclical shift of each letter by \"key\"-number of letters in the alphabet

        (e.g. \"Das ist ein Text.\" 3) ... program exits now""")

    print(f"Encode the text: \"{sys.argv[1]}\" with key: {sys.argv[2]}")
    print(encode_text(*sys.argv[1:]), "\n")

    print("Histogram for the given text")
    print(string_histogram(sys.argv[1]), "\n")

######
#
# (1):
# string conversion only necessary if key is given by sys.argv string-"calculation"
# e.g.: encode_text("abc", "26-3"). 
# If function is called internally with integer calculation in key parameter: encode_text("abc", 26-3)
# key is simply converted in try section by integer casting

def string_histogram2(text):
    """Return dictionary of letters : frequency of each letter in given text"""
    char_frequency_dict = defaultdict(int)  # default value is 0, no if/ else differentiation if key already in dict is necessary
    for letter in text:
        if letter.isalpha():
            char_frequency_dict[letter.lower()] += 1
    return dict(char_frequency_dict)