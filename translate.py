#!/usr/bin/python3

import os 
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
FILENAME = 'cedict_ts.u8'
cedict_file_path = dir_path + '/' + FILENAME
known_words_file_path = dir_path + '/' + 'known_words.txt'

line_count = 0

words = {}

# Parses dictionary file
with open(cedict_file_path) as f:
    for line in f:
        if line.startswith('#'):
            continue
        line_count = line_count + 1

        new_word = {}

        space_index = line.index(' ')
        traditional = line[:space_index]
        new_word['traditional'] = traditional

        line = line[space_index+1:]

        space_index = line.index(' ')
        simplified = line[:space_index]
        new_word['simplified'] = simplified

        line = line[space_index+1:]

        pinyin_start = line.index('[')
        pinyin_end = line.index(']')
        pinyin = line[pinyin_start+1:pinyin_end]
        new_word['pinyin'] = pinyin

        line = line[pinyin_end+1:]

        definition = line[:len(line)-1] # removes trailing return
        new_word['definition'] = definition

        if simplified in words.keys():
            words[simplified].append(new_word)
        else:
            words[simplified] = [new_word]


# Parses known words file
known_words = set([])
with open(known_words_file_path) as f:
    for line in f:
        known_words.add(line[:len(line)-1])


#print('words.keys() is ' + str(words.keys()))

vocab = set([])

# handles translation
for line in sys.stdin:
    index = 0
    line = line[:len(line)-1] # remove trailing return
    while(index < len(line)):
        # just using word length of one. You can handle longer words later
        word_length = 6
        found = False
        for word_length in range(1,6)[::-1]:
            token = line[index:index+word_length]
            if token in words.keys():
                index += word_length
                if token not in known_words:
                    if token not in vocab:
                        vocab.add(token)
                break
            if (word_length == 1):
                index += 1

for token in vocab:
    word_list = words[token]
    for word in word_list:
        print(word['simplified'] + ' ' + word['pinyin'] + ' ' + word['definition'])
