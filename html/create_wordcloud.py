from wordcloud import WordCloud

def main(doc):

    ######## fill in  dicts with strings #############

    data = doc['body'] + doc['answers'] + doc['title']

    try:
        data += doc['accepted_answer']
    except:pass

    # make wordcloud
    cloud = WordCloud().generate(data)

    # store file
    cloud.to_file('static/clouds/' + doc['id'] + ".png")

    # make html text to return
    resultstring = "<div id='wordcloud'><img id='wordcloudimg' src='static/clouds/" + doc['id'] + ".png'></div>"

    return resultstring
