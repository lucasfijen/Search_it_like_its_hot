import search

# Convert input_text to prepare for request
def query_handler(input_text):
    htmltext = ""
    # Add here extra data that needs to be showed above

    results = search.search_in_index(text=input_text)

    for article in results['hits']['hits']:
        htmltext += create_div_from_dict(article)
    return htmltext

def convert_string_to_dict(input_text):
    # text="", categories=[], date=None, datetype=None, size=10
    results = {'TEXT':'', 'CATEGORY':[], 'EXCLUDE':[], 'TIME':'', 'SIZE':10}

    # make splitted query dict
    splitsquery = input_text.split()
    current_cat = 'TEXT'
    startvalue = 0
    for i in range(len(splitsquery)):

        if splitsquery[i] in results.keys():

            if current_cat in ('CATEGORY', 'EXCLUDE'):
                results[current_cat] = splitsquery[startvalue:i]
            else:
                results[current_cat] = " ".join(splitsquery[startvalue:i])

            current_cat=splitsquery[i]
            startvalue = i + 1

    if startvalue < len(splitsquery):
        results[current_cat] = " ".join(splitsquery[startvalue:])
    # CATEGORY (list of categories that should be searched)
    # and or not
    #
    # EXCLUDE (list of all terms you want to exclude from search)
    #
    #
    # TIME  (split into starting date and value later, incl later, earlier)
    #
    #
    # AMOUNT (how many articles should be searched)
    try:
        results['SIZE'] = int(results['SIZE'])
    except:
        results['SIZE'] = 10

    print(results)
#convert_string_to_dict('cooking an egg EXCLUDE jan piet hein lul SIZE a0')


# creates a single div for a articledict
def create_div_from_dict(article):
    article_dict = article['_source']
    resultstring = "<div id='resultdiv'>"
    if 'title' in article_dict:
        if 'link' in article_dict:
            resultstring += '<a href="http://' + article_dict['link'] + \
                            '" target="_blank">' + article_dict['title'] + '</a>'
        else:
            resultstring += '<h1>' + article_dict['title'] + '</h1>'

    if 'body' in article_dict:
        # Something to only take the first x words
        splittext = article_dict['body'].split(' ')
        text = " ".join(splittext[:100])
        resultstring += '<p>' + text
        if(len(splittext) > 100):
            resultstring += '...'
        resultstring += '</p>'

    resultstring += '</div>'

    return resultstring
