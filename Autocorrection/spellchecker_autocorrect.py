import nltk
import string

from spellchecker import SpellChecker


def correctSentence(sentence_to_correct):

    words = nltk.word_tokenize(sentence_to_correct)


    spell = SpellChecker()

    corrected_sentence = []
    for word in words:
        corrected_sentence.append(spell.correction(word))   #schreibe alle Wörter, sowohl die die eine Korrektur bekommen haben also auch die ohne, in eine Liste
    #print(corrected_sentence)

    sentence = ""
    for part in corrected_sentence: #gehe durch die Liste
        if part not in string.punctuation:  #alle Wörter die kein Satzzeichen sind bekommen ein Leerzeichen vorangestellt
            sentence = sentence + " " + part
        else:
            sentence = sentence + part


    return sentence.lstrip()    #wegschneiden des ersten Leerzeichens

#print(correctSentence("When whte people commit mass shoootings they are never shot, they are apprehended and go to jail."))