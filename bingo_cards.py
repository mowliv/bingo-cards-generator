#
# Generate a set of bingo cards from an RTF template file and a phrases file
#
# michaelo, 10/1/99
#

import sys
import random


def replace_string(buf, find_str, new_str):
    split_array = buf.split(find_str)

    if len(split_array) != 2:
        print("replace_string: got %d matches to findStr '%s'" % (len(split_array), find_str))
        assert len(split_array) == 2

    return new_str.join(split_array)


def remove_random_item(array):
    i = random.randint(0, len(array)-1)
    result = array[i]
    del array[i]
    return result


def generate_card(template, _phrases, filename_base, card_num):
    # copy the phrases array since we are going to destroy it.
    phrases = _phrases[:]

    # the first phrase is taken as center square
    center_phrase = phrases[0]
    del phrases[0]

    # this is the replacement string from the template
    match_string = 'ABINGO'
    
    for i in range(25):

        # magic square #12 (the 13th) is the FREE middle square
        if i == 12:
            phrase = center_phrase
        else:
            if not phrases:
                print("Error: ran out of phrases. Must have at least 24 phrases in the phrases file.")
                sys.exit(1)
            phrase = remove_random_item(phrases)
            phrase = '\n' + phrase
        template = replace_string(template, match_string, phrase)
        
        # bump the match string to next (ABINGO, BBINGO, CBINGO, etc)
        match_string = chr(ord(match_string[0])+1) + match_string[1:]

    # stick in the card number
    template = replace_string(template, 'CARD-BINGO', str(card_num))
    
    # write out to some file
    f = open(filename_base + str(card_num) + '.rtf', 'w')
    f.write(template)
    f.close()


def make_cards(template_file, phrases_file, num_cards):
    template = open(template_file).read()
    # load squares and throw out blank lines and comments (start with #)
    phrases = [item.strip() for item in open(phrases_file).readlines() if item.strip() and item[0] != '#']
    assert num_cards > 0
    
    for i in range(num_cards):
        generate_card(template, phrases, 'card ', i + 1)

    print(f"Generated {num_cards} cards as .RTF files")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('usage: bingoCards templateFile phrasesFile numCards')
        sys.exit(0)
        
    make_cards(sys.argv[1], sys.argv[2], int(sys.argv[3]))
