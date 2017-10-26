import json
import nltk
from collections import Counter,defaultdict

def create_wordcloud(doc,lang):
    data = ""

    with open('json_files/'+doc+'.json', 'r') as js:
        data = json.load(js)

    article = {}
    ######## fill in  dicts with strings#############
    for i,val in data.items():
        if type(data[i]) is not int:
            data[i] = repr(data[i]).lower() #make data to lowercase and only str
        if i == 'body':
            article[i] = val
        elif i == 'answers':
            article[i] = val
        elif i == 'accepted_answer':
            article[i] = val
    content = ""
    article_big ={}
    # concatenate all the strings element in one string list
    for _,v in article.items():
        content +=" "+v
        article_big[doc] = content


    ############# tokenize dict #################
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+')

    for i in article_big:
        article_big[i] = tokenizer.tokenize(article_big[i])

    ############ stem dicts ########################
    from nltk.corpus import stopwords

    filtered_article = article_big
    item_to_remove = []
    for key,word in filtered_article.items():
        if word in stopwords.words(lang):
            item_to_remove.append(word)
    for sw in item_to_remove:
        try:
            filtered_article['body'].remove(sw)
        except:pass
        try:
            filtered_article['answer'].remove(sw)
        except:pass
        try:
            filtered_article['accepted_answer'].remove(sw)
        except:pass
    article_big = filtered_article

    ############### count words in data_file #####################
    count_dict = Counter()
    for key,word in article_big.items():
        for sent in word:
            count_dict.update([sent])
    count_dict = Counter({ind: count_dict for ind, count_dict in count_dict.items() if count_dict > 2})
    # print c.most_common()

    ############### create text occurence for cloud ###################
    txt = ""
    for key,val in count_dict.items():
        txt +=" "+key
    txt = txt.strip()
    return txt
