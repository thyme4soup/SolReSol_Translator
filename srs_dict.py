
import os
import time
from thesaurus import Word

if os.name == "nt":
    import winsound
    windows = True
else:
    from pysine import sine
    windows = False

srs_dict = {}

def get_synonyms(word):
    my_word = Word(word)
    return my_word.synonyms()

def clean(word):
    word = word.strip()
    acc = ""
    for ch in word:
        acc += ch.lower()
    return acc

with open("solresol.txt","r") as dict_file:
    for line in dict_file:
        srs, eng = line.split("\t")
        for word in eng.split(', '):
            srs_dict[clean(word)] = srs.lower()

def translate(sentence):
    words = sentence.split(' ')
    acc = ""
    for i in range(len(words)):

        word = clean(words[i])
        words[i] = srs_dict.get(word, "")

        if not words[i] == "":
            pass
        else:
            synonyms = get_synonyms(word)
            syn = 0
            while words[i] == "" and syn < len(synonyms):
                words[i] = srs_dict.get(synonyms[syn], "")
                syn += 1
            if words[i] == "":
                print("dropping from sentence \"{}\" : {}".format(sentence, word))
            else:
                print("substituted \"{}\" for \"{}\"".format(synonyms[syn-1], word))

    return " ".join([x for x in words if x != ""])
   
def srs_tone_to_int(srs):
    switcher = {
        " " : 0,
        "do" : 1,
        "re" : 2,
        "mi" : 3,
        "fa" : 4,
        "sol" : 5,
        "la" : 6,
        "si" : 7
    }
    return switcher.get(srs, None)
    

def srs_to_serial(sentence):
    ser_acc = []
    acc = ""
    for ch in sentence:
        acc += ch
        int_srs = srs_tone_to_int(acc)
        if not int_srs == None:
            ser_acc.append(int_srs)
            acc = ""
    if not acc == "":
        print("potential error in translation of {}".format(sentence))
    return ser_acc

def play_srs_serial(srs_serial, tone_time=0.2):

    srs_frq = {
        1 : 261, #do, C
        2 : 293, #re
        3: 329, #mi
        4: 349, #fa
        5: 391, #sol
        6: 440, #la
        7: 466 #si
    }

    if windows:
        for tone_num in srs_serial:
            frq = srs_frq.get(tone_num, None)
            if frq != None:
                winsound.Beep(frq, tone_time * 1000)
            else:
                time.sleep(tone_time)
    else:
        for tone_num in srs_serial:
            frq = srs_frq.get(tone_num, None)
            if frq != None:
                sine(frequency = frq, duration = tone_time)
            else:
                time.sleep(tone_time)

def play_from_sentence(sentence, tone_time=0.2):
    play_srs_serial(srs_to_serial(translate(sentence)), tone_time=tone_time)


############

#haiku = "Your gentle kisses and other feral blisses haunt my memory"
#print(haiku)
#play_from_sentence(haiku, tone_time=0.15)

play_from_sentence("hello world", tone_time=0.2)

user_input = ""
while user_input.lower() != "exit":
    user_input = raw_input("Type a sentence, exit to leave\n")
    play_from_sentence(user_input, 0.2)

############
