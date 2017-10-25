import testsearch
import search

# Convert input_text to prepare for request
def query_handler(input_text):
    htmltext = ""
    # Add here extra data that needs to be showed above

    results = search.search_in_index(text=input_text)

    for article in results['hits']['hits']:
        htmltext += create_div_from_dict(article)
    return htmltext


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
