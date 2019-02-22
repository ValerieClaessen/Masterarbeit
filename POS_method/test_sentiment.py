from nltk.corpus import sentiwordnet as swn


print(swn.senti_synset('breakdown.n.03'))
list(swn.senti_synsets('slow'))

happy = swn.senti_synsets('happy', 'a')
happy0 = list(happy)[0]
print(happy0.pos_score())
happy0.neg_score()
happy0.obj_score()
