import nltk
import re
import nltk.tag as nt
import nltk.data
##default_tagger = nltk.data.load(nt._pos_tag)
##model = {'11am': 'AVB'}
##tagger = nltk.tag.UnigramTagger(model=model, backoff=default_tagger)
class ChunkParser(nltk.ChunkParserI):
    def __init__(self, train_sents):
        train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)]  for sent in train_sents]
        self.tagger = nltk.TrigramTagger(train_data)  
    def parse(self, sentence):
        pos_tags = [pos for (word,pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word,pos),chunktag)              in zip(sentence, chunktags)]
        return nltk.chunk.conlltags2tree(conlltags) 
sentence = [("AM", "NT"), ("PM", "NT"), ("\d{1,2}:\d{1,2}", "EX"), ("\d{1,2}:\d{1,2}-\d{1,2}:\d{1,2}", "EX")]   # a simple sentence with POS tags  
pattern = "NP: {<EX>?<NT>}"  # define a tag pattern of an NP chunk  
NPChunker = nltk.RegexpParser(pattern) # create a chunk parser   
result = NPChunker.parse(sentence)

ex=["Full closure at Alaska  12:01-5 AM  1-6AM 11.30 pm  -1am 16th jump street"]
ex2 = ["Full Closure on 23/12/2015 at 11 am - 2:01 pm"]
def pl():
    try:
        for token in ex:
            tk = nltk.word_tokenize(token)
            tagged = nltk.pos_tag(tk)
            print(tagged)
            
##            chunk = r"""
##                Chunk:
##                    {<CD><am|pm>}
##                """
##            namedEnt = nltk.ne_chunk(tagged, binary=False)
##            namedEnt.draw()
##            cp = nltk.RegexpParser(chunk)
##            chunked = cp.parse(namedEnt)
##            print(chunked)
##            chunked.draw()
            time.sleep(555)
    except Exception, e:
        print str(e)

##pl()


string = "Full closure at Alaska  12:01-5AM  1-6AM 12:01am-5:45pm 1am 11:30pm  1am-6pm 16th jump street 12 "


xxx = time_extract(string)


