import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = """Football is a family of team sports that involve, to varying degrees, kicking a ball to score a goal. Unqualified, the word football normally means the form of football that is the most popular where the word is used. Sports commonly called football include association football (known as soccer in North America, Ireland and Australia); gridiron football (specifically American football or Canadian football); Australian rules football; rugby union and rugby league; and Gaelic football.[1] These various forms of football share, to varying degrees, common origins and are known as "football codes".

There are a number of references to traditional, ancient, or prehistoric ball games played in many different parts of the world.[2][3][4] Contemporary codes of football can be traced back to the codification of these games at English public schools during the 19th century.[5][6] The expansion and cultural influence of the British Empire allowed these rules of football to spread to areas of British influence outside the directly controlled Empire.[7] By the end of the 19th century, distinct regional codes were already developing: Gaelic football, for example, deliberately incorporated the rules of local traditional football games in order to maintain their heritage.[8] In 1888, The Football League was founded in England, becoming the first of many professional football associations. During the 20th century, several of the various kinds of football grew to become some of the most popular team sports in the world.[9]"""


def summarizer(rowdocs):
       stopwords = list(STOP_WORDS)
       #print(stopwords)
       nlp = spacy.load('en_core_web_sm')
       doc=nlp(rowdocs)
       #print(doc)
       tokens = [token.text for token in doc]
       #print(tokens)
       word_freq = {}
       for word in doc:
          if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
               if word.text not in word_freq.keys():
                    word_freq[word.text] = 1
               else:
                   word_freq[word.text] +=1
       #print(word_freq)
       max_freq = max(word_freq.values())
       #print(max_freq)
       for word in word_freq.keys():
            word_freq[word] = word_freq[word]/max_freq
       #print(word_freq)
       sent_tokens = [sent for sent in doc.sents]
       #print(sent_tokens)
       sent_scores = {}
       for sent in sent_tokens:
            for word in sent:
                 if word.text in word_freq.keys():
                      if sent not in sent_scores.keys():
                           sent_scores[sent] = word_freq[word.text]
                      else:
                           sent_scores[sent] += word_freq[word.text]
       #print(sent_scores)
       select_len = int(len(sent_tokens)*0.3)
       #print(select_len)
       summary = nlargest(select_len, sent_scores,key=sent_scores.get)
       #print(summary)
       final_summary = [word.text for word in summary]
       summary = ' '.join(final_summary)
       #print(text)
       #print(summary)
       #print("length of orginal text ",len(text.split(' ')))
       #print("length of summary text ",len(summary.split(' ')))
       return summary,doc,len(rowdocs.split(' ')),len(summary.split(' '))

      
     