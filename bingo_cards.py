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
    # copy the phrasesarray since we are going to destroy it.
    phrases = _phrases[:]
    
    match_string = 'ABINGO'
    
    for i in range(25):

        # magic square #12 (the 13th) is the FREE middle square
        if i == 12:
            square = "\n\nYou're on Mute (FREE!)"
        else:
            phrase = remove_random_item(phrases)
            phrase = '\n' + phrase.strip()
        template = replace_string(template, match_string, phrase)
        
        # bump the match string to next
        match_string = chr(ord(match_string[0])+1) + match_string[1:]

    # stick in the card number
    template = replace_string(template, 'CARD-BINGO', str(card_num))
    
    # write out to some file
    f = open(filename_base + str(card_num) + '.rtf', 'w')
    f.write(template)
    f.close()


def make_cards(template_file, phrases_file, num_cards):
    template = open(template_file).read()
    # load squares and throw out blank lines
    phrases = list(filter(lambda x: x, open(phrases_file).readlines()))
    assert num_cards > 0
    
    for i in range(num_cards):
        generate_card(template, phrases, 'card ', i + 1)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('usage: bingoCards templateFile phrasesFile numCards')
        sys.exit(0)
        
    make_cards(sys.argv[1], sys.argv[2], int(sys.argv[3]))
