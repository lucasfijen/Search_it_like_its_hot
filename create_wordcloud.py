import json
import nltk
from collections import Counter,defaultdict

def create_wordcloud():
    data = ""

    with open('json_files/3dprinting1006.json', 'r') as js:
        data = json.load(js)

    article = {}
    ########fill in  dicts with strings#############
    for i in data:
        if type(data[i]) is not int:
            data[i] = repr(data[i]).lower() #make data to lowercase and only str
        if i == 'body':
            article[i] = data[i]
        elif i == 'answers':
            article[i] = data[i]
        elif i == 'accepted_answer':
            article[i] = data[i]

    ############# tokenize dict #################
    for i in article:
        article[i] = nltk.word_tokenize(article[i])


    ############ stem dicts ###########################
    from nltk.corpus import stopwords
    filtered_article = article
    item_to_remove = []
    for i in article:
        for word in article[i]:
            if word in stopwords.words('english'):
                item_to_remove.append(word)

    # for elem in filtered_article:
    #     for t,word in filtered_article.items():
    #         for el in word:
    #             if el in item_to_remove:
    #                 print filtered_article.pop(t,0)
    # print filtered_article

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

    article = filtered_article
    ############### count words in data_file #####################
    c = Counter()
    for i in article:
        for word in article[i]:
            c.update([word])
    print c.most_common()

    ############### create word cloud #########################
    txt = ""
    for i in c:
        for j in range(c[i]):
            txt +=" "+i
    txt = txt.strip()
    return txt
