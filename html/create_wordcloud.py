import json
import nltk
from collections import Counter,defaultdict
from wordcloud import WordCloud

def main(doc):
    data = ""

    ######## fill in  dicts with strings#############

    data += doc['body']
    data += doc['answers']
    try:
        data += doc['accepted_answer']
    except:pass
    
    data += doc['title']

    cloud = WordCloud().generate(data)
    
    #store file
    cloud.to_file('static/clouds/' + doc['id'] + ".png")

    resultstring = "<aside id='wordcloud'><img id='wordcloudimg' src='static/clouds/"+doc['id']+".png'></aside>"
    return resultstring