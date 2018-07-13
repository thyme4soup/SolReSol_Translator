import winsound
import time
import requests


srs_dict = {}

def get_synonyms(word):
    url_base = "http://www.stands4.com/services/v2/syno.php"
    params = {
        "uid" : "wack"
        "tokenid" : "waack"
        "word" : word
    }
    response = requests.get(url_base, params=params)
    print(response.contents)

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
        word = words[i]
        words[i] = srs_dict.get(word, "")
        if words[i] == "":
            print("dropping from sentence \"{}\" : {}".format(sentence, word))
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

def play_srs_serial(srs_serial):
    srs_frq = {
        1 : 261, #do, C
        2 : 293, #re
        3: 329, #mi
        4: 349, #fa
        5: 391, #sol
        6: 440, #la
        7: 466 #si
    }
    for tone_num in srs_serial:
        frq = srs_frq.get(tone_num, None)
        if frq != None:
            winsound.Beep(frq, 200)
        else:
            time.sleep(0.2)

            

            
            
#print(srs_dict)

haiku = "Your gentle kiss and other feral bliss haunt my recollection"

x = translate("hello how are you")
y = translate("what is your name")
#print((x, srs_to_serial(x)))
#print((y, srs_to_serial(y)))

play_srs_serial(srs_to_serial(translate(haiku)))
